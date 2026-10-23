# Evaluation and remaining work

BaseInstance plus Scenario defines a task; an independent checker recomputes feasibility and objectives. Four objectives and 14 atoms are implemented; implementation coverage is distinct from dataset and solver coverage.

The original 1,176-task city split is 588/196/392. The independent 1,512-task composition split is 1224/72/216 and shares city worlds; it does not imply joint unseen-city/interaction generalization. Final dynamic date assignments await QA.

Direct emits route JSON. Model emits declarative Scenario JSON, checked for semantic fidelity before a fixed HiGHS solve. Controlled language is not arbitrary business prose. Neither track grants arbitrary Python execution. Report first attempts and repetitions separately, retaining transport and semantic failures in their declared denominators.

The method plan includes exact solvers, construction/local search, metaheuristics, neural construction/improvement, LLMs, and hybrids. Each condition needs version/weight/implementation identity, semantic capability, training exposure, hardware, total search opportunity and budget. Unsupported tasks remain visible; constraints and directed costs are not weakened to expand coverage. [Full method coverage plan](METHOD_COVERAGE.md).

The unverified custom LNS-style implementation is withdrawn from public results. Historical mixed-pool EXACT/BKS counts and dependent gaps remain withheld, despite completed internal jobs. No replacement reference pool has yet been published. EXACT requires trusted optimal termination and checker/solver/bound agreement; BKS is not an optimality guarantee; no incumbent is not an infeasibility proof. Relative gap is null for missing/zero references and separated by objective/direction. [Audit](LNS_IMPLEMENTATION_AUDIT_20261024.md).

Static, Reactive, and Oracle use the same designated future snapshot for scoring. Ordinary inputs must have been received before decision time; only Oracle has declared future privilege. This is not within-route traffic switching. Pure observations, late recovery, and reconstruction are separate conditions. A heuristic Oracle is not a certified bound. Formal production future-snapshot experiments and a model leaderboard remain pending.

Cluster comparisons by city/static parent or city/date, summarize repeats within task, and disclose limited cluster counts and in-pool reference bias. Do not treat all OD cells, nested sizes, derived scenarios or seeds as independent samples.
