#!/usr/bin/env python3
import argparse,json,time
from pathlib import Path
import numpy as np
try:
 from scipy.optimize import minimize
 SCIPY=True
except Exception:
 SCIPY=False

def cvec(i,a):
 v=np.zeros(16,dtype=complex); v[4*i+a]=1; return v

def orth(Z):
 Q,R=np.linalg.qr(Z)
 return Q[:,:2]

def random_plane(rng, support=None):
 if support is None:
  Z=rng.normal(size=(16,2))+1j*rng.normal(size=(16,2))
 else:
  Z=np.zeros((16,2),complex)
  m=len(support)
  W=rng.normal(size=(m,2))+1j*rng.normal(size=(m,2))
  for k,idx in enumerate(support): Z[idx,:]=W[k,:]
 return orth(Z)

def partials(C):
 T=C.reshape(4,4,4,4)
 return np.einsum('iaib->ab',T), np.einsum('iaja->ij',T), np.trace(C)

def gap(C):
 tr1,tr2,tr=partials(C)
 return float(np.real(np.linalg.norm(tr1,'fro')**2+np.linalg.norm(tr2,'fro')**2-0.5*abs(tr)**2-2*np.linalg.norm(C,'fro')**2))

def compK(P,Q):
 Es=[]
 for a in range(2):
  for b in range(2): Es.append(np.outer(P[:,a], Q[:,b].conj()))
 K=np.zeros((4,4),complex)
 for i,E in enumerate(Es):
  tr1E,tr2E,trE=partials(E)
  for j,F in enumerate(Es):
   tr1F,tr2F,trF=partials(F)
   K[i,j]=np.vdot(tr1E,tr1F)+np.vdot(tr2E,tr2F)-0.5*np.conj(trE)*trF-2*np.vdot(E,F)
 return (K+K.conj().T)/2, Es

def eval_planes(P,Q):
 K,Es=compK(P,Q)
 w,V=np.linalg.eigh(K)
 imax=int(np.argmax(w)); lam=float(np.real(w[imax]))
 C=sum(V[j,imax]*Es[j] for j in range(4))
 C=C/np.linalg.norm(C)
 return {'lambda_max':lam,'eigvals':[float(x) for x in w], 'gap_top':gap(C)}

def controls():
 # product projection P=span{|00>,|10>}; Q=span{|00>}1? choose same product equality support span e00,e10
 P=np.column_stack([cvec(0,0),cvec(1,0)]); Q=P.copy()
 prod=eval_planes(P,Q)
 # traceless diag span |00>,|11>
 P=np.column_stack([cvec(0,0),cvec(1,1)]); Q=P.copy()
 tr=eval_planes(P,Q)
 return {'product_projection':prod,'traceless_diagonal':tr}

def support_search(rng,trials):
 supports=[]
 # local low-dimensional rectangles sizes 2x2, 2x3, 3x2 within flattened indices
 for rows in [(0,1),(0,2),(1,2),(2,3),(0,1,2),(1,2,3)]:
  for cols in [(0,1),(0,2),(1,2),(2,3),(0,1,2),(1,2,3)]:
   idx=[4*i+a for i in rows for a in cols]
   if len(idx)>=2: supports.append(idx)
 best={'lambda_max':-9}; count=0
 for suppP in supports:
  for suppQ in supports:
   for _ in range(max(1,trials//(len(supports)**2))):
    P=random_plane(rng,suppP); Q=random_plane(rng,suppQ); r=eval_planes(P,Q); count+=1
    if r['lambda_max']>best['lambda_max']: best=r|{'supportP':suppP,'supportQ':suppQ}
 return {'count':count,'best':best}

def perturb_equalities(rng,trials,eps):
 bases=[np.column_stack([cvec(0,0),cvec(1,0)]), np.column_stack([cvec(0,0),cvec(1,1)])]
 best={'lambda_max':-9}; count=0
 for B in bases:
  for _ in range(trials):
   P=orth(B+eps*(rng.normal(size=(16,2))+1j*rng.normal(size=(16,2))))
   Q=orth(B+eps*(rng.normal(size=(16,2))+1j*rng.normal(size=(16,2))))
   r=eval_planes(P,Q); count+=1
   if r['lambda_max']>best['lambda_max']: best=r|{'eps':eps}
 return {'count':count,'best':best}

def optimize(seed,restarts,maxiter):
 rng=np.random.default_rng(seed)
 def plane_from_x(x):
  z=x[:16]+1j*x[16:32]
  w=x[32:48]+1j*x[48:64]
  P=orth(np.column_stack([z,w]))
  z=x[64:80]+1j*x[80:96]
  w=x[96:112]+1j*x[112:128]
  Q=orth(np.column_stack([z,w]))
  return P,Q
 def obj(x):
  P,Q=plane_from_x(x); return -eval_planes(P,Q)['lambda_max']
 best={'lambda_max':-9}
 for r in range(restarts):
  x=rng.normal(size=128)
  if SCIPY:
   res=minimize(obj,x,method='BFGS',options={'maxiter':maxiter,'gtol':1e-7})
   xx=res.x; success=bool(res.success)
  else:
   xx=x; val=-obj(xx); step=.1; success=False
   for _ in range(maxiter):
    y=xx+step*rng.normal(size=256); vy=-obj(y)
    if vy>val: xx,val=y,vy
    step*=.995
  P,Q=plane_from_x(xx); rr=eval_planes(P,Q)|{'restart':r,'optimizer_success':success}
  if rr['lambda_max']>best['lambda_max']: best=rr
 return best

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=6006); ap.add_argument('--trials',type=int,default=3000); ap.add_argument('--opt-restarts',type=int,default=6); ap.add_argument('--maxiter',type=int,default=150); ap.add_argument('--out',required=True)
 args=ap.parse_args(); rng=np.random.default_rng(args.seed); t=time.time()
 out={'seed':args.seed,'scipy':SCIPY,'controls':controls()}
 out['support_search']=support_search(rng,args.trials)
 out['perturb_eps_0_01']=perturb_equalities(rng,args.trials//2,0.01)
 out['perturb_eps_0_1']=perturb_equalities(rng,args.trials//2,0.1)
 out['optimize']=optimize(args.seed+17,args.opt_restarts,args.maxiter)
 out['best_overall']=max([out['controls']['product_projection'],out['controls']['traceless_diagonal'],out['support_search']['best'],out['perturb_eps_0_01']['best'],out['perturb_eps_0_1']['best'],out['optimize']], key=lambda d:d['lambda_max'])
 out['robust_positive']=out['best_overall']['lambda_max']>1e-8 and out['best_overall']['gap_top']>1e-8
 out['elapsed_sec']=time.time()-t
 Path(args.out).write_text(json.dumps(out,indent=2))
 print(json.dumps({'best_overall':out['best_overall'],'robust_positive':out['robust_positive'],'elapsed_sec':out['elapsed_sec']},indent=2))
if __name__=='__main__': main()
