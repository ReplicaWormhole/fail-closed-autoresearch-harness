# WS-full-pcl-certificate uncertainty

See global `research_harness/uncertainty_ledger.md`.

## LOOP-0012 local uncertainty update

U-0002 remains open.  LOOP-0012 isolates the admissible trace-coupled Schur/rank-one-update object:

```text
S_R(M)=M_RR-c c^*/m,
m=M_ii=D_ii+(1/2)|t_i|^2,
c=M_Ri=D_Ri+(1/2)conj(t_R)t_i.
```

Equivalently, prove all trace-update determinants

```text
det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S) >= 0.
```

The unresolved step is a symbolic Plucker/Gram/SOS proof for these trace-coupled objects.  D-only pivots/minors are again rejected by LOOP-0012 diagnostics.

Artifact: `research_harness/adversarial_reviews/LOOP-0012/full_pcl_certificate_lane.md`.

## LOOP-0013 local uncertainty update

U-0002 remains open. The trace-coupled determinant update identity is separated from the missing PSD certificate. The unresolved target is a symbolic proof of `det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)>=0` for all principal subsets or an equivalent Schur/Gram/SOS certificate for `M`. Artifact: `research_harness/adversarial_reviews/LOOP-0013/full_pcl_certificate_lane.md`.
