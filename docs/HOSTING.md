# Website, domain and storage plan · 2026-10-19

**A domain plus managed static hosting is sufficient for the current project page. A general-purpose cloud server is optional at this stage.** This is an architecture recommendation, not a purchase or deployment.

| Need | Suggested layer |
| --- | --- |
| Stable project address | A domain you control; compare renewal cost and availability before purchase |
| README-style website and figures | Managed static hosting, with an explicitly curated site output |
| Larger versioned downloads | Object storage or a data-release service with checksums and source-specific access rules |
| Always-on collection, submission API, queue workers | A separate service/compute host when the requirement is concrete |
| Long MILP runs or later model training | Budget CPU/memory or GPU compute separately; a small web VPS is not a solver cluster |

GitHub Pages is static hosting. It is available for public repositories on Free and for private repositories on eligible paid plans. Repository privacy does not by itself make the published site private. [GitHub documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

Cloudflare Pages supports static HTML, custom domains and Git integration. Its current free-plan limits include 500 builds/month and a 25 MiB maximum single asset; larger files should use storage such as R2. This does not guarantee faster access on any particular network. [Static HTML](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) · [Limits](https://developers.cloudflare.com/pages/platform/limits/)

R2 bills storage and operations; Internet egress is currently free, with a Standard-storage free tier. It is not unlimited free storage. [Pricing](https://developers.cloudflare.com/r2/pricing/)

For this project: first choose the domain, preserve the private research repository, and review a separate site export. Keep public pages and private evidence separate. Test the intended audience's connectivity before choosing hosting based on speed claims.

An always-on host can reduce dependence on a laptop for future acquisition. The current fresh series is already underway; do not migrate its collector or change network/provider bindings mid-run without a separately validated transition. Prepare the environment and a small pilot first. Purchase, DNS changes, site publication and service migration are not part of this repository sync.
