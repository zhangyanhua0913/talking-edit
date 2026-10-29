"""Isolated UTF-8 worker: reuse FredTalk's actual roughcut implementation, never its HTTP server."""
import importlib.util
import json
import sys
from pathlib import Path

root=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('fred_review_snapshot',root/'server.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
cuts=module.validate(json.loads((root/'cuts.json').read_text(encoding='utf-8')))
result=module.export(cuts)
result['retained_spans']=module.retained(cuts)
print(json.dumps(result,ensure_ascii=False))
