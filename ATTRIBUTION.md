# Attribution and source distinctions

- **OpenStreetMap contributors** provide the canonical spatial data. OSM data are distributed under [ODbL](https://www.openstreetmap.org/copyright). OSM-derived artifacts require appropriate attribution and applicable database obligations; this repository does not relabel them under a blanket software license.
- **OSRM** supplies modelled static routes, distances and profile-based durations. [Official project](https://github.com/Project-OSRM/osrm-backend). Static durations are model estimates, not recorded journeys.
- **AMap** supplies provider traffic-aware fresh OD durations through its official service. [Distance documentation](https://lbs.amap.com/api/webservice/guide/api/direction#distance). Fresh raw provider data are not included in this repository snapshot.
- **Baidu traffic platform** supplies city-level context/forecast data. [Official page](https://jiaotong.baidu.com/congestion/city/urbanpredict). These are not road-edge or OD ground truth and are not included as raw responses here.
- **Chengdu historical link speeds**: [publisher Figshare record](https://figshare.com/articles/dataset/Urban_link_travel_speed_dataset_from_a_megacity_road_network/7140209). Publisher license/source provenance is distinct from OSM and contemporary provider outputs; raw historical files are not included here.
- **Our scenario attributes** (demand, windows, service, prizes and fleet parameters) are generated experimental parameters on a real spatial base, not observed customer demand.

This is a public research preview with curated artifacts; raw and private evaluation data are not included. No unified data redistribution permission, accepted paper, formal citation, or permissive project-wide license is asserted. Any later public release must identify artifact-specific terms and retain source provenance.
