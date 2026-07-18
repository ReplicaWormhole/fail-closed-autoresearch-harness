# Co-mathematician mode for CLAIM-0001

Adopted: 2026-06-03T20:01:29+02:00
Reference inspiration: arXiv:2605.06651, "AI co-mathematician: Accelerating mathematicians with agentic AI".

This repository no longer treats the automatic research process as a bare sequence of proof-search cron ticks.  It is a stateful mathematical workspace with a project coordinator, approved goals, persistent workstreams, uncertainty tracking, failed-route memory, progressive disclosure, and review gates.

## Operating principles

1. Human-centered research support, not autonomous publication.
   - The system assists the mathematician by reducing uncertainty, surfacing bottlenecks, and producing auditable artifacts.
   - It must escalate when stuck rather than silently burn loops or converge to reviewer-pleasing prose.

2. Mathematics beyond proofs.
   - Valid outputs include literature notes, counterexample searches, equality geometry, proof skeletons, executable diagnostics, formalizable lemmas, and working-paper sections.
   - Only auditor-accepted complete proofs/counterexamples/bridge defects count as success.

3. Stateful workspace.
   - High-level state is maintained in `PROJECT_STATE.md`, `GOALS.md`, `dashboard.md`, `uncertainty_ledger.md`, `failed_explorations.md`, and `status.json`.
   - Low-level artifacts live in workstream directories, loop directories, scripts, and logs.

4. Progressive disclosure.
   - Default user-facing output should report dashboard-level status, not raw subagent chatter.
   - Every high-level claim must link to the workstream/loop/script/log that supports it.

5. Persistent workstreams.
   - Workstreams are attached to approved goals and persist across loops.
   - A loop may advance one or more workstreams, spawn new ones, or escalate a blocked workstream.

6. Uncertainty as a first-class object.
   - Any unresolved lemma, numerical-only observation, bridge assumption, or refuted shortcut belongs in `uncertainty_ledger.md` or `failed_explorations.md`.

7. Hard review gates.
   - Workstream outputs require review before being marked complete.
   - Skeptic/auditor approval must be about mathematical content, not polish.
   - If reviewers cycle without progress, mark `death_spiral_stop` or `blocked_escalate` rather than revising forever.

8. Human steering and escalation.
   - If the same bottleneck survives repeated loops with no material reduction, open an escalation item and pause or request user steering depending on `status.json`.

## Success gates

Success is recorded only when an auditor accepts one of:

- complete proof of the original rank-two partial-trace inequality;
- certified reconstructable rank-two positive-gap counterexample;
- accepted bridge defect showing the active target must be replaced.

All other progress remains fail-closed.
