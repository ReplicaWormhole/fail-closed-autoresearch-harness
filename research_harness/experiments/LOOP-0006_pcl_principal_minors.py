#!/usr/bin/env python3
"""LOOP-0006 probes for PCL principal minors of M=-K.

This is not a proof engine. It computes A,B,T,M from the explicit compression
formulas and records principal-minor/equality regressions used by the symbolic
certificate lane report.
"""
import itertools
import numpy as np

n = 4
N = n*n


def mat(u):
    return u.reshape(n, n)


def rand_frame(k, seed):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(N, k)) + 1j*rng.normal(size=(N, k))
    Q, _ = np.linalg.qr(A)
    return Q[:, :k]


def pt1_rank(U, V):
    return U.T @ np.conjugate(V)


def pt2_rank(U, V):
    return U @ V.conj().T


def hs(A, B):
    return np.vdot(A, B)


def blocks(Uframe, Vframe):
    A = np.zeros((4, 4), complex)
    B = np.zeros((4, 4), complex)
    T = np.zeros((4, 4), complex)
    basis = []
    for i in range(2):
        for a in range(2):
            basis.append((i, a, mat(Uframe[:, i]), mat(Vframe[:, a])))
    for p, (i, a, U, V) in enumerate(basis):
        for r, (j, b, X, Y) in enumerate(basis):
            trA = np.vdot(V.reshape(-1), U.reshape(-1))
            trB = np.vdot(Y.reshape(-1), X.reshape(-1))
            A[p, r] = hs(pt1_rank(U, V), pt1_rank(X, Y))
            B[p, r] = hs(pt2_rank(U, V), pt2_rank(X, Y))
            T[p, r] = np.conj(trA) * trB
    M = 2*np.eye(4) - A - B + 0.5*T
    M = (M + M.conj().T)/2
    return A, B, T, M


def example_product():
    F = np.zeros((N, 2), complex)
    F[0, 0] = 1
    F[1, 1] = 1
    return F, F


def example_traceless():
    P = np.zeros((N, 2), complex)
    Q = np.zeros((N, 2), complex)
    P[0, 0] = 1
    P[5, 1] = 1
    Q[0, 0] = 1
    Q[5, 1] = 1
    return P, Q


def principal_minors(M):
    out = []
    for k in range(1, 5):
        for I in itertools.combinations(range(4), k):
            det = np.linalg.det(M[np.ix_(I, I)]).real
            out.append((I, det))
    return out


def summarize(name, U, V):
    A, B, T, M = blocks(U, V)
    print(f"== {name} ==")
    print("M=")
    print(np.array2string(M, precision=12, suppress_small=True))
    print("eig(M)=", np.linalg.eigvalsh(M))
    for I, det in principal_minors(M):
        print("minor", I, f"{det:.16g}")


def main():
    np.set_printoptions(precision=12, suppress=True)
    for name, maker in [("product", example_product), ("traceless", example_traceless)]:
        U, V = maker()
        summarize(name, U, V)

    minima = {k: (float("inf"), -1, ()) for k in range(1, 5)}
    mineig = (float("inf"), -1)
    for s in range(1000):
        U = rand_frame(2, 700000 + 2*s)
        V = rand_frame(2, 700001 + 2*s)
        *_, M = blocks(U, V)
        wmin = np.linalg.eigvalsh(M)[0]
        if wmin < mineig[0]:
            mineig = (float(wmin), s)
        for I, det in principal_minors(M):
            k = len(I)
            if det < minima[k][0]:
                minima[k] = (float(det), s, I)
    print("== random_1000_summary ==")
    print("min eigenvalue", mineig)
    for k in range(1, 5):
        print("min principal minor size", k, minima[k])

if __name__ == "__main__":
    main()
