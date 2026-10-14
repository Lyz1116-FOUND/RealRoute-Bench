# Evaluation protocol and evidence

## Task identity

`BaseInstance + Scenario` determines the problem. The Scenario includes objectives, visit policy, fleet, depots, route endings, enabled atoms and exact numeric parameters. Complete semantics are in [Problem Spec v1](PROBLEM_SPEC_V1.md); its opening implementation-status wording belongs to the original definition-stage document. Current implementation status is in [STATUS](STATUS.md).

The normalizer validates schema and dependencies. The checker does not import solver code and recomputes route timing, stepwise load, required visits, relational constraints, resources and objective. A private constructive witness is never passed to evaluated models.

## Traditional references

Directed MILP adapters cover 14 atoms, structural axes and four objectives. The LNS is heuristic and may limit feasible-group insertion/search; construction failure does not establish infeasibility.

The completed pilot uses 17 Shanghai parent-N20 tasks (PDP physical N19), 5 seconds per MILP/LNS condition, one seed, four backends. It supplies 9 EXACT and 8 BKS references. A route produced by LNS can match a certified optimum, but certification comes from a separate trusted MILP bound/termination record.

EXACT requires trusted solver optimal termination, accepted checker solution, and reconstructed objective, solver objective and bound agreement within relative tolerance 1e-6. BKS indicates a feasible best-known route, not an optimum. Zero reference objectives have undefined relative gaps; gap direction respects minimization/maximization. Model claims/metadata cannot certify optimality.

The proposed formal reference time limits are 60 seconds for parent N20 and 300 seconds for parent N50. Full execution remains pending. A configured full Gurobi license is expired; explicit restricted-license runs can fail size limits. HiGHS is reported as its own backend. No silent fallback is labelled a Gurobi result.

## LLM tracks

Direct receives the full public matrix and exact natural-language constraints and emits route JSON without tools. Model emits a declarative Scenario, which is normalized and compared against every numeric/semantic task parameter before a fixed solver runs. Arbitrary generated Python execution is not currently supported.

Separate tracks and cohorts. Record prompt hash, renderer version, requested/actual model, thinking settings, complete answer, tokens, inference wall time and external solver wall time. First-attempt parsing/semantic/route failures and transport errors are distinct. Explicit recovery trials do not overwrite first attempts or inflate Pass@1. Unknown interrupted token usage retains budget reservations.

Formal model versions, multi-instance coverage, repeats, timeout/retry policy and aggregate reporting need to be frozen. Current trial cohorts cover ATSP and ACVRPTW only and cannot establish a model ranking. Service names shared by providers do not prove identical weights or serving settings.

## Future-snapshot task

At decision cutoff, the solver commits a route. Every mode is scored on the same fixed designated future matrix, with public operational scenario parameters derived from static data. Static uses the same day's earliest fully available frame; Reactive the latest fully available observation; Oracle the actual future target frame. All methods must share scenario, node identity, solver and algorithmic budget.

Nominal one-hour pairs: 07→08, 08→09, 16:30→17:30, 17:30→18:30. API acquisition/receipt times define availability, not just nominal slot labels. Missing pairs are excluded for every mode with explicit diagnostics. Historical diagnostic pairs are separate from the formal fresh series. No within-route weight switching and no completed predictive/JEPA experiments are claimed.

## Formal evaluation preparation still required

1. Freeze model/track/task/repetition/resource protocols before full test execution.
2. Run all static references with objective, bound, status, backend and independent checker records.
3. Freeze composition holdouts, auditing induced pickup/delivery semantics and all prompt/retrieval exposure.
4. Audit dynamic completeness, acquisition windows, node hashes and receipt-time cutoffs.
5. Freeze dynamic date blocks and purge history/future-horizon exposure at boundaries.
6. Run controlled full traditional/LLM/temporal experiments and report per-city/constraint/date outcomes and uncertainty.

ODs in one frame are spatial samples, not independent time samples. Statistical resampling should reflect city/date/instance grouping. Baidu context is optional auxiliary data; missing context does not automatically invalidate a complete AMap matrix. Formal leaderboard submission/ranking is not implemented.
