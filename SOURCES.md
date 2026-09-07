# Sources, candidate tools and data policy

Official entry points inspected while preparing this plan on 2026-09-07. These links support the bounded descriptions below; they do not prove an implemented integration, available benchmark data, endorsement or scientific validity for every planned scenario.

| Source | Supported planning use |
| --- | --- |
| [pandapower documentation](https://pandapower.readthedocs.io/en/latest/) | Official network-analysis documentation, examples and transformer components; candidate for the first adapter. |
| [PyPSA](https://pypsa.org/) | Official power-system optimization framework and ecosystem; candidate for planning, generation and storage scenarios. |
| [Copernicus Climate Data Store](https://climate.copernicus.eu/climate-data-store) | Candidate public climate and weather inputs; exact product terms and downscaling validity must be checked before ingestion. |

## Before adopting a dependency or dataset

Record the exact official release and license, maintenance/advisory state, runtime and transitive dependencies, safe loading behavior, telemetry/network use, storage/compute cost, alternatives and rollback. A source being listed here does not authorize installation or data download. Exact versions are deliberately deferred until the implementation environment and compatibility evidence exist.

For each dataset/model, document provenance, permitted use, attribution, redistribution rights, access requirements, geography/population/time coverage, uncertainty and missing variables. Link source records to all derived artifacts. Reject incompatible terms and use an honestly labeled synthetic fixture when appropriate. Keep private information, credentials, controlled-access data and third-party assets out of this public repository.

## Evidence limits

Evaluate pandapower for the initial distribution benchmark and PyPSA for later system planning. Begin transformer thermal modeling with a documented reduced-order model. Compare any future finite-element tool with that baseline before adoption; no engine is installed by this planning repository.

Official tool documentation establishes the tool's stated purpose; our model cards and independent benchmarks must establish applicability to our experiment. Sources are not blanket proof for results we have not measured. The project's original documents use AGPL-3.0-only; referenced material retains its own terms.
