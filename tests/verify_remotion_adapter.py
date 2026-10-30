"""Local synthetic E2E for the Remotion agent adapter and existing review protocol."""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/talking-edit/scripts'))
from core import Project
from media import binary,run,import_file,render
cli=Path(__file__).resolve().parents[1]/'skills/talking-edit/scripts/cli.py'
p=argparse.ArgumentParser();p.add_argument('--workdir',required=True);p.add_argument('--remotion-project',required=True);p.add_argument('--browser',required=True);a=p.parse_args()
root=Path(a.workdir);root.mkdir(parents=True,exist_ok=True)
source=root/'synthetic.mp4';run([binary('ffmpeg'),'-v','error','-y','-f','lavfi','-i','testsrc2=size=640x360:rate=25:duration=2','-f','lavfi','-i','sine=frequency=440:duration=2','-c:v','libx264','-c:a','aac','-shortest',str(source)])
project=Project.create(root/'project','仅合成素材适配测试');import_file(project,source,'video');s=project.state();workflow=dict(s['workflow'],packaging='remotion-plugin')
project.update({'workflow':workflow,'cues':[{'id':'cue','start':0,'end':1.9,'text':'合成测试'}],'scenes':[{'id':'s','start':0,'end':2,'mode':'fullscreen','title':'合成测试'}]},s['revision'])
for stage in ('roughcut','packaging'):project.decide(project.open_review(stage),project.state()['revision'],'confirm','隔离合成素材测试')
def command(*args):
 result=subprocess.run([sys.executable,str(cli),'--project',str(project.root),*args],capture_output=True);data=json.loads(result.stdout);assert data['ok'],data;return data['result']
scene=command('render-scene','--scene','s','--code',a.remotion_project,'--entry','src/index.tsx','--composition','FreeTestPanel','--browser',a.browser)
command('attach-scene','--scene','s','--video',scene['video'],'--keyframe',scene['keyframe'],'--code',scene['code'],'--entry','src/index.tsx','--component','FreeTestPanel','--source-revision','synthetic')
project.decide(project.open_review('keyframes'),project.state()['revision'],'confirm','隔离合成素材测试')
result=render(project);assert result['technicalPass'] and result['animation_count']==1 and abs(result['duration']-2)<.15
print(json.dumps({'ok':True,'duration':result['duration'],'animation_count':result['animation_count']}))
