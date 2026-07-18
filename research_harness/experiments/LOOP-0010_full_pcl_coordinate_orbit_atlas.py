#!/usr/bin/env python3
"""LOOP-0010 full-PCL coordinate principal-minor orbit atlas.

This is a finite exact-coordinate diagnostic, not a proof for arbitrary frames.
For all coordinate rank-two support planes P,Q in C^4 tensor C^4, it computes all
principal minors of M=2I-A-B+(1/2)T, records the determinant update split
  det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S),
and groups examples by coarse combinatorial signatures.
"""
from __future__ import annotations
import itertools, json, importlib.util, math
from collections import defaultdict
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
mod_path=ROOT/'research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py'
if not mod_path.exists():
    mod_path=ROOT/'research_harness/experiments/LOOP-0009_principal_minor_lane.py'
spec=importlib.util.spec_from_file_location('prev', mod_path)
prev=importlib.util.module_from_spec(spec); spec.loader.exec_module(prev)
# Always import LOOP8 for frame construction and PCL matrices.
spec2=importlib.util.spec_from_file_location('loop8', ROOT/'research_harness/experiments/LOOP-0008_full_pcl_search.py')
loop8=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(loop8)

def coord(i): return divmod(i,4)

def plane(indices):
    F=np.zeros((16,2),complex)
    F[indices[0],0]=1; F[indices[1],1]=1
    return F

def trace_vec(Uframe,Vframe):
    t=[]
    for a in range(2):
        for b in range(2):
            U=loop8.mat(Uframe[:,a]); V=loop8.mat(Vframe[:,b])
            t.append(np.vdot(V.reshape(-1),U.reshape(-1)))
    return np.asarray(t,dtype=complex)

def adjugate(A):
    n=A.shape[0]; adj=np.zeros_like(A)
    if n==1: adj[0,0]=1; return adj
    for r in range(n):
        for c in range(n):
            rows=[x for x in range(n) if x!=c]; cols=[x for x in range(n) if x!=r]
            adj[r,c]=((-1)**(r+c))*np.linalg.det(A[np.ix_(rows,cols)])
    return adj

def eval_subset(P,Q,S):
    A,B,T,M,_=loop8.pcl_matrices(P,Q)
    D=2*np.eye(4)-A-B
    t=trace_vec(P,Q)
    I=list(S); DS=D[np.ix_(I,I)]; MS=M[np.ix_(I,I)]; u=t[I]
    detM=float(round(np.linalg.det(MS).real,12))
    detD=float(round(np.linalg.det(DS).real,12))
    upd=0.5*(u @ adjugate(DS) @ np.conjugate(u))
    update=float(round(upd.real,12))
    err=float(abs(np.linalg.det(MS)-(np.linalg.det(DS)+upd)))
    return detM,detD,update,err

def subset_signature(IP,IQ,S):
    # Coarse signature: which P basis vectors and Q basis vectors appear in the selected E_{ab};
    # tensor row/column coordinate multiplicities for those basis vectors; and trace-match count.
    Pcoords=[coord(x) for x in IP]; Qcoords=[coord(x) for x in IQ]
    pairs=[divmod(s,2) for s in S]
    usedP=sorted({a for a,b in pairs}); usedQ=sorted({b for a,b in pairs})
    Psel=[Pcoords[a] for a in usedP]; Qsel=[Qcoords[b] for b in usedQ]
    trace_matches=sum(1 for a,b in pairs if Pcoords[a]==Qcoords[b])
    p_first=len({x[0] for x in Psel}); p_second=len({x[1] for x in Psel})
    q_first=len({x[0] for x in Qsel}); q_second=len({x[1] for x in Qsel})
    # partial trace collision counts inside selected rank-one basis operators
    same_first=sum(1 for (a,b),(c,d) in itertools.combinations(pairs,2) if Pcoords[a][0]==Pcoords[c][0] and Qcoords[b][0]==Qcoords[d][0])
    same_second=sum(1 for (a,b),(c,d) in itertools.combinations(pairs,2) if Pcoords[a][1]==Pcoords[c][1] and Qcoords[b][1]==Qcoords[d][1])
    return f'k={len(S)}|usedP={len(usedP)}|usedQ={len(usedQ)}|p({p_first},{p_second})|q({q_first},{q_second})|trace={trace_matches}|coll({same_first},{same_second})'

