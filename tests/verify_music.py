"""Synthetic integration check: authorized music mix keeps duration/voice and invalidates correctly."""
import sys,json,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/talking-edit/scripts'))
from core import Project,EditError
from media import run,binary,import_file,render,probe
a=argparse.ArgumentParser();a.add_argument('--workdir',required=True);args=a.parse_args();root=Path(args.workdir);root.mkdir(parents=True,exist_ok=True)
run([binary('ffmpeg'),'-v','error','-y','-f','lavfi','-i','testsrc2=size=640x360:rate=25:duration=4','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4','-c:v','libx264','-c:a','aac','-shortest',str(root/'source.mp4')])
run([binary('ffmpeg'),'-v','error','-y','-f','lavfi','-i','sine=frequency=220:sample_rate=32000:duration=1','-c:a','pcm_s16le',str(root/'music.wav')])
p=Project.create(root/'project','免费合成配乐测试');import_file(p,root/'source.mp4','video');music=import_file(p,root/'music.wav','music');music.update(gain_db=-15,fade_seconds=.2)
s=p.state();p.update({'music':music,'cues':[dict(id='a',start=0,end=4,text='配乐测试')],'workflow':dict(s['workflow'],packaging='none')},s['revision'])
p.decide(p.open_review('roughcut'),p.state()['revision'],'confirm','仅合成测试')
try:render(p);raise AssertionError('music rendered without scope confirmation')
except EditError as e:assert e.code=='review_required'
p.decide(p.open_review('packaging'),p.state()['revision'],'confirm','仅合成测试')
r=render(p);assert r['technicalPass'] and abs(r['duration']-4)<.15 and r['music']['sha256']==music['sha256'];assert render(p)['file']==r['file']
assert next(x for x in probe(p.public_file(r['file']))['streams'] if x['codec_type']=='audio')['channels']==2
print(json.dumps({'ok':True,'duration':r['duration'],'mix':r['file'],'paid_calls':0}))
