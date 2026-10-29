"""Creates only synthetic free media; does not stand in for user confirmation."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/talking-edit/scripts'))
from core import Project,atomic
from media import binary,run,import_file,render,file_hash
from cli import review

p=argparse.ArgumentParser();p.add_argument('--workdir',required=True);p.add_argument('--open-review',action='store_true');a=p.parse_args()
root=Path(a.workdir).resolve();root.mkdir(parents=True,exist_ok=True)
source=root/'fixture.mp4'
if not source.exists():
    run([binary('ffmpeg'),'-v','error','-f','lavfi','-i','testsrc2=size=640x360:rate=25:duration=6','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=6','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(source)])
subs=root/'fixture.srt';subs.write_text('1\n00:00:00,000 --> 00:00:02,000\n第一句测试字幕\n\n2\n00:00:02,000 --> 00:00:04,000\n整句删除测试\n\n3\n00:00:04,000 --> 00:00:06,000\n最后一句测试字幕\n',encoding='utf-8')
project=Project.create(root/'project','免费合成素材验收（非真人审看）')
import_file(project,source,'video');import_file(project,subs,'subtitles')
s=project.state();w=s['workflow'];w['packaging']='none'
project.update({'workflow':w,'cuts':[dict(id='test-cut',start=2,end=4,enabled=True,reason='合成色块测试',reviewed=True)]},s['revision'])
rid=project.open_review('roughcut');project.decide(rid,project.state()['revision'],'confirm',note='仅程序化免费测试，不是用户真实项目授权')
r1=render(project);assert abs(r1['duration']-4)<.15
assert render(project)['file']==r1['file']
s=project.state();s['cues'][0]['text']='只改字幕不改声音';project.update({'cues':s['cues']},s['revision'])
rid=project.open_review('roughcut');project.decide(rid,project.state()['revision'],'confirm',note='仅合成测试')
r2=render(project);assert r1['audio_sha256']==r2['audio_sha256'];assert r1['file']!=r2['file']
atomic(root/'validation.json',{'first':r1,'subtitle_revision':r2,'paid_calls':0})
print(json.dumps({'validation':str(root/'validation.json'),'project':str(project.root),'result':r2},ensure_ascii=False))
if a.open_review:print(json.dumps(review(project,'final',False),ensure_ascii=False))
