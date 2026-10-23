<p align="center"><img src="assets/hero.svg" alt="RealRoute-Bench" width="100%"></p>

# RealRoute-Bench

**Routing evaluation across real city road worlds, scales, constraint interactions, and traffic information.**

[中文](README.zh-CN.md) · [Status](docs/STATUS.md) · [Full report (Chinese)](docs/GROUP_SUMMARY_20261024.md) · [Data card](docs/DATA_CARD.md) · [Method coverage](docs/METHOD_COVERAGE.md)

**Research preview. Captured at 2026-10-24T01:47:26.493593+09:00 (Japan time).** This public repository contains curated inputs, documentation, and aggregate evidence. It is not an executable workspace backup or a completed leaderboard.

## Foundation and provenance

12 city worlds, 2,400 fixed public-road access points, nested N20/50/100/200 subsets, and 48 static duration/distance pairs. Static tasks: 1,176 (588/196/392 city split); separate composition tasks: 1,512 (1224/72/216), sharing city worlds across interaction partitions. Existing task parent scales are N20/N50; original pickup-delivery physical sizes can be N19/N49.

OSM provides spatial sources; OSRM computes profile-derived static estimates; AMap provides traffic-aware OD estimates. These are not measured vehicle journeys. Operational attributes are synthetic. Reconstructed values remain estimates and are not relabelled as acquired observations.

## Dated progress

| Component | Verified record |
|---|---|
| Recorded production slots | 1,080/1,680 (64.3%); ledger coverage only |
| Nominal-window provider frames | 1,005 |
| Late-recovery provider frames | 17; genuine queries with separately disclosed timing |
| Derived/reconstructed references | 58; excluded from nominal acquisition counts |
| All local frame attempts | 1,119, including 81 quarantined attempts; includes commissioning and unused attempts |
| Historical static candidate jobs | 5,880/5,880 results with matching receipts; mixed-pool quality summary withheld |
| New composition candidate batch | 312/2,086 jobs; job completion is not public-reference eligibility |
| Spark development pilot | 64 requests; first attempts 9/48 valid, added repetitions 5/16 valid; no model ranking |
| Engineering | Latest archived full suite: 541 tests, 0 failures, 2 skipped. This update: 8 focused provenance tests; full suite not rerun |

[Aggregate evidence](evidence/PROGRESS_SNAPSHOT.json) · [Acquisition categories](downloads/COLLECTION_PROGRESS.json) · [City/day counts](downloads/COLLECTION_COVERAGE.csv)

The active acquisition plan is 15–28 October 2026, China local time, 10 nominal slots per city per day. City groups start at +0/+5/+10 minutes. A frame is a bounded acquisition window, not an instantaneous observation. The ledger PASS flag alone is not provenance evidence.

## Methods and acceptance

`BaseInstance + Scenario → solver/model → Solution → independent checker`

Exact solvers, constructive/local search, metaheuristics, neural construction/improvement, LLMs, and hybrid systems all require versioned admission, semantic support, and resource budgets. Full method coverage and formal neural baselines remain incomplete. Unsupported semantics are rejected, not silently weakened.

Direct outputs routes. Model outputs a declarative Scenario, checked before fixed HiGHS execution. Scores and resource conditions are separate. No universal natural-language or arbitrary generated-code competence is claimed.

**The custom-heuristic withdrawal remains effective.** Its 17 pilot rows are absent. The [51 retained historical records](downloads/PILOT_RESULTS.csv) preserve original solver fields, while relative gaps and mixed-pool EXACT/BKS summaries remain withheld. [Provenance audit](docs/LNS_IMPLEMENTATION_AUDIT_20261024.md). New internal batches still include that method; only execution counts are published, not acceptance as a literature baseline.

## Resources and next work

[Static input ZIP](downloads/static_public_v1.zip) · [City split](downloads/STATIC_SPLIT.json) · [Frozen specification](docs/PROBLEM_SPEC_V1.md) · [Schemas](schemas/) · [Catalog](catalog/) · [Attribution](ATTRIBUTION.md)

Close source/timing and final-date QA, build a new admitted reference pool, and complete difficulty controls before full comparisons. Predictive/JEPA methods, product Agent evaluation, the final dynamic release, and formal leaderboards are pending.

```sh
python3 scripts/verify_downloads.py
python3 scripts/test_collection_provenance_v4.py
python3 scripts/verify_progress_v4.py
```

These are offline artifact/aggregation checks, not raw API replay or external traffic-accuracy validation. No raw provider responses, private routes/witnesses, accounts, credentials, or local absolute paths are shipped.
