"""Free regression for phone display matrices, delayed audio, head cuts and speed."""
import argparse
import array
import json
import sys
import wave
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/talking-edit/scripts'))
from core import Project,atomic
from media import binary,run,import_file,render,extract_audio,probe

parser=argparse.ArgumentParser();parser.add_argument('--workdir',required=True);args=parser.parse_args()
root=Path(args.workdir).resolve();root.mkdir(parents=True,exist_ok=True)
run([binary('ffmpeg'),'-v','error','-y','-f','lavfi','-i','testsrc2=size=360x640:rate=25:duration=6','-itsoffset','0.16','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=5.84','-c:v','libx264','-c:a','aac',str(root/'encoded.mp4')])
run([binary('ffmpeg'),'-v','error','-y','-display_rotation','90','-i',str(root/'encoded.mp4'),'-c','copy',str(root/'rotated.mp4')])
p=Project.create(root/'project','Phone clock synthetic regression')
import_file(p,root/'rotated.mp4','video');s=p.state()
p.update({'cues':[dict(id='cue',start=.5,end=2,text='时钟回归')],'cuts':[dict(id='head',start=0,end=.4,enabled=True),dict(id='middle',start=2.3,end=2.55,enabled=True),dict(id='tail',start=s['duration']-.3,end=s['duration'],enabled=True)]},s['revision'])
with wave.open(str(extract_audio(p))) as w:
    samples=array.array('h',w.readframes(w.getnframes()));rate=w.getframerate()
onset=next(i/rate for i,x in enumerate(samples) if abs(x)>300)
assert .12<onset<.19,onset
rid=p.open_review('roughcut');p.decide(rid,p.state()['revision'],'confirm',note='synthetic automated test only')
normal=render(p);assert (normal['width'],normal['height'])==(640,360)
stream=next(x for x in probe(p.root/normal['file'])['streams'] if x['codec_type']=='video')
assert not any(abs(x.get('rotation',0))>1 for x in stream.get('side_data_list',[]))
s=p.state();p.update({'speed':1.1},s['revision']);rid=p.open_review('roughcut');p.decide(rid,p.state()['revision'],'confirm',note='synthetic speed test only')
fast=render(p);assert abs(fast['duration']-fast['mapping'][-1]['output_end'])<.15
atomic(root/'verification.json',dict(audio_onset=onset,normal=normal,speed_1_1=fast))
print(json.dumps(dict(audio_onset=onset,normal_duration=normal['duration'],fast_duration=fast['duration'],display=[normal['width'],normal['height']])))
