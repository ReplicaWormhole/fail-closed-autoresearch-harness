#!/usr/bin/env python3
"""LOOP-0009 principal-minor / rank-one-update lane.

Numerically probes all principal minors of the 4x4 PCL matrix
M = D + (1/2) t t^*, D=2I-A-B, and verifies the exact matrix determinant lemma
identity on every principal subset. This is a diagnostic lane, not a proof.
"""
from __future__ import annotations
import argparse, importlib.util, itertools, json, time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
mod_path=ROOT/'research_harness/experiments/LOOP-0008_full_pcl_search.py'
spec=importlib.util.spec_from_file_location('loop8pcl', mod_path)
loop8=importlib.util.module_from_spec(spec); spec.loader.exec_module(loop8)

def trace_vector_from_frames(Uframe,Vframe):
    t=[]
    for i in range(2):
        for a in range(2):
            U=loop8.mat(Uframe[:,i]); V=loop8.mat(Vframe[:,a])
            t.append(np.vdot(V.reshape(-1), U.reshape(-1)))
    return np.asarray(t,dtype=np.complex128)

def det_update_error(D,t,I):
    I=list(I); DS=D[np.ix_(I,I)]; u=t[I]
    lhs=np.linalg.det(DS+0.5*np.outer(np.conj(u),u))
    # polynomial form valid whether DS is invertible or singular: det(D+alpha u u*) = det(D)+alpha u* adj(D) u.
    n=DS.shape[0]
    adj=np.zeros_like(DS)
    for r in range(n):
        for c in range(n):
            rows=[x for x in range(n) if x!=c]
            cols=[x for x in range(n) if x!=r]
            adj[r,c]=((-1)**(r+c))*np.linalg.det(DS[np.ix_(rows,cols)]) if n>1 else 1.0
    # Here the update is outer(conj(u), u), so the determinant-lemma scalar is
    # u^T adj(DS) conj(u), not the Hermitian quadratic conj(u)^T adj(DS) u.
    update=0.5*(u @ adj @ np.conjugate(u))
    rhs=np.linalg.det(DS)+update
    return float(abs(lhs-rhs)), float(np.real(lhs)), float(np.real(np.linalg.det(DS))), float(np.real(update))

def eval_frames(U,V):
    A,B,T,M,Es=loop8.pcl_matrices(U,V)
    D=2*np.eye(4)-A-B
    t=trace_vector_from_frames(U,V)
    w=np.linalg.eigvalsh(M)
    out={'min_eig_M':float(w[0]),'eig_M':[float(x) for x in w],'min_by_size':{},'negative_counts':{},'max_rank_one_update_error':0.0,'examples':{}}
    for k in range(1,5):
        rec=[]
        for I in itertools.combinations(range(4),k):
            err,detM,detD,update=det_update_error(D,t,I)
            out['max_rank_one_update_error']=max(out['max_rank_one_update_error'],err)
            rec.append({'I':list(I),'detM':detM,'detD':detD,'trace_update_adj_term':update,'update_error':err})
        rec.sort(key=lambda r:r['detM'])
        out['min_by_size'][str(k)]=rec[0]
        out['negative_counts'][str(k)]=sum(r['detM'] < -1e-10 for r in rec)
        # keep most repaired subset: detD negative but detM nonnegative, if any
        repaired=[r for r in rec if r['detD'] < -1e-10 and r['detM'] > -1e-10]
        if repaired:
            repaired.sort(key=lambda r:r['detD'])
            out['examples'][f'repaired_size_{k}']=repaired[0]
    return out

