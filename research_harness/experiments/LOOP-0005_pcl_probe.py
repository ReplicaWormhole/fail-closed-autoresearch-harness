#!/usr/bin/env python3
"""LOOP-0005 PCL compression probes.

Builds the 4x4 compression matrix K(P,Q) for q(C)=||tr1 C||^2+||tr2 C||^2-.5|tr C|^2-2||C||^2
on Hom(QH,PH), with H=C^4 tensor C^4.  Uses vector<->4x4 matrix convention
u_{ab}=U[a,b].
"""
import numpy as np

n=4
N=n*n

def rand_frame(k, seed):
    rng=np.random.default_rng(seed)
    A=rng.normal(size=(N,k))+1j*rng.normal(size=(N,k))
    Q,_=np.linalg.qr(A)
    return Q[:,:k]

def mat(u):
    return u.reshape(n,n)

def pt1_rank(U,V):
    # trace over first tensor index of |vec(U)><vec(V)|
    return U.T @ np.conjugate(V)

def pt2_rank(U,V):
    # trace over second tensor index of |vec(U)><vec(V)|
    return U @ V.conj().T

def hs(A,B):
    return np.vdot(A,B)

def compression(Uframe,Vframe):
    K=np.zeros((4,4),dtype=complex)
    basis=[]
    for i in range(2):
        for a in range(2):
            basis.append((i,a,mat(Uframe[:,i]),mat(Vframe[:,a])))
    for p,(i,a,U,V) in enumerate(basis):
        for r,(j,b,X,Y) in enumerate(basis):
            trA=np.vdot(V.reshape(-1), U.reshape(-1)) # tr |u><v| = <v,u>
            trB=np.vdot(Y.reshape(-1), X.reshape(-1))
            K[p,r]=hs(pt1_rank(U,V),pt1_rank(X,Y))+hs(pt2_rank(U,V),pt2_rank(X,Y))-0.5*np.conj(trA)*trB-2*(i==j)*(a==b)
    return (K+K.conj().T)/2

def negK_decomp_blocks(Uframe,Vframe):
    # Returns pieces for -K = 2I - A - B + .5 T, where A/B are partial trace Gram? Actually K=A+B-.5T-2I.
    A=np.zeros((4,4),complex); B=np.zeros((4,4),complex); T=np.zeros((4,4),complex)
    basis=[]
    for i in range(2):
        for a in range(2):
            basis.append((i,a,mat(Uframe[:,i]),mat(Vframe[:,a])))
    for p,(i,a,U,V) in enumerate(basis):
        for r,(j,b,X,Y) in enumerate(basis):
            trA=np.vdot(V.reshape(-1), U.reshape(-1))
            trB=np.vdot(Y.reshape(-1), X.reshape(-1))
            A[p,r]=hs(pt1_rank(U,V),pt1_rank(X,Y))
            B[p,r]=hs(pt2_rank(U,V),pt2_rank(X,Y))
            T[p,r]=np.conj(trA)*trB
    return A,B,T

def example_product():
    # P=Q= span{ e0 tensor e0, e0 tensor e1 } gives product-type zero family
    F=np.zeros((N,2),complex)
    F[0,0]=1
    F[1,1]=1
    return F,F

def example_traceless():
    # C= |00><00| - |11><11| is known equality direction; include supports.
    P=np.zeros((N,2),complex); Q=np.zeros((N,2),complex)
    P[0,0]=1; P[5,1]=1
    Q[0,0]=1; Q[5,1]=1
    return P,Q

if __name__=='__main__':
    np.set_printoptions(precision=12,suppress=True)
    for name, maker in [('product',example_product),('traceless',example_traceless)]:
        U,V=maker(); K=compression(U,V); w=np.linalg.eigvalsh(K)
        print(name, 'K eig=', w)
        print(K)
    best=(-99,None)
    vals=[]
    for s in range(2000):
        U=rand_frame(2,100000+2*s); V=rand_frame(2,100000+2*s+1)
        K=compression(U,V); lam=np.linalg.eigvalsh(K)[-1]
        vals.append(lam)
        if lam>best[0]: best=(lam,s)
    print('random trials=2000 max_lambda',best[0],'seed_index',best[1],'min',min(vals),'mean',float(np.mean(vals)))
    # Check block identity numerically for a random case.
    U=rand_frame(2,7); V=rand_frame(2,8); K=compression(U,V); A,B,T=negK_decomp_blocks(U,V)
    print('block_identity_norm', np.linalg.norm(K-(A+B-0.5*T-2*np.eye(4))))
    print('sample eig A+B-.5T', np.linalg.eigvalsh(A+B-0.5*T))
