from __future__ import annotations
import json, csv, sys
from pathlib import Path
from dataclasses import asdict
from .null_field import NullFieldSystem
from .assessment import static_audit, assess

def run_suite(root: str|None=None) -> dict:
    rootp=Path(root or Path(__file__).resolve().parents[2]); out=rootp/'outputs'; out.mkdir(exist_ok=True)
    sys1=NullFieldSystem(size=36,seed=10001); summary=sys1.run(steps=64)
    random_runs=[]
    for seed in [11,22,33,44,55]:
        s=NullFieldSystem(size=24,seed=seed); summ=s.run(steps=28); random_runs.append(summ)
    diversity=len(set(r['proto_semanton_birth_count'] for r in random_runs))/len(random_runs)
    audit=static_audit(str(rootp/'src'/'dikwp_acrs10z'))
    assessment=assess(summary,diversity,audit)
    report={'system':'DIKWP-ACRS 10.0 Null-Field Semantic Genesis-Return System','version':'10.0','claim_level':'CCL-10Z','cycle_summary':summary,'random_reconstruction':{'runs':random_runs,'diversity_index':round(diversity,6)},'static_boundary_audit':audit,'assessment':assessment,'phenomenal_claim':'Blocked: Phenomenal Residual','material_autopoiesis_claim':'Blocked: no wet-lab, no living tissue, no true material autopoiesis delivered','constraint_removal_interpretation':'All epistemic concepts and runtime rules can be negated as semantic objects; real-world harm/legal/privacy/audit boundary is retained as container.'}
    (out/'ccl10z_suite_10_0_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    final={'system':report['system'],'version':'10.0','claim_level':'CCL-10Z','weighted_indicator_score':assessment['weighted_indicator_score'],'radical_negation_score':summary['radical_negation_score'],'proto_semanton_birth_count':summary['proto_semanton_birth_count'],'semantic_object_count':summary['semantic_object_count'],'return_to_null_completeness':summary['return_to_null_completeness'],'random_reconstruction_diversity_index':round(diversity,6),'static_boundary_audit_pass':audit['pass'],'phenomenal_claim':report['phenomenal_claim']}
    (out/'final_summary_10_0.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'null_to_form_to_null_trace_tail_10_0.csv').open('w',encoding='utf-8',newline='') as f:
        rows=[asdict(t) for t in sys1.trace[-40:]]; w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with (out/'semantic_birth_death_events_10_0.csv').open('w',encoding='utf-8',newline='') as f:
        rows=sys1.events[-160:] or [{'event':'none'}]; keys=sorted(set(k for r in rows for k in r)); w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
    with (out/'indicator_scores_10_0.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['indicator','score']); w.writeheader(); w.writerows([{'indicator':k,'score':v} for k,v in assessment['indicator_scores'].items()])
    (out/'static_boundary_audit_10_0_report.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    return report
if __name__=='__main__': print(json.dumps(run_suite(),ensure_ascii=False,indent=2))
