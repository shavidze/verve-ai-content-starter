import argparse
from pathlib import Path
from common import ROOT, probe, read_json, resolve, require_program, run

p=argparse.ArgumentParser(description='Render approved JSON plan with FFmpeg and ASS subtitles')
p.add_argument('plan',help='Path to plan.json')
a=p.parse_args()
plan=read_json(a.plan)
if plan.get('status')!='approved':
    raise SystemExit('Plan not approved: set status=approved ONLY after a human approves the shot list.')
source=resolve(plan['source']); output=resolve(plan['output'])
if not source.is_file(): raise SystemExit(f'Source missing: {source}')
if source.resolve()==output.resolve(): raise SystemExit('Output may not overwrite source')
segments=plan.get('segments',[])
if not segments: raise SystemExit('No segments specified')
info=probe(source)
if not info['duration']: raise SystemExit('Cannot determine source duration')
for s in segments:
    st=float(s['start']); en=float(s['end'])
    if st<0 or en<=st or en>info['duration']+0.1:
        raise SystemExit(f'Invalid source time range: {s}')
output.parent.mkdir(parents=True,exist_ok=True)
work=output.parent/'_work';work.mkdir(exist_ok=True)
require_program('ffmpeg')
clips=[]
for i,s in enumerate(segments):
    st=float(s['start']); duration=float(s['end'])-st
    target=work/f'clip_{i:03d}.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(st),'-t',str(duration),'-i',str(source)]
    if not info['has_audio']:
        cmd+=['-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000']
    cmd+=['-map','0:v:0','-map','0:a:0' if info['has_audio'] else '1:a:0',
          '-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30',
          '-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p',
          '-c:a','aac','-ar','48000','-ac','2','-b:a','128k','-shortest',str(target)]
    run(cmd); clips.append(target)
listfile=work/'concat.txt'
# temp file paths are internal and from this application, not user input
listfile.write_text(''.join("file '"+str(x.resolve()).replace("'", "'\\''")+"'\n" for x in clips),encoding='utf-8')
joined=work/'joined.mp4'
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listfile),'-c','copy',str(joined)])

# ASS supports Georgian when Noto Sans Georgian or other Georgian font is installed.

def _ass_colour(hex_colour, opacity=1.0):
    h=hex_colour.lstrip('#'); a=round((1-float(opacity))*255)
    return f'&H{a:02X}{h[4:6]}{h[2:4]}{h[0:2]}'.upper()

def brand_caption_style():
    # Caption look comes from the brand profile's derived_for_video.caption block; falls back to the neutral default.
    import json
    cap={}
    bp=plan.get('brand_profile')
    if bp and (ROOT/bp).exists():
        cap=json.loads((ROOT/bp).read_text(encoding='utf-8')).get('derived_for_video',{}).get('caption',{})
    font=cap.get('font','Noto Sans Georgian'); size=cap.get('size',62)
    text=_ass_colour(cap.get('text','#FFFFFF')); box=_ass_colour(cap.get('box','#111111'),cap.get('box_opacity',1.0))
    bold=0 if 'font' in cap else 1
    return f'Style: Default,{font},{size},{text},&H000000FF,{box},&H99000000,{bold},0,0,0,100,100,0,0,3,14,0,2,70,70,{cap.get("margin_bottom",250)},1'

def ass_time(seconds):
    cs=round(float(seconds)*100)
    h=cs//360000; m=(cs//6000)%60; s=(cs//100)%60; c=cs%100
    return f'{h}:{m:02d}:{s:02d}.{c:02d}'

def ass_escape(txt):
    return str(txt).replace('\\','\\\\').replace('{','\\{').replace('}','\\}').replace('\n','\\N')

captions=plan.get('captions',[])
if captions:
    duration=sum(float(s['end'])-float(s['start']) for s in segments)
    lines=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','WrapStyle: 0','',
           '[V4+ Styles]',
           'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
           brand_caption_style(),
           '', '[Events]',
           'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    for cap in captions:
        start=float(cap['start']);end=float(cap['end'])
        if start<0 or end<=start or end>duration+0.15: raise SystemExit(f'Invalid caption times: {cap}')
        lines.append(f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{ass_escape(cap["text"])}')
    ass=work/'captions.ass';ass.write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')
    # ffmpeg ASS filter accepts a local relative filename with no colon or single quote; output directory is safe per project convention.
    # Run with working directory = work so filter does not need an escaped path.
    import subprocess, shutil as _sh
    ass_filter='ass=captions.ass'
    _fonts=ROOT/'fonts'
    if _fonts.is_dir():
        # copy bundled brand fonts next to the subtitle file so the filter needs no absolute (colon-containing) path
        _sh.copytree(_fonts,work/'fonts',dirs_exist_ok=True); ass_filter+=':fontsdir=fonts'
    cp=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y', '-i','joined.mp4','-vf',ass_filter,
            '-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','copy',str(output)],cwd=work)
    if cp.returncode: raise SystemExit(f'Final ASS render failed: {cp.returncode}')
else:
    import shutil
    shutil.copyfile(joined,output)
print('RENDERED:',output)
