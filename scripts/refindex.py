"""Helper to maintain refs/index.json (list of {file,url,licencia,vista,...})."""
import json, os
IDX = os.path.join(os.path.dirname(__file__), '..', 'refs', 'index.json')
def load():
    return json.load(open(IDX)) if os.path.exists(IDX) else []
def add(entry):
    idx = [e for e in load() if e['file'] != entry['file']]
    idx.append(entry)
    idx.sort(key=lambda e: e['file'])
    json.dump(idx, open(IDX, 'w'), indent=1, ensure_ascii=False)
