# Repository contents and storage boundaries

This public repository currently contains a **curated project-page snapshot**. Updating progress here does not back up the executable workspace.

| Location | What belongs there |
| --- | --- |
| This curated repository | Bilingual overview, dated aggregate progress, schemas/catalog, frozen specification, source attribution, small figures, approved input-only samples, checksums and research limitations |
| A private research-code repository or separately reviewed code snapshot | Source, tests, solver adapters, sanitized configuration templates, dependency locks, versioned task/protocol manifests, reproduction commands and small public fixtures |
| Versioned storage / backup | Large OSM/OSRM assets, raw traffic archives, complete processed matrices, run artifacts and data inventories; access and distribution policy per source |
| Local secret store | API keys, authorization material, passwords, license files and operational credentials; never Git, including private Git |

Private reference answers, certificates and construction witnesses require a privileged evaluation boundary. They must never enter model prompts, few-shot examples or retrieval. Keeping Git private does not remove this separation.

Do not upload virtual environments, caches, national PBF files or continuously changing SQLite ledgers into the README repository. Do not assume that a private repository makes a deployed website private. Keep any future public site a separate, explicitly reviewed export.

Suggested research-code layout when that scope is explicitly adopted:

```text
src/  extensions/  scripts/  tests/
schemas/  catalog/  config/       # sanitized templates and scientific configuration
docs/  manifests/               # protocols, data versions and hashes
pyproject.toml  requirements.lock
```

This update preserves the curated repository scope and does not change repository visibility. It does not silently turn the curated page into a full source backup or publish a site.
