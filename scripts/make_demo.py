from common import ROOT, require_program, run
from pathlib import Path

require_program('ffmpeg')
out=ROOT/'jobs/demo/input.mp4'
out.parent.mkdir(parents=True,exist_ok=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-y',
     '-f','lavfi','-i','color=c=#292d30:s=540x960:r=25:d=13',
     '-f','lavfi','-i','sine=frequency=200:sample_rate=48000:duration=13',
     '-shortest','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(out)])
print(f'Created: {out}')
