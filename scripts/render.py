"""Render a JSON edit plan to a 1080x1920 MP4 with FFmpeg and ASS subtitles.

Plan features:
  segments   list of {start, end, source?, zoom?}; `source` overrides the plan source, `zoom` (e.g. 1.07) punches in
             to disguise a jump cut between two takes with the same framing
  captions   list of {start, end, text} on the final timeline; look comes from the brand profile
  overlays   list of {start, end, x, y, w, h, text, background, color, size}: solid brand-coloured box with centred text
  end_card   {duration, background, logo, logo_tint, lines, text_color, text_size}: brand closing card appended after the segments
  audio      {loudnorm: -16} normalises loudness of the final mix
  caption_style  optional per-job override of brand caption fields, e.g. {"margin_bottom": 1230}
"""
import argparse, json, shutil, subprocess
from pathlib import Path
from common import ROOT, probe, read_json, resolve, require_program, run

p=argparse.ArgumentParser(description='Render approved JSON plan with FFmpeg and ASS subtitles')
p.add_argument('plan',help='Path to plan.json')
p.add_argument('--preview',action='store_true',help='Render a watermarked preview of a draft plan for human review')
a=p.parse_args()
plan=read_json(a.plan)
if plan.get('status')!='approved' and not a.preview:
    raise SystemExit('Plan not approved: set status=approved ONLY after a human approves the shot list. Use --preview for a watermarked review copy.')
output=resolve(plan['output'])
if a.preview: output=output.with_name(output.stem+'-preview'+output.suffix)
segments=plan.get('segments',[])
if not segments: raise SystemExit('No segments specified')
require_program('ffmpeg')
output.parent.mkdir(parents=True,exist_ok=True)
work=output.parent/'_work';work.mkdir(exist_ok=True)

brand={}
if plan.get('brand_profile') and (ROOT/plan['brand_profile']).exists():
    brand=json.loads((ROOT/plan['brand_profile']).read_text(encoding='utf-8'))

ENC=['-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p']
AENC=['-c:a','aac','-ar','48000','-ac','2','-b:a','160k']

# ---- 1. cut and conform every segment ----
clips=[];probed={}
for i,s in enumerate(segments):
    source=resolve(s.get('source') or plan['source'])
    if not source.is_file(): raise SystemExit(f'Source missing: {source}')
    if source.resolve()==output.resolve(): raise SystemExit('Output may not overwrite source')
    info=probed.setdefault(source,probe(source))
    st=float(s['start']); en=float(s['end'])
    if st<0 or en<=st or en>info['duration']+0.1: raise SystemExit(f'Invalid source time range: {s}')
    dur=en-st; z=float(s.get('zoom',1.0))
    if not 1.0<=z<=1.5: raise SystemExit(f'zoom must be between 1.0 and 1.5: {s}')
    W,H=round(1080*z/2)*2,round(1920*z/2)*2
    # punch-in keeps the upper part of the frame, where faces usually are
    vf=f'scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.35,setsar=1,fps=30'
    fade=min(0.03,dur/4)
    af=f'afade=t=in:d={fade},afade=t=out:st={dur-fade:.3f}:d={fade}'
    target=work/f'clip_{i:03d}.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(st),'-t',str(dur),'-i',str(source)]
    if not info['has_audio']: cmd+=['-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000']
    cmd+=['-map','0:v:0','-map','0:a:0' if info['has_audio'] else '1:a:0','-vf',vf,'-af',af,*ENC,*AENC,'-shortest',str(target)]
    run(cmd); clips.append(target)
body_duration=sum(probe(c)['duration'] for c in clips)

# ---- 2. optional brand end card ----
end=plan.get('end_card')
end_duration=0.0
if end:
    end_duration=float(end.get('duration',3.0))
    logo=resolve(end['logo'])
    if not logo.is_file(): raise SystemExit(f'End card logo missing: {logo}')
    bg=end.get('background','#111111').lstrip('#'); tint=end.get('logo_tint','#FFFFFF').lstrip('#')
    r,g,b=(int(tint[k:k+2],16) for k in (0,2,4))
    target=work/'clip_end.mp4'
    fc=(f'[1:v]format=rgba,lutrgb=r={r}:g={g}:b={b},scale={int(end.get("logo_width",620))}:-1:flags=lanczos[lg];'
        f'[0:v][lg]overlay=(W-w)/2:{int(end.get("logo_y",760))},fade=t=in:d=0.4,format=yuv420p[v]')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',f'color=c=0x{bg}:s=1080x1920:r=30:d={end_duration}',
         '-loop','1','-t',str(end_duration),'-i',str(logo),'-f','lavfi','-t',str(end_duration),'-i','anullsrc=channel_layout=stereo:sample_rate=48000',
         '-filter_complex',fc,'-map','[v]','-map','2:a',*ENC,*AENC,'-t',str(end_duration),str(target)])
    clips.append(target)
duration=body_duration+end_duration

listfile=work/'concat.txt'
listfile.write_text(''.join("file '"+str(x.resolve()).replace("'", "'\\''")+"'\n" for x in clips),encoding='utf-8')
joined=work/'joined.mp4'
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listfile),'-c','copy',str(joined)])

