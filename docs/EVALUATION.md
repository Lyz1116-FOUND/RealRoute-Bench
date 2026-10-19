# Evaluation design and current boundaries

BaseInstance + Scenario defines a task. An independent checker validates routes, coverage, load, timing, resources, relations and rewards, and recomputes objectives. Canonical labels do not change semantics.

## Separate protocols

- Original static city holdout: 1176 distinct tasks; 588 train / 196 validation / 392 test. City-derived scales and scenarios stay together.
- Separate composition holdout: 1512 tasks; 1224 train / 72 validation / 216 test. City worlds are shared across interaction partitions. This does not establish joint city-and-composition generalization.
- Final dynamic-date assignments wait for sequence QA. Missing observations remain missing; later dates cannot replace historical truth.

## Output tracks

Direct returns route JSON. Model returns declarative Scenario JSON, checked against the public task semantics before fixed-solver execution. A deterministic parser supplies a controlled-language baseline. None executes arbitrary generated Python.

## Reporting

- Receipt and task/source identities gate trusted results. Pending or corrupt artifacts are not completed evidence.
- Report planned, started, terminal and valid separately; distinguish pre-request blocking from actual HTTP attempts.
- Capability support comes from public semantics, not successful solves or scheduling.
- Primary method coverage uses the lowest predeclared seed. Any-seed coverage is labelled separately; repeated-seed paired quality uses all predeclared valid repetitions, without choosing the last or best answer.
- Group objectives by type, unit and scale. Missing or zero references have null relative gaps. BKS comparisons disclose in-pool reference bias.
- EXACT requires trusted optimal termination and agreement between solver objective, bound and checker. Failure is not an infeasibility proof; a feasible witness is not optimality evidence.
- Keep first answers and checker-assisted revisions separate. Historical replays are not new model calls or Pass@1 measurements.

## Future snapshots

Static uses the earliest available same-day observation; Reactive uses the latest available at the decision; Oracle sees the target future matrix. Routes are scored on that common fixed future snapshot. Frame hashes, actual availability, node worlds, public scenario provenance and execution bindings are audited. No within-route time-varying routing is implied. A heuristic Oracle is not a mathematical lower bound, and negative differences remain visible.

Formal model identity, serving settings, tools, usage and budgets still need verification. Interim figures and engineering tests do not establish a formal leaderboard or statistical ranking.