def coordinate_scan():
    planes=[]
    for I in itertools.combinations(range(loop8.N),2):
        F=np.zeros((loop8.N,2),complex); F[I[0],0]=1; F[I[1],1]=1; planes.append((I,F))
    best_by_size={str(k):None for k in range(1,5)}; neg_pairs={str(k):0 for k in range(1,5)}; repaired=[]; total=0
    worst_eig=None
    for IP,P in planes:
        for IQ,Q in planes:
            total+=1; r=eval_frames(P,Q)
            if worst_eig is None or r['min_eig_M'] < worst_eig['min_eig_M']:
                worst_eig={'plane_P':list(IP),'plane_Q':list(IQ), **r}
            for k,v in r['min_by_size'].items():
                if r['negative_counts'][k]: neg_pairs[k]+=1
                if best_by_size[k] is None or v['detM'] < best_by_size[k]['detM']:
                    best_by_size[k]={'plane_P':list(IP),'plane_Q':list(IQ), **v}
            for name,ex in r['examples'].items():
                if len(repaired)<8:
                    repaired.append({'plane_P':list(IP),'plane_Q':list(IQ),'kind':name,**ex})
    return {'total_pairs':total,'negative_pair_counts_by_size':neg_pairs,'min_by_size':best_by_size,'worst_eig':worst_eig,'sample_repaired_D_by_trace_update':repaired[:8]}

def random_scan(seed,trials):
    rng=np.random.default_rng(seed)
    best_by_size={str(k):None for k in range(1,5)}; neg={str(k):0 for k in range(1,5)}; maxerr=0.0; worst_eig=None
    for j in range(trials):
        P=loop8.random_frame(rng); Q=loop8.random_frame(rng); r=eval_frames(P,Q); maxerr=max(maxerr,r['max_rank_one_update_error'])
        if worst_eig is None or r['min_eig_M'] < worst_eig['min_eig_M']:
            worst_eig={'trial':j, **r}
        for k,v in r['min_by_size'].items():
            if r['negative_counts'][k]: neg[k]+=1
            if best_by_size[k] is None or v['detM'] < best_by_size[k]['detM']:
                best_by_size[k]={'trial':j, **v}
    return {'trials':trials,'negative_frame_counts_by_size':neg,'min_by_size':best_by_size,'worst_eig':worst_eig,'max_update_identity_error':maxerr}

def controls():
    out={}
    # Use LOOP8 equality support controls.
    for name,(U,V) in {
        'product_projection_support_00_10': (np.column_stack([loop8.cvec(0,0), loop8.cvec(1,0)]), np.column_stack([loop8.cvec(0,0), loop8.cvec(1,0)])),
        'diagonal_traceless_support_00_11': (np.column_stack([loop8.cvec(0,0), loop8.cvec(1,1)]), np.column_stack([loop8.cvec(0,0), loop8.cvec(1,1)])),
        'right_product_support_00_01': (np.column_stack([loop8.cvec(0,0), loop8.cvec(0,1)]), np.column_stack([loop8.cvec(0,0), loop8.cvec(0,1)])),
    }.items(): out[name]=eval_frames(U,V)
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=9009); ap.add_argument('--random-trials',type=int,default=2000); ap.add_argument('--out',type=Path,default=ROOT/'research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json')
    args=ap.parse_args(); t0=time.time()
    res={'loop':'LOOP-0009','claim':'CLAIM-0001','lane':'principal-minor rank-one-update diagnostics','controls':controls(),'coordinate_scan':coordinate_scan(),'random_scan':random_scan(args.seed,args.random_trials),'success_condition_met':False,'caveat':'All results are numerical diagnostics/regressions; no principal-minor proof or certified counterexample.','elapsed_sec':time.time()-t0}
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(res,indent=2)+'\n')
    summary={'controls_min_eig':{k:v['min_eig_M'] for k,v in res['controls'].items()},'coordinate_negative_pairs':res['coordinate_scan']['negative_pair_counts_by_size'],'random_negative_frames':res['random_scan']['negative_frame_counts_by_size'],'random_min_by_size':{k:v['detM'] for k,v in res['random_scan']['min_by_size'].items()},'max_update_identity_error':res['random_scan']['max_update_identity_error'],'log':str(args.out),'elapsed_sec':res['elapsed_sec']}
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
