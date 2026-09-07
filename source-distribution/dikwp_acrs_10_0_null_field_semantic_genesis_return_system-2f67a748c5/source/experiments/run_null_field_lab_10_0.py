from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from dikwp_acrs10z.null_field import NullFieldSystem
if __name__=='__main__':
    s=NullFieldSystem(seed=777); print(json.dumps(s.run(steps=40),ensure_ascii=False,indent=2))
