# Data card · 2026-10-19

This is a private research preview with curated static inputs, not a complete dynamic data release.

## Sources and semantics

- OSM places and roads supply canonical WGS84 spatial identity. A node is a public-road access point, not a certified facility entrance.
- OSRM supplies profile-derived static duration and selected-route distance. It is not an observed trip time.
- AMap supplies traffic-aware OD estimates on fixed requested endpoints; it does not expose the provider's full routing graph or actual vehicle trajectories.
- Baidu supplies city-level context, curves and forecasts for a different scope; it is not OD truth.
- Chengdu historical data remain a separate native-source auxiliary track: 45 downloaded days, 44 complete usable days; full mapping to the contemporary v3 node world is unresolved.
- Demand, windows, rewards, penalties and fleet parameters are synthetic experimental attributes.

## Fresh acquisition

China-local 2026-10-15 through 2026-10-28; 12 cities, 200 fixed nodes, 10 frames per day. The target is 1680 frames of 39800 non-diagonal OD values each. There are currently 522 complete production PASS frames and 18 quarantined slots. Diagonal zero is legitimate; missing off-diagonal entries are never zero-filled.

Three four-city groups start at nominal time, +5 minutes and +10 minutes. Each frame keeps source, request/response, acquisition and available_at evidence. Provider observation/update time may be unknown. Same-frame OD entries are correlated spatial observations, not independent time samples.

## Missingness and imputation

Quarantine and real missingness are preserved. Offline imputation is synthetic reconstruction and may use later frames or later dates. It cannot count as complete REAL acquisition, replace measured evaluation truth, or enter causal decision inputs without a separate availability protocol.

## Splits and distribution

The downloadable static bundle has 1176 distinct tasks. Original pickup–delivery cases can use physical N19/N49 despite N20/N50 parent scales; the separate composition cohort uses its own construction. Final dynamic-date splits await QA.

No credentials, provider account balances, raw API responses, private witnesses or detailed reference solutions are in this repository. Source-specific rights and attribution remain distinct; see [ATTRIBUTION.md](../ATTRIBUTION.md). This card does not grant new redistribution permissions.