def main():
    planes=list(itertools.combinations(range(16),2))
    summary={str(k):{'total':0,'negative_detM':0,'negative_detD':0,'min_detM':math.inf,'min_detD':math.inf,'det_triples':defaultdict(int),'sign_patterns':defaultdict(int),'signature_examples':{}} for k in range(1,5)}
    maxerr=0.0; repaired=[]
    for IP in planes:
        P=plane(IP)
        for IQ in planes:
            Q=plane(IQ)
            for k in range(1,5):
                for S in itertools.combinations(range(4),k):
                    detM,detD,update,err=eval_subset(P,Q,S); maxerr=max(maxerr,err)
                    rec=summary[str(k)]; rec['total']+=1
                    rec['negative_detM']+= int(detM < -1e-10); rec['negative_detD']+= int(detD < -1e-10)
                    rec['min_detM']=min(rec['min_detM'],detM); rec['min_detD']=min(rec['min_detD'],detD)
                    triple=(detM,detD,update); rec['det_triples'][str(triple)]+=1
                    sign=('M-' if detM < -1e-10 else 'M0' if abs(detM)<=1e-10 else 'M+', 'D-' if detD < -1e-10 else 'D0' if abs(detD)<=1e-10 else 'D+')
                    rec['sign_patterns'][str(sign)]+=1
                    sig=subset_signature(IP,IQ,S)
                    if sig not in rec['signature_examples']:
                        rec['signature_examples'][sig]={'plane_P':list(IP),'plane_Q':list(IQ),'subset':list(S),'detM':detM,'detD':detD,'update':update}
                    if detD < -1e-10 and detM >= -1e-10 and len(repaired)<20:
                        repaired.append({'k':k,'plane_P':list(IP),'plane_Q':list(IQ),'subset':list(S),'detM':detM,'detD':detD,'update':update,'signature':sig})
    out={'loop':'LOOP-0010','lane':'full PCL coordinate orbit atlas','claim':'CLAIM-0001','caveat':'finite coordinate-support diagnostic only; not proof for arbitrary frames','max_update_identity_error':maxerr,'summary':{},'repaired_negative_D_examples':repaired,'success_condition_met':False}
    for k,rec in summary.items():
        triples=sorted(rec['det_triples'].items(), key=lambda kv: (-kv[1],kv[0]))
        out['summary'][k]={kk:vv for kk,vv in rec.items() if kk not in ('det_triples','signature_examples','sign_patterns')}
        out['summary'][k]['unique_det_triple_count']=len(rec['det_triples'])
        out['summary'][k]['top_det_triples']=triples[:12]
        out['summary'][k]['sign_patterns']=dict(rec['sign_patterns'])
        out['summary'][k]['coarse_signature_count']=len(rec['signature_examples'])
        out['summary'][k]['signature_examples']=dict(list(rec['signature_examples'].items())[:20])
    outp=ROOT/'research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.json'
    outp.parent.mkdir(parents=True,exist_ok=True); outp.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'max_update_identity_error':maxerr,'by_size':{k:{'total':v['total'],'negative_detM':v['negative_detM'],'negative_detD':v['negative_detD'],'min_detM':v['min_detM'],'min_detD':v['min_detD'],'unique_det_triple_count':len(v['det_triples']),'coarse_signature_count':len(v['signature_examples'])} for k,v in summary.items()},'log':str(outp)},indent=2))
if __name__=='__main__': main()
