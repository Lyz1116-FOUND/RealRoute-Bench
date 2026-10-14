# RealRoute-Bench data card · research preview

Snapshot: 2026-10-15. This is a private artifact snapshot, not a completed fresh-dynamic release.

## Spatial identity

Canonical coordinates are WGS84. AMap's request adapter converts to GCJ-02 without replacing canonical coordinates. Frozen node IDs, matrix order, coordinates, quotas and source hashes bind static and future dynamic layers. Each point is an OSM-place-associated public-road access point, not a certified building entrance.

Per city: Master-200 and nested 20/50/100/200; matrix shape `[N, N]`, row origin and column destination. Duration is seconds; distance is metres. Static distance corresponds to the router's selected fastest route. Invalid/missing OD entries are represented by masks and contract status, never silently zero-filled. Diagonal zero is distinct from a missing off-diagonal observation.

Demand and scenario operational parameters are synthetic. Directed matrices do not imply that every individual OD pair is asymmetric.

## Fresh sequence

Target: China-local 2026-10-15 through 2026-10-28, 10 daily slots, 12 cities, 200 nodes. The three launch groups are Beijing/Shanghai/Xi'an/Chongqing (+0 minutes), Chengdu/Hangzhou/Wuhan/Xiamen (+5), Sanya/Yiwu/Dunhuang/Anji (+10).

Record `scheduled_time`, `frame_start_time`, `frame_end_time`, per-OD request and response timestamps, `available_at`, timezone, valid/observed masks, provider, canonical CRS, node version and manifest hash. Frames are acquisition intervals, not instantaneous traffic observations. ≤5 minutes is a target to evaluate in final QA, not an achieved guarantee.

AMap durations are provider traffic-aware OD estimates. Its returned distance is auxiliary and is not substituted for canonical OSM static distance. AMap's hidden route can differ from the OSM route; their ratio is a provider/profile diagnostic, not a pure isolated congestion factor.

Missed data remain missing. No later-day observations or predictions are relabelled as the scheduled frame. Final retained-frame counts and calendar continuity require completed QA.

## Chengdu historical auxiliary

Original period: 2015-06-01 through 2015-07-15; 45 calendar days. Native topology: 1,902 nodes and 5,943 directed links. Published resolution: 2 minutes in five windows: 03–05, 08–10, 12–14, 17–19, 21–23. The native normalized array has shape `[45, 300, 5943]` with state validity; native missing-data/interpolation provenance is not an observed-edge mask supplied by the publisher.

All publisher files were downloaded and verified locally. Conflicting June 3 windows are quarantined, leaving 44 complete usable days. The uniform 10-slot grid has seven supported clock slots; 07:00, 16:30 and 23:30 fall outside published windows. Unsupported slots remain missing; no interpolation across those gaps creates observations.

The native graph lacks original OSM edge IDs/full geometry and has unresolved coordinate-system evidence. A coarse numeric screen found only 81/200 v3 points inside the native hull; this is a feasibility diagnostic, not a validated map match. Native N200 diagnostic matrices do not use the same v3 endpoints. Original reconstruction uses future temporal information, so strict causal prediction eligibility is false. This auxiliary dataset is not a replacement for the contemporary 12-city sequence.

## Other source candidates

T-Drive preprocessing/map matching is not completed. Audited DiDi candidates lack sufficient verified spatial/time/unit metadata for canonical ingestion. They remain candidates, not completed dynamic sources.

## Baidu city context

Nine matching cities are covered. Yiwu, Dunhuang and Anji remain missing rather than inheriting nearby-city values. Provider statistical scope is not verified equal to our study region. Preserve source update time, request/receipt times, forecast target time/version, spatial scope, response hash and linked AMap slot.

Current metrics are sampled near the planned AMap acquisition, published curves deduplicated each slot, predictions saved twice daily, and recent summaries daily. These are separate lower-frequency tasks. Publish-time/receipt-time cutoffs prevent future leakage. City averages, congestion indices and migration/tourism labels cannot generate genuine OD traffic matrices by scaling static costs.

## Static partition

Train: Shanghai, Xi'an, Hangzhou, Wuhan, Xiamen study region, Yiwu (588).
Validation: Chengdu, Anji (196).
Test: Beijing, Chongqing, Sanya, Dunhuang (392).
All derived scales/scenarios of one city stay in its partition. The input-only snapshot includes test inputs for inspection; they must not be used for prompt tuning, retrieval or training in claimed held-out experiments. Composition/date holdouts are separate and pending.

## Integrity and interpretation

Download checksums are in `downloads/SHA256.json`. The ZIP contains only instance inputs and assignments. This repository does not include road PBFs/runtime tiles, full raw traffic, private witness routes, or collector accounts. Spatial source completeness and an implemented collection chain do not imply final fresh-data completeness or formal solver evaluation.
