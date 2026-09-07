from pathlib import Path
import sys, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from dikwp_acrs10z.assessment import static_audit
if __name__=='__main__': print(json.dumps(static_audit(str(ROOT/'src'/'dikwp_acrs10z')),ensure_ascii=False,indent=2))
