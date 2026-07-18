# WS-full-pcl-certificate failed attempts

## D-only pivots / D-only Schur complements

Status: refuted as a proof route.  See global `research_harness/failed_explorations.md` and LOOP-0011/LOOP-0012 diagnostics.

LOOP-0012 strengthened the rejection from principal minors to one-by-one pivot/LDL behavior: in the coordinate scan over `14400` support-pair cases, `D_negative_eig_count=48` and `D_no_nonnegative_pivot_order=120`, while `M` had `M_negative_eig_count=0` and `M_no_nonnegative_pivot_order=0`.  Future Schur arguments must pivot on the trace-coupled `M`, not on `D=2I-A-B`.
