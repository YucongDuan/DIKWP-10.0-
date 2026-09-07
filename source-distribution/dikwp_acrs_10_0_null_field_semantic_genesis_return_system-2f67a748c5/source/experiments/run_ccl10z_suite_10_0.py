from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from dikwp_acrs10z.suite import run_suite
if __name__=='__main__': print(json.dumps(run_suite(str(ROOT))['assessment'],ensure_ascii=False,indent=2))
