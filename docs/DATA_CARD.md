# Data card · 2026-10-24

Snapshot: 2026-10-24T01:47:26.493593+09:00 (Japan time). Public research preview; final dynamic release and date assignments remain incomplete.

## Sources

OSM places/roads provide real spatial sources and public-road access points, not certified building entrances. OSRM yields profile-derived static duration and corresponding-route distance. AMap yields traffic-aware OD estimates, not observed vehicle trips. Demands, windows, service times, fleets, prizes and penalties are synthetic experimental attributes. Baidu city context is not OD truth. Chengdu 2015 data remain a separate native historical track: 91 source files, 45 calendar days, 44 usable source days, 308 auxiliary matrices; no verified identity mapping to the 2026 node world.

## Acquisition and counts

The active plan covers China-local 2026-10-15 through 2026-10-28: 12 cities × 14 days × 10 slots = 1,680 target slots. There are 1,080 current ledger records: **1,005 nominal provider frames, 17 late-recovery provider frames, 58 reconstructed references, 0 unverified**. All current ledger rows can be PASS while retaining these different source classes. Local raw attempts separately total 1,119, with 81 quarantined; they include commissioning, duplicate/unused attempts, and failures. A slot count is not an attempt count or an independent-sample count.

Classification uses source path, provider manifest status, nominal identity and actual request start relative to the city's scheduled start, with 330 s lateness tolerance. Cleared reason flags never establish provenance. Absolute paths are normalized only under the explicit workspace root; out-of-root or missing evidence is unverified. See the machine-readable category definitions and city/day table.

Each N200 frame has 39,800 non-diagonal directed OD pairs. Cities start in +0/+5/+10-minute groups; each matrix is collected over a bounded window of at most 300 s. Diagonal zero is structural. Missing off-diagonal values are not zero-filled in raw frames. Timing and same-frame spatial dependence must be retained.

## Reconstruction and availability

The 864-slot active reconstruction index includes 54 matrices with estimated values. Its coverage differs from the 1,080-slot ledger and 58 derived references. The extension preserves 1,080,584 observed cells and estimates 1,068,616 unknown cells within the reconstructed matrices. These are not new acquired observations.

Legacy reconstructions can use later observations and are offline estimates. The newer spatial/temporal reconstruction version preserves observed cells and discloses its historical donors, but its development was a retrospective study, not proof of end-to-end online availability. Real missing cells have no measured ground truth. Report observed-only and reconstructed sensitivity conditions separately; late-recovery queries do not become original-slot truth.

## Scope and exclusions

The input download has 1,176 static tasks with synthetic business attributes and physical N19/N20/N49/N50. The independent composition set has 1,512 tasks on shared city worlds. Nested scales and derived scenarios are correlated. No raw provider responses, private answer routes, credentials or account details are exported. [Source attribution](../ATTRIBUTION.md) remains artifact-specific; this card grants no new redistribution permission.
