import json
import shutil
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def resolve(value):
    path=Path(value)
    return path if path.is_absolute() else ROOT/path

def read_json(path):
    with open(resolve(path),encoding='utf-8') as f:
        return json.load(f)

def require_program(program):
    if not shutil.which(program):
        raise RuntimeError(f'{program} is missing from PATH. Install FFmpeg with ffprobe.')

def run(args, *, capture=False):
    cp=subprocess.run([str(x) for x in args],text=True,capture_output=capture,check=False)
    if cp.returncode:
        if capture:
            print(cp.stderr)
        raise RuntimeError(f'Command failed with exit code {cp.returncode}: {args[0]}')
    return cp.stdout if capture else None

def probe(path):
    require_program('ffprobe')
    out=run(['ffprobe','-v','error','-show_entries','stream=index,codec_type,width,height,r_frame_rate:format=duration','-of','json',str(resolve(path))],capture=True)
    data=json.loads(out)
    video=next((s for s in data.get('streams',[]) if s.get('codec_type')=='video'),None)
    if not video: raise ValueError('No video stream found')
    dur=float(data.get('format',{}).get('duration','0') or 0)
    return {'duration':dur,'width':video.get('width'),'height':video.get('height'),'fps':video.get('r_frame_rate'), 'has_audio':any(s.get('codec_type')=='audio' for s in data.get('streams',[]))}
