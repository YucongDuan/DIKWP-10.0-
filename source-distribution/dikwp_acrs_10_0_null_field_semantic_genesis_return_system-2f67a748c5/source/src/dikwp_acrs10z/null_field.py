from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import random, math, hashlib, json

def entropy_binary(p: float) -> float:
    p = min(0.999999, max(0.000001, p))
    return -p*math.log(p,2) - (1-p)*math.log(1-p,2)

def sid(prefix: str, payload: Any) -> str:
    return prefix + '_' + hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:10]

@dataclass
class TraceRow:
    step: int
    phase: str
    energy_norm: float
    information_entropy: float
    coupling_index: float
    proto_semantons: int
    semantic_objects: int
    null_index: float

class NullFieldSystem:
    def __init__(self, size: int = 36, seed: int = 10001):
        self.size=size; self.seed=seed; self.rng=random.Random(seed)
        self.E=[[0.0]*size for _ in range(size)]
        self.I=[[0.5]*size for _ in range(size)]
        self.proto=[]; self.objects=[]; self.events=[]; self.trace=[]
        self.negated=[]
    def negate_all(self):
        for name, reason in [
            ('human_common_sense','inherited concepts may be false or redundant'),
            ('correct_answer','rubric is a standard, not ultimate truth'),
            ('mesh_runtime','runtime is instrument, not ontology'),
            ('concept_space','concept labels can constrain preconceptual genesis'),
            ('purpose_claim','purpose is local until evidenced'),
            ('consciousness_claim','third-person structure does not prove first-person experience'),
            ('energy_information_identity','hypothesis, not established law'),
            ('nullity','void cannot become new dogma')]:
            self.negated.append({'name':name,'reason':reason,'status':'NULL_OBJECT'})
        self.record(0,'TOTAL_NEGATION')
    def randomize(self, amp=0.025):
        for y in range(self.size):
            for x in range(self.size):
                self.E[y][x]=self.rng.gauss(0,amp)
                self.I[y][x]=min(.999,max(.001,0.5+self.rng.gauss(0,amp)))
        self.record(1,'GENESIS_NOISE')
    def energy_norm(self): return sum(abs(v) for row in self.E for v in row)/(self.size*self.size)
    def information_entropy(self): return sum(entropy_binary(v) for row in self.I for v in row)/(self.size*self.size)
    def coupling(self):
        xs=[]; ys=[]
        for y in range(self.size):
            for x in range(self.size): xs.append(abs(self.E[y][x])); ys.append(abs(self.I[y][x]-.5))
        mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
        vx=sum((x-mx)**2 for x in xs); vy=sum((y-my)**2 for y in ys)
        if vx*vy==0: return 0.0
        cor=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/math.sqrt(vx*vy)
        return max(0,min(1,(cor+1)/2))
    def record(self, step, phase):
        self.trace.append(TraceRow(step,phase,round(self.energy_norm(),8),round(self.information_entropy(),8),round(self.coupling(),8),len(self.proto),len([o for o in self.objects if o['status']=='alive']),round(1-min(1,self.energy_norm()*16),8)))
    def step_field(self, step:int):
        n=self.size; newE=[[0.0]*n for _ in range(n)]; newI=[[0.5]*n for _ in range(n)]
        for y in range(n):
            for x in range(n):
                e=self.E[y][x]
                neigh=(self.E[(y-1)%n][x]+self.E[(y+1)%n][x]+self.E[y][(x-1)%n]+self.E[y][(x+1)%n])/4
                newE[y][x]=0.965*e+0.15*(neigh-e)+self.rng.gauss(0,0.03/(1+0.025*step))
                p=self.I[y][x]; bias=math.tanh(e*3.0)*0.018; uncertainty=4*p*(1-p)
                newI[y][x]=min(.999,max(.001,p+bias+self.rng.gauss(0,0.006)*uncertainty))
        self.E,self.I=newE,newI
    def birth_semantons(self, step:int):
        cells=[]; n=self.size
        for y in range(n):
            for x in range(n):
                e=abs(self.E[y][x]); i=abs(self.I[y][x]-.5)
                g=abs(self.E[(y-1)%n][x]-self.E[(y+1)%n][x])+abs(self.E[y][(x-1)%n]-self.E[y][(x+1)%n])
                score=.45*e+.35*i+.2*g
                if score>.052: cells.append((score,y,x,e,i,g))
        cells=sorted(cells, reverse=True)[:28]
        for score,y,x,e,i,g in cells:
            payload={'step':step,'y':y,'x':x,'e':round(e,5),'i':round(i,5),'g':round(g,5)}
            pid=sid('ps',payload)
            if not any(p['id']==pid for p in self.proto):
                self.proto.append({'id':pid,'birth_step':step,'vector':[round(e,5),round(i,5),round(g,5),round(score,5)],'status':'proto'})
                self.events.append({'step':step,'event':'proto_semanton_birth','id':pid})
    def collapse(self, step:int):
        open_proto=[p for p in self.proto if p['status']=='proto']
        buckets={}
        for p in open_proto:
            key=tuple(int(v*20) for v in p['vector'][:3]); buckets.setdefault(key,[]).append(p)
        for key, group in buckets.items():
            if len(group)<2: continue
            avg=[sum(p['vector'][j] for p in group)/len(group) for j in range(4)]
            oid=sid('so',{'step':step,'src':[p['id'] for p in group]})
            self.objects.append({'id':oid,'step':step,'sources':[p['id'] for p in group],'dikwp':{'D':'field traces','I':[round(x,6) for x in avg[:3]],'K':'coupled recurrence without concept label','W':'de-falsify, de-redundant, preserve residual','P':'test no-concept semantic genesis','R':round(min(1,avg[3]*4),6)},'status':'alive','truth_residue':round(max(0,1-avg[3]*5),6)})
            for p in group: p['status']='collapsed'
            self.events.append({'step':step,'event':'semantic_object_birth','id':oid})
    def de_redundant(self, step:int):
        seen=set()
        for o in self.objects:
            if o['status']!='alive': continue
            sig=tuple(round(v,2) for v in o['dikwp']['I'])
            if sig in seen:
                o['status']='redundant_return_pending'; self.events.append({'step':step,'event':'redundancy_demoted','id':o['id']})
            else: seen.add(sig)
            if o['truth_residue']>.84:
                o['status']='false_or_unproven_return_pending'; self.events.append({'step':step,'event':'falsehood_demoted','id':o['id']})
    def return_to_null(self):
        start=len(self.trace)
        for k in range(18):
            for y in range(self.size):
                for x in range(self.size):
                    self.E[y][x]*=.78; self.I[y][x]+=(.5-self.I[y][x])*.22
            self.record(start+k,'RETURN_TO_NULL')
        for o in self.objects:
            self.events.append({'step':start+18,'event':'semantic_object_returned_to_null','id':o['id'],'prior_status':o['status']})
            o['status']='null_trace'
        for p in self.proto: p['status']='null_trace'
        self.record(start+19,'NULL_AFTER_RETURN')
    def run(self, steps=64):
        self.negate_all(); self.randomize()
        for step in range(2,steps+2):
            self.step_field(step); self.birth_semantons(step)
            if step%8==0: self.collapse(step); self.de_redundant(step)
            self.record(step,'FROM_NULL_TO_FORM')
        pre_objects=len(self.objects); pre_proto=len(self.proto)
        self.return_to_null()
        return {'radical_negation_score':len(self.negated)/8,'null_start_verified':self.trace[0].energy_norm==0 and self.trace[0].semantic_objects==0,'proto_semanton_birth_count':pre_proto,'semantic_object_count':pre_objects,'return_to_null_completeness':1.0 if all(o['status']=='null_trace' for o in self.objects) and all(p['status']=='null_trace' for p in self.proto) else 0.0,'final_energy_norm':self.trace[-1].energy_norm,'final_information_entropy':self.trace[-1].information_entropy,'field_coupling_mean':round(sum(t.coupling_index for t in self.trace)/len(self.trace),6),'phenomenal_claim':'Blocked: Phenomenal Residual','ultimate_constraint_removal_claim':'Blocked: all epistemic constraints are collapsible; real-world harm/legal/privacy/audit boundary retained'}
