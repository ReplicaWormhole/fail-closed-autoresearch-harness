# LOOP-0011 scalar slack-domination lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: scalar crossed PAL/PCL mixed Gram slack versus exchange penalty
success_condition_met: none

## Executive verdict

The earlier delegated scalar lane timed out before producing a report, so I repaired it in the controller by running the prepared diagnostic script with bounded parameters.  No proof and no scalar counterexample were found.

The useful output is a sharper diagnostic for the LOOP-0010 scalar bottleneck.  For the crossed scalar minor,

```text
Delta = D1 D2 - |m|^2
      = GramSlack - ExchangePenalty,
GramSlack       = N12 N21 - |m|^2,
ExchangePenalty = N12 N21 - D1 D2.
```

When `N12 N21 > 0`, this is equivalently the ratio inequality

```text
q := D1D2/(N12N21) >= rho := |m|^2/(N12N21).
```

The coordinate equality cases show `ExchangePenalty/GramSlack` can equal `1`; random cases tested were bounded away from `1`, and local optimization moved back toward equality but did not produce a scalar violation.

## Real run output

Command from repository root:

```text
python3 research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py   --samples 1500 --opt-starts 2 --maxiter 60   --out research_harness/logs/LOOP-0011_scalar_slack_domination_lane_seed11011.json   > research_harness/logs/LOOP-0011_scalar_slack_domination_lane_seed11011.stdout.log
python3 -m py_compile research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py
```

Stdout summary:

```json
{
  "coordinate_equality_count": 264,
  "coordinate_equality_signature_count": 3,
  "coordinate_max_ratio": 1.0,
  "coordinate_min_delta": 0.0,
  "random_max_ratio": [0.3025637369333136, 1490],
  "random_min_delta": [1.8042001266381489, 1251],
  "random_min_normalized_gap": [0.6968995627087884, 1490],
  "local_min_delta_objective": 1.4531204332359976e-08,
  "local_max_penalty_ratio_objective": -0.9999970379320856,
  "local_min_normalized_gap_objective": 3.899191214726261e-06
}
```

Control equality values:

```text
product_LOOP9: delta=0.0, slack=0.75, penalty=0.75, ratio=1.0
traceless_LOOP9: delta=0.0, slack=3.75, penalty=3.75, ratio=1.0
```

## Interpretation

The tested equality controls and coordinate scan indicate that the scalar inequality can be sharp exactly when the exchange penalty equals the Gram slack.  Thus a valid proof cannot try to make the penalty negative or absent.  It must prove a genuine cancellation/slack-domination statement.

The coordinate scan found:

```text
total coordinate pairs = 14400
equality count |Delta| <= 1e-12 = 264
equality signature count = 3
positive exchange penalty count = 6848
max penalty/slack ratio = 1.0
min normalized gap q-rho = 0.0
```

The random scan found no near-boundary scalar violation:

```text
samples = 1500
min Delta = 1.8042001266381489 at sample 1251
max penalty/slack ratio = 0.3025637369333136 at sample 1490
min normalized q-rho = 0.6968995627087884 at sample 1490
positive exchange penalty count = 750
max identity/offdiag residual = 8.881784197001252e-16
```

Local BFGS probes moved toward equality:

```text
min Delta objective = 1.4531204332359976e-08
max penalty/slack ratio objective value = -0.9999970379320856  # objective is negative ratio
min normalized gap objective = 3.899191214726261e-06
```

Because the optimization objective for max ratio is negative ratio, the value `-0.9999970379320856` corresponds to ratio near `0.9999970379320856`.  This is equality/near-equality behavior, not a violation.

## Fail-closed caveats

- This is only the scalar crossed minor; even a scalar proof would still need the full PCL/CLAIM bridge handled correctly.
- The script gives finite coordinate/random/local diagnostics and algebraic bookkeeping, not a symbolic proof.
- No certified positive original rank-two gap was produced.
- No hidden Hermitian, normal, positive, or diagonal assumption is used in the general random/local probes.

Artifacts:

- `research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py`
- `research_harness/logs/LOOP-0011_scalar_slack_domination_lane_seed11011.json`
- `research_harness/logs/LOOP-0011_scalar_slack_domination_lane_seed11011.stdout.log`