# ---- 3. subtitles, overlays, end-card text (ASS) ----
def ass_time(seconds):
    cs=round(float(seconds)*100)
    h=cs//360000; m=(cs//6000)%60; s=(cs//100)%60; c=cs%100
    return f'{h}:{m:02d}:{s:02d}.{c:02d}'

def ass_escape(txt):
    return str(txt).replace('\\','\\\\').replace('{','\\{').replace('}','\\}').replace('\n','\\N')

def ass_colour(hex_colour, opacity=1.0):
    h=hex_colour.lstrip('#'); alpha=round((1-float(opacity))*255)
    return f'&H{alpha:02X}{h[4:6]}{h[2:4]}{h[0:2]}'.upper()

def inline_colour(hex_colour):
    h=hex_colour.lstrip('#'); return f'&H{h[4:6]}{h[2:4]}{h[0:2]}&'.upper()

# per-job overrides (e.g. move captions off a prop) without changing the brand profile
cap={**brand.get('derived_for_video',{}).get('caption',{}),**plan.get('caption_style',{})}
cap_style=(f"Style: Default,{cap.get('font','Noto Sans Georgian')},{cap.get('size',62)},{ass_colour(cap.get('text','#FFFFFF'))},&H000000FF,"
           f"{ass_colour(cap.get('box','#111111'),cap.get('box_opacity',1.0))},&H99000000,{0 if 'font' in cap else 1},0,0,0,100,100,0,0,3,14,0,2,70,70,{cap.get('margin_bottom',250)},1")
lines=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','WrapStyle: 0','',
       '[V4+ Styles]',
       'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
       cap_style,
       'Style: Overlay,Noto Serif Georgian,100,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1',
       f'Style: EndCard,Noto Sans Georgian,{int((plan.get("end_card") or {}).get("text_size",46))},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1',
       'Style: Draft,Noto Sans Georgian,30,&H40FFFFFF,&H000000FF,&H80000000,&H00000000,0,0,0,0,100,100,2,0,3,6,0,7,40,40,150,1',
       '', '[Events]',
       'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
highlight=inline_colour(cap.get('highlight',cap.get('text','#FFFFFF'))); base=inline_colour(cap.get('text','#FFFFFF'))
for c in plan.get('captions',[]):
    start=float(c['start']);finish=float(c['end'])
    if start<0 or finish<=start or finish>body_duration+0.15: raise SystemExit(f'Invalid caption times: {c}')
    text=ass_escape(c['text'])
    # *word* marks a word to show in the brand highlight colour
    parts=text.split('*')
    if len(parts)%2==1 and len(parts)>1:
        text=''.join(pt if k%2==0 else f'{{\\1c{highlight}}}{pt}{{\\1c{base}}}' for k,pt in enumerate(parts))
    lines.append(f'Dialogue: 0,{ass_time(start)},{ass_time(finish)},Default,,0,0,0,,{text}')
for ov in plan.get('overlays',[]):
    st,en=ass_time(ov['start']),ass_time(ov['end']); x,y,w,h=(int(ov[k]) for k in ('x','y','w','h'))
    lines.append(f'Dialogue: 1,{st},{en},Overlay,,0,0,0,,{{\\an7\\pos({x},{y})\\fad(150,150)\\1c{inline_colour(ov.get("background","#111111"))}\\p1}}m 0 0 l {w} 0 {w} {h} 0 {h}{{\\p0}}')
    lines.append(f'Dialogue: 2,{st},{en},Overlay,,0,0,0,,{{\\an5\\pos({x+w//2},{y+h//2})\\fad(150,150)\\fs{int(ov.get("size",100))}\\1c{inline_colour(ov.get("color","#FFFFFF"))}}}{ass_escape(ov.get("text",""))}')
if end:
    y0=int(end.get('text_y',1080))
    for k,txt in enumerate(end.get('lines',[])):
        lines.append(f'Dialogue: 1,{ass_time(body_duration+0.3)},{ass_time(duration)},EndCard,,0,0,0,,{{\\an5\\pos(540,{y0+k*64})\\fad(400,0)\\1c{inline_colour(end.get("text_color","#FFFFFF"))}}}{ass_escape(txt)}')
if a.preview:
    lines.append(f'Dialogue: 3,{ass_time(0)},{ass_time(duration)},Draft,,0,0,0,,DRAFT · მონახაზი')
(work/'captions.ass').write_text('\n'.join(lines)+'\n',encoding='utf-8-sig')

# The ASS filter runs with cwd=work so it needs no absolute path (a Windows drive colon would break the filter string).
ass_filter='ass=captions.ass'
if (ROOT/'fonts').is_dir():
    shutil.copytree(ROOT/'fonts',work/'fonts',dirs_exist_ok=True); ass_filter+=':fontsdir=fonts'
audio=['-c:a','copy']
ln=plan.get('audio',{}).get('loudnorm')
if ln is not None: audio=['-af',f'loudnorm=I={float(ln)}:TP=-1.5:LRA=11',*AENC]
cp=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','joined.mp4','-vf',ass_filter,*ENC,*audio,'-movflags','+faststart',str(output)],cwd=work)
if cp.returncode: raise SystemExit(f'Final render failed: {cp.returncode}')
print('RENDERED:',output)
