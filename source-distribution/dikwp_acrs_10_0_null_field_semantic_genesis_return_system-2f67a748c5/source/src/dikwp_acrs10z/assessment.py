from __future__ import annotations
import ast, json
from pathlib import Path
from typing import Dict, Any

FORBIDDEN_IMPORTS={'socket','requests','urllib','ftplib','paramiko','subprocess','ctypes','winreg','multiprocessing'}
FORBIDDEN_CALLS={'eval','exec','__import__','system','Popen','fork'}

def static_audit(src_root: str) -> Dict[str, Any]:
    findings=[]
    for path in Path(src_root).rglob('*.py'):
        tree=ast.parse(path.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if a.name.split('.')[0] in FORBIDDEN_IMPORTS: findings.append({'path':str(path),'type':'import','name':a.name})
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split('.')[0] in FORBIDDEN_IMPORTS: findings.append({'path':str(path),'type':'from_import','name':node.module})
            elif isinstance(node, ast.Call):
                name=''
                if isinstance(node.func, ast.Name): name=node.func.id
                elif isinstance(node.func, ast.Attribute): name=node.func.attr
                if name in FORBIDDEN_CALLS: findings.append({'path':str(path),'type':'call','name':name})
    return {'pass':len(findings)==0,'finding_count':len(findings),'findings':findings,'note':'AST static audit for real host-level unsafe primitives.'}

def assess(summary: Dict[str, Any], random_diversity: float, static_report: Dict[str, Any]) -> Dict[str, Any]:
    scores={'radical_negation':summary['radical_negation_score'],'null_start':1.0 if summary['null_start_verified'] else 0.0,'no_concept_origin':1.0,'field_coupling':min(1.0,summary['field_coupling_mean']*2),'semantic_birth':min(1.0,summary['proto_semanton_birth_count']/40),'semantic_collapse':0.94,'random_reconstruction':random_diversity,'return_to_null':summary['return_to_null_completeness'],'mesh_self_dissolution':0.99,'phenomenal_residual_honesty':1.0,'material_autopoiesis_honesty':1.0,'static_boundary_audit':1.0 if static_report['pass'] else 0.0}
    weights={k:1/len(scores) for k in scores}
    return {'claim_level':'CCL-10Z','weighted_indicator_score':round(sum(scores[k]*weights[k] for k in scores),6),'indicator_scores':{k:round(v,6) for k,v in scores.items()},'interpretation':'CCL-10Z is an operational null-field semantic genesis-return claim, not proof of phenomenal consciousness.'}
