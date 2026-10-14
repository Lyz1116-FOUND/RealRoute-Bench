# Project-page design audit

Reviewed 2026-10-15. Primary maintainers' pages and READMEs were inspected; no popularity ranking is asserted and no design endorsement is implied.

| Reference | Observed structure | Applied to this README |
|---|---|---|
| [SWE-bench original page](https://www.swebench.com/original.html) and [repository](https://github.com/SWE-bench/SWE-bench) | Clear research question; overview diagram; task/evaluation explanation; distinct resources | One-line research question, task pipeline and accessible artifact table |
| [LiveCodeBench](https://github.com/LiveCodeBench/LiveCodeBench) | Prominent homepage/data/leaderboard/explorer navigation; multi-scenario scope and version-conscious data | Compact resource navigation, distinct research axes and dated snapshot |
| [LiveBench](https://github.com/LiveBench/LiveBench) | Table of contents, quickstart, evaluation configuration, release notes and objective checks | Offline verification command, independent checker explanation and explicit version/status |
| [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) | Concise introduction, documentation entry and reproducible development instructions | Short landing-page summary plus separate data/evaluation/status documents |

## Composition choices

1. Locally authored SVG banner with factual scale numbers and research-preview status; no acceptance or leaderboard badges.
2. Stable conceptual pipeline, original frozen maps and measured city-structure plot.
3. Clearly separate data already present from target collection totals.
4. Separate Direct and declarative Model tracks and preserve temporal information semantics.
5. Pilot results appear below the benchmark definition; they are not presented as a ranking.
6. Input-only downloads, hashes and a minimal standard-library verifier; no installation commands for code absent from this repository.
7. English landing README plus Chinese companion; deeper details use short linked documents.
8. Relative images and artifact links work inside a private GitHub repository without external tracking images or a public site.

Assets and prose are authored for RealRoute-Bench; no reference site's logo, figure or text was copied.
