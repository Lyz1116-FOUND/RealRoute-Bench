# Current-stage status · 2026-10-15

| Component | State | Evidence / boundary |
|---|---|---|
| Problem Spec / 14 atoms / 11 templates / 6 presets | Implemented | Frozen definition and machine-readable catalog |
| Normalizer / independent checker | Implemented and tested | Engineering delivery records; no solver imports in checker |
| 12-city OSM v3 / 2,400 endpoints | Frozen | Node identities and static matrices remain immutable |
| Local road/OSRM reconstruction | Completed | Reproduces frozen duration matrices; not original server binary identity |
| Static scenarios | 1,176 unique inputs | Real spatial base; synthetic operational attributes |
| Static city-held-out split | Frozen | 588 train / 196 validation / 392 test |
| City structure metrics | Completed | Declared study-region metrics; limited raw topology semantics |
| Protected AMap + separate Baidu collection chain | Implemented locally | Runtime and quotas must be checked live; not a completed 14-day sequence |
| Historical Chengdu | Native auxiliary track | Full source downloaded, 44 usable complete days; canonical v3 mapping unresolved |
| T-Drive / DiDi canonical ingestion | Pending | No completed map-matched canonical source |
| MILP / LNS adapters | Implemented | 17-case development pilot; licensed/full-scale coverage limitations |
| LLM Direct / declarative Model | Implemented; actual pilots | Two task families, separate cohorts; not formal model ranking |
| Full 1,176-instance reference run | Pending | Gurobi full license expired; HiGHS alternative explicitly labelled |
| Unseen-composition / dynamic-date split | Pending | Static city split alone does not establish these holdouts |
| Formal LLM / temporal results | Pending | Multi-instance repeats and full fresh-data QA still needed |
| Arbitrary generated-code isolation | Not implemented | Current Model track is declarative JSON |
| Predictive/JEPA and time-dependent driving | Not completed | Separate later extensions |
| Paper / formal leaderboard / public release | Pending | Private README project page only |

The prior engineering delivery recorded 183 tests passing, 156 managed core files and 492 v3 files verified. These are dated verification results, not a claim that every future change has already passed the same checks.

This snapshot does not copy collection control state, credentials or private reference answers. It must not be used as an automatic scheduler status report.
