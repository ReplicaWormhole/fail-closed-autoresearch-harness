#!/usr/bin/env python3
import argparse, json, sys, time
from pathlib import Path
import numpy as np

try:
    from scipy.optimize import differential_evolution, minimize
    SCIPY=True
except Exception:
    SCIPY=False

def mat_from_vec(v): return v.reshape(4,4)
def inner(A,B): return np.vdot(A,B)  # tr(A^* B)
def orthonormal_pair_from_z(z):
    Z = z[:16] + 1j*z[16:32]
    W = z[32:48] + 1j*z[48:64]
    x1 = Z/np.linalg.norm(Z)
    W = W - x1*np.vdot(x1,W)
    nw=np.linalg.norm(W)
    if nw < 1e-12:
        # deterministic fallback
        e=np.zeros(16,dtype=complex); e[0]=1
        W=e-x1*np.vdot(x1,e); nw=np.linalg.norm(W)
        if nw<1e-12:
            e=np.zeros(16,dtype=complex); e[1]=1
            W=e-x1*np.vdot(x1,e); nw=np.linalg.norm(W)
    x2=W/nw
    return mat_from_vec(x1), mat_from_vec(x2)

def random_pair(rng):
    Z=rng.normal(size=(16,2))+1j*rng.normal(size=(16,2))
    Q,_=np.linalg.qr(Z)
    return mat_from_vec(Q[:,0]), mat_from_vec(Q[:,1])

def pal_values(X1,X2,Y1,Y2):
    L1=X1@Y1.conj().T; L2=X2@Y2.conj().T
    R1=X1.conj().T@Y1; R2=X2.conj().T@Y2
    t1=np.trace(X1.conj().T@Y1); t2=np.trace(X2.conj().T@Y2)
    a=inner(L1,L2)
    b=inner(R1,R2)-0.5*np.conj(t1)*t2
    D1=2-np.linalg.norm(L1,'fro')**2-np.linalg.norm(R1,'fro')**2+0.5*abs(t1)**2
    D2=2-np.linalg.norm(L2,'fro')**2-np.linalg.norm(R2,'fro')**2+0.5*abs(t2)**2
    z=a+np.conj(b)
    viol=abs(z)**2-D1*D2
    return dict(violation=float(np.real(viol)), absz2=float(abs(z)**2), D1=float(np.real(D1)), D2=float(np.real(D2)), z=[float(z.real),float(z.imag)], a=[float(a.real),float(a.imag)], b=[float(b.real),float(b.imag)])

def original_gap_from_frames(X1,X2,Y1,Y2):
    # choose phases making Re(H12) maximal for PAL z and equal singular values at worst ratio; scan s ratio too
    # Build C = s1 |x1><y1'| + s2 |x2><y2'| with y2 phase chosen to align real offdiag.
    vals=pal_values(X1,X2,Y1,Y2)
    z=vals['z'][0]+1j*vals['z'][1]
    # try phase deltas on grid and ratio grid, report max original gap
    x1=X1.reshape(16); x2=X2.reshape(16); y1=Y1.reshape(16); y2=Y2.reshape(16)
    best=-1e9
    bestpar=None
    for th in np.linspace(0,2*np.pi,121,endpoint=False):
        yy2=np.exp(1j*th)*y2
        for r in np.geomspace(1e-3,1e3,241):
            s1=1.0; s2=r
            C=s1*np.outer(x1, y1.conj())+s2*np.outer(x2, yy2.conj())
            C=C/np.linalg.norm(C)
            T=C.reshape(4,4,4,4) # row i,a col j,b
            tr1=np.einsum('iajb->ab', T)
            tr2=np.einsum('iajb->ij', T)
            tr=np.trace(C)
            gap=np.linalg.norm(tr1,'fro')**2+np.linalg.norm(tr2,'fro')**2-2*np.linalg.norm(C,'fro')**2-0.5*abs(tr)**2
            if gap>best:
                best=float(np.real(gap)); bestpar=(float(th), float(r))
    vals['max_original_gap_grid']=best; vals['best_phase_ratio']=bestpar
    return vals

def matrix_unit_sweep():
    units=[]
    for i in range(4):
        for j in range(4):
            M=np.zeros((4,4),complex); M[i,j]=1; units.append((i,j,M))
    best={'violation':-1e9}; count=0; eq=0
    # orthonormal matrix unit pairs are distinct
    for ix,(i1,j1,X1) in enumerate(units):
      for ix2,(i2,j2,X2) in enumerate(units):
        if ix2==ix: continue
        for iy,(k1,l1,Y1) in enumerate(units):
          for iy2,(k2,l2,Y2) in enumerate(units):
            if iy2==iy: continue
            vals=pal_values(X1,X2,Y1,Y2); count+=1
            if abs(vals['violation'])<1e-12: eq+=1
            if vals['violation']>best['violation']:
                best=vals|{'X':[(i1,j1),(i2,j2)],'Y':[(k1,l1),(k2,l2)]}
    return {'count':count,'equalities':eq,'best':best}

def random_search(n, seed):
    rng=np.random.default_rng(seed); best={'violation':-1e9}; negD=0
    for k in range(n):
        X1,X2=random_pair(rng); Y1,Y2=random_pair(rng)
        vals=pal_values(X1,X2,Y1,Y2)
        if vals['D1']<-1e-10 or vals['D2']<-1e-10: negD+=1
        if vals['violation']>best['violation']:
            best=vals|{'iter':k}
    return best, negD

def optimize(seed, maxiter):
    rng=np.random.default_rng(seed)
    def obj(z):
        X1,X2=orthonormal_pair_from_z(z[:128]); Y1,Y2=orthonormal_pair_from_z(z[128:])
        return -pal_values(X1,X2,Y1,Y2)['violation']
    best=None
    for r in range(8):
        z0=rng.normal(size=256)
        if SCIPY:
            res=minimize(obj,z0,method='BFGS',options={'maxiter':maxiter,'gtol':1e-8})
            val=-float(res.fun); z=res.x; success=bool(res.success)
        else:
            z=z0; val=-obj(z); success=False
            step=0.05
            for it in range(maxiter):
                cand=z+step*rng.normal(size=z.shape)
                cv=-obj(cand)
                if cv>val: z,val=cand,cv
                step*=0.999
        X1,X2=orthonormal_pair_from_z(z[:128]); Y1,Y2=orthonormal_pair_from_z(z[128:])
        vals=original_gap_from_frames(X1,X2,Y1,Y2)
        vals.update({'restart':r,'optimizer_success':success})
        if best is None or vals['violation']>best['violation']: best=vals
    return best

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=4004); ap.add_argument('--random',type=int,default=5000); ap.add_argument('--maxiter',type=int,default=300); ap.add_argument('--out',required=True)
    args=ap.parse_args(); t=time.time()
    out={'seed':args.seed,'scipy':SCIPY,'matrix_unit':matrix_unit_sweep()}
    best,negD=random_search(args.random,args.seed); out['random']={'trials':args.random,'best':best,'negative_D_count':negD}
    out['optimize']=optimize(args.seed+17,args.maxiter)
    out['elapsed_sec']=time.time()-t
    Path(args.out).write_text(json.dumps(out,indent=2))
    print(json.dumps({'scipy':SCIPY,'unit_best':out['matrix_unit']['best'],'random_best':best,'opt_best':out['optimize'],'elapsed_sec':out['elapsed_sec']},indent=2))
if __name__=='__main__': main()
