#!/usr/bin/env python3
"""LOOP-0009 zero-mode classification probe.

Reuses LOOP-0008 tangent machinery and inspects the Hessian zero eigenspaces at
known equality controls. Numerical diagnostics only, not a proof.
"""
from __future__ import annotations
import argparse, json, importlib.util, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
mod_path=ROOT/'research_harness/experiments/LOOP-0008_tangent_equality_lane.py'
spec=importlib.util.spec_from_file_location('loop8tan', mod_path)
loop8=importlib.util.module_from_spec(spec); spec.loader.exec_module(loop8)
N=16

def support_projectors(C0):
    U2,s,V2,Uperp,Vperp=loop8.svd_support(C0)
    P=U2@U2.conj().T; Q=V2@V2.conj().T
    Pp=np.eye(N)-P; Qp=np.eye(N)-Q
    return P,Q,Pp,Qp

def block_norms(D,P,Q,Pp,Qp):
    parts={
      'core_PDQ': P@D@Q,
      'right_PDQperp': P@D@Qp,
      'left_PperpDQ': Pp@D@Q,
      'forbidden_PperpDQperp': Pp@D@Qp,
    }
    return {k: loop8.fro2(v) for k,v in parts.items()}

def phase_alignment_zero(D,C0):
    # how much of D lies along i*C0 (unit-sphere phase orbit) as real projection
    ic=1j*C0/math.sqrt(loop8.fro2(C0))
    return float(np.real(loop8.hs(ic,D)))

def analyze_control(name,C0,tol):
    cb=loop8.tangent_complex_basis(C0)
    rb=loop8.orthonormalize_real_tangent_sphere(cb,C0)
    H=loop8.real_quadratic_matrix(rb)
    evals,evecs=np.linalg.eigh(H)
    P,Q,Pp,Qp=support_projectors(C0)
    zero_idx=[i for i,x in enumerate(evals) if abs(x)<=tol]
    neg_idx=[i for i,x in enumerate(evals) if x < -tol]
    modes=[]
    for j in zero_idx:
        D=np.zeros_like(C0)
        for k,b in enumerate(rb): D += evecs[k,j]*b
        modes.append({
            'eig': float(evals[j]),
            'block_norms': block_norms(D,P,Q,Pp,Qp),
            'phase_alignment_iC0': phase_alignment_zero(D,C0),
            'trace_abs': float(abs(np.trace(D))),
            'tr1_fro2': loop8.fro2(loop8.tr1(D)),
            'tr2_fro2': loop8.fro2(loop8.tr2(D)),
            'gap_quadratic': float(np.real(loop8.gap_polar(D,D))),
        })
    # aggregate block norms
    agg={}
    for key in ['core_PDQ','right_PDQperp','left_PperpDQ','forbidden_PperpDQperp']:
        vals=[m['block_norms'][key] for m in modes]
        agg[key]={'min':float(min(vals)) if vals else None,'max':float(max(vals)) if vals else None,'mean':float(np.mean(vals)) if vals else None}
    # Probe finite motion along zero basis vectors: should stay equality/nonpositive to roundoff if symmetry/equality direction.
    sweeps=[]
    for m_idx,j in enumerate(zero_idx[:min(6,len(zero_idx))]):
        D=np.zeros_like(C0)
        for k,b in enumerate(rb): D += evecs[k,j]*b
        vals=[]
        for eps in [1e-1,3e-2,1e-2,3e-3,1e-3]:
            Cp=loop8.tangent_path(C0,D,eps)
            vals.append({'eps':eps,'ngap':loop8.normalized_gap(Cp),'rank':int(np.linalg.matrix_rank(Cp,tol=1e-10))})
        sweeps.append({'mode_index':m_idx,'eig':float(evals[j]),'sweep':vals})
    return {
        'name': name,
        'rank': int(np.linalg.matrix_rank(C0,tol=1e-10)),
        'gap': loop8.gap(C0),
        'real_sphere_tangent_dim': len(rb),
        'zero_count_tol': len(zero_idx),
        'negative_count_tol': len(neg_idx),
        'positive_count_tol': int(np.sum(evals>tol)),
        'eigenvalue_min': float(evals[0]),
        'eigenvalue_max': float(evals[-1]),
        'zero_block_norm_aggregate': agg,
        'zero_modes': modes,
        'zero_mode_sweeps': sweeps,
        'interpretation': 'Numerical zero-mode diagnostics only. Core/right/left block patterns suggest which modes may be support-basis or equality-family directions, but no exact classification is certified.'
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--tol',type=float,default=1e-10); ap.add_argument('--out',type=Path,default=ROOT/'research_harness/logs/LOOP-0009_zero_mode_classification.json')
    args=ap.parse_args()
    controls=loop8.equality_examples()
    res={'loop':'LOOP-0009','claim':'CLAIM-0001','tol':args.tol,'controls':{name:analyze_control(name,C0,args.tol) for name,C0 in controls.items()},'success_condition_met':False,'caveat':'Numerical tangent-zero diagnostics only; not an equality classification proof.'}
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps({name:{'zero_count':r['zero_count_tol'],'positive_count':r['positive_count_tol'],'eigmax':r['eigenvalue_max'],'core_mean':r['zero_block_norm_aggregate']['core_PDQ']['mean']} for name,r in res['controls'].items()},indent=2))
if __name__=='__main__': main()
