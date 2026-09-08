> Current v1.0 implementation and evidence: [delivery contract](docs/v1/CONTRACT.md), [AC model admission](docs/v1/MODEL.md), [research packages](research/README.md). The historical architecture below is preserved; aspirational domains are not current implementation claims.

# Sources, candidate tools, and data policy

Reviewed on 2026-09-07 for the architecture foundation. These primary or official sources support the bounded statements below. They do not approve a dependency, settle every nested asset's rights, prove model applicability, establish a benchmark tolerance, or show an implemented integration.

## Source authority

Use sources in this order for a specific claim:

1. exact dataset/model release, its terms, and its accompanying technical definition;
2. applicable standard or primary paper for the modeled quantity and method;
3. official engine specification/documentation for stated behavior;
4. repository tests and retained benchmark evidence for our exact adapter/model;
5. qualified engineering interpretation for the intended use.

Marketing copy, an agent explanation, a package name, and a successful install are not scientific evidence. Where an official standard is paywalled, record the exact edition and access boundary; do not reconstruct its requirements from secondary summaries.

## Architecture and numerical interoperability

| Source | Bounded use in this plan | Unresolved before adoption |
| --- | --- | --- |
| [NIST SP 811, SI derived units](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes) and [time guidance](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-8) | Supports explicit quantity dimensions and the distinction that power is energy per time; supports seconds as the computational time unit while allowing declared display units. | Exact serialization, decimal/float behavior, and unit-library choice. |
| [FMI 3.0.2 specification](https://fmi-standard.org/docs/3.0.2/) | Primary interoperability reference for model exchange, co-simulation, scheduled execution, communication steps, clocks, events, early return, and explicit solver status. | Whether FMI is needed, adapter conformance, compatible implementations, licensing, performance, checkpoint behavior, and failure recovery. |
| [HELICS official documentation](https://docs.helics.org/) | Candidate reference for time-coordinated multi-domain energy co-simulation. | No requirement yet; dependency/runtime/telemetry review and a measured need are prerequisites. |
| [ASME V&V 20-2009 (R2021)](https://www.asme.org/codes-standards/find-codes-standards/standard-for-verification-and-validation-in-computational-fluid-dynamics-and-heat-transfer/2009) and [ASME VVUQ overview](https://www.asme.org/codes-standards/publications-information/verification-validation-uncertainty) | Supports separating code/numerical verification, validation against data for a stated variable/use point, and uncertainty. It also warns that transfer away from validation points requires engineering judgment. | Standards access, method tailoring to electrical/thermal domains, and qualified reviewer interpretation. |

FMI and HELICS influence the contract vocabulary only. The foundation adds neither dependency and does not claim conformance.

## Distribution-network benchmark candidates

| Source | What it can support | Rights/model decision state |
| --- | --- | --- |
| [IEEE PES Distribution Test Feeders](https://cmte.ieee.org/pes-testfeeders/) and the committee's [radial feeder data document](https://cmte.ieee.org/pes-testfeeders/wp-content/uploads/sites/167/2017/08/testfeeders.pdf) | Authoritative technical candidate for small distribution-feeder topology, equipment data, and published reference results, including the IEEE 13-node feeder. | `REVIEW_REQUIRED`: exact asset/release, terms, redistribution, corrections, phase conventions, and machine-readable source identity must be established. Public download is not a redistribution license. |
| [SimBench dataset downloads](https://simbench.de/en/download/datasets/) and [SimBench 1.0 documentation](https://simbench.de/wp-content/uploads/2020/01/simbench_documentation_en_1.0.0.pdf) | Candidate networks plus load, renewable, power-plant, and storage profiles. The documentation states the database is under ODbL and individual contents under the Database Contents License. | `REVIEW_REQUIRED`: choose one exact small code/release and determine attribution, share-alike, produced-work, database-modification, and AGPL repository/bundle obligations with qualified rights review. Validate reference outputs and profile semantics independently. |
| [EPRI OpenDSS official documentation](https://opendss.epri.com/IntroductiontoOpenDSS.html), [test cases](https://opendss.epri.com/ExamplesDocsandTestCases.html), and [license](https://opendss.epri.com/Licencing.html) | Official distribution-system solver and test-case candidate; license page presents BSD-style software terms. | `REVIEW_REQUIRED`: distinguish engine code from each IEEE/EPRI test asset, select an exact release/interface, verify macOS/runtime support, native dependencies, model corrections, and output conventions. The `tshort/OpenDSS` GitHub mirror identifies itself as unofficial and is not an adoption authority. |
| [NREL/DOE RTS-GMLC](https://github.com/GridMod/RTS-GMLC) | Later transmission, production-cost, and reliability replication candidate with CSV source data and a repository-specific data-use agreement. | Not suitable as the first small distribution feeder. Exact release, notice/credit/indemnity terms, sub-assets, conversion outputs, and model applicability need review. |

GH-001 starts with the IEEE and SimBench candidates and may choose neither. If no candidate has adequate rights, reference outputs, and tractable topology, the safe fallback is an original, clearly synthetic contract fixture that makes no public-feeder validation claim.

## Candidate numerical engines

| Source | Stated capability relevant here | Current decision |
| --- | --- | --- |
| [pandapower official documentation](https://pandapower.readthedocs.io/en/stable/), including [transformers](https://pandapower.readthedocs.io/en/stable/elements/trafo.html) and [time-series execution](https://pandapower.readthedocs.io/en/stable/timeseries/run_function.html), plus its [BSD-3-Clause license](https://github.com/e2nIEE/pandapower/blob/develop/LICENSE) | Candidate Python network model with power-flow, transformer, controller, diagnostics, and time-series surfaces. Documentation exposes engine-specific units and sign conventions that an adapter must translate explicitly. | Candidate only. GH-002 must pin an exact release, verify transitive solvers/runtime, safe loading, advisories, platform/hardware behavior, diagnostics, numerical reference agreement, and rollback. |
| [PyPSA official documentation](https://docs.pypsa.org/latest/), including [storage units](https://docs.pypsa.org/latest/user-guide/components/storage-units/) and [storage constraints](https://docs.pypsa.org/latest/api/networks/constraints/), plus its [MIT license](https://github.com/PyPSA/PyPSA/blob/master/LICENSE) | Later candidate for dispatch/capacity studies. Official equations distinguish power capacity from energy state and include standing/charging/discharging losses and snapshot weighting. | Not required for the first feeder. Solver choice, exact version, optimization backend/license, representative-period semantics, platform support, and validation remain open. |

Software licenses above apply to the named repositories, not automatically to bundled example networks, reference outputs, optimization backends, or transitive packages. No engine is installed or approved by this documentation.

## Transformer and component physics

| Source | Bounded use | Limit |
| --- | --- | --- |
| [IEEE C57.91-2025](https://standards.ieee.org/ieee/C57.91/7163/) | Current official guide candidate for mineral-oil-immersed transformer loading, temperature calculations, ambient/cooling effects, and loss-of-life context. | Purchase/access and exact applicability remain unresolved. It does not validate a Grid Horizons implementation or apply to every insulation/cooling/design class. |
| [ASME VVUQ 60.1-2025 listing](https://www.asme.org/codes-standards/about-standards/technology-highlights/digital-engineering) | Official evidence that computational-physics software selection itself warrants structured credibility review. | The guideline is not yet adopted as a project requirement; access and relevance must be reviewed in GH-014. |

The first transformer model must be a documented reduced-order electrical-loss/thermal model. A finite-element or multiphysics engine is intentionally unnamed: GH-014 must first specify the question, material/boundary data, mesh/timestep convergence evidence, comparison reference, licensing, hardware, and reviewer availability. Engine popularity cannot fill those gaps.

## Storage, planning, reliability, and lifecycle

| Source | Bounded use | Limit |
| --- | --- | --- |
| [DOE 2022 Grid Energy Storage Technology Cost and Performance Assessment](https://www.energy.gov/cmei/2022-grid-energy-storage-technology-cost-and-performance-assessment) | Candidate assumptions and terminology for storage cost, duration, cycle/calendar life, replacement, recycling, and decommissioning. | Values are source-vintage, technology-, duration-, geography-, and methodology-specific; no value is imported until exact tables, units, year, uncertainty, and rights are recorded. |
| [EIA Form 861 reliability definitions](https://www.eia.gov/electricity/annual/html/epa_11_02.html) | Official definitions and reporting context for SAIDI, SAIFI, CAIDI, major-event treatment, and coverage. | Aggregate historical utility metrics are not a feeder model, outage process, or validation target without a defensible mapping. Reliability scenarios must report their own event/restoration assumptions. |
| [NREL Life Cycle Assessment Harmonization](https://www.nrel.gov/docs/fy13osti/57187.pdf) | Supports cradle-to-grave boundaries and shows that technology/system boundary, capacity factor, efficiency, lifetime, resource, and methodology choices drive comparability and uncertainty. | Harmonized literature values are not a substitute for a declared functional unit, current inventory, geography, allocation method, or uncertainty for a specific design. |
| [NREL Annual Technology Baseline](https://atb.nrel.gov/) | Candidate source for versioned, transparent generation/storage cost and performance assumptions in later capacity studies. | Exact edition/scenario, currency year, regionalization, technology maturity, attribution, and applicability must be fixed per study. |
| [Copernicus Climate Data Store](https://climate.copernicus.eu/climate-data-store) | Candidate weather/reanalysis source for later resource and stress scenarios. | Each product has its own terms, variables, resolution, uncertainty and transformation needs. No product is approved or downloaded. |

## Source and data record policy

Every external artifact gets a `SourceRecord` before use. At minimum record:

- exact publisher, canonical URL, release/version/date, retrieval date, and immutable artifact identity;
- author/licensor, terms URL, required notice/attribution, access constraints, modification and redistribution decision;
- original units, sign conventions, coverage, reference basis, missingness, corrections, uncertainty, and known limitations;
- every transformation, its parent artifact, tool/version, parameters, output unit/schema, and reversible or lossy nature;
- rights state: `CLEARED_REFERENCE`, `CLEARED_REDISTRIBUTION`, `REVIEW_REQUIRED`, or `REJECTED`.

Only `CLEARED_REDISTRIBUTION` artifacts may be bundled. `CLEARED_REFERENCE` artifacts may be cited and fetched by an authorized user under their own access, but the project must not mirror them. `REVIEW_REQUIRED` blocks runs and publication using the artifact. `REJECTED` remains recorded so later contributors do not repeat the same unsafe path.

Public availability, an API response, and a GitHub repository do not imply unrestricted reuse. Keep credentials, controlled infrastructure information, customer/utility data, personal records, CEII, NDA material, and undisclosed third-party assets out of the repository and run bundles. Synthetic data must be generated from documented rules and labeled synthetic; it must not be a lightly transformed private source.

## Dependency adoption record

Before installing or committing a production dependency, GH-002 or a later approved decision records:

- exact official package/source, release, source identity, license and transitive/runtime dependencies;
- maintenance signal, advisories, release/update policy, safe loading behavior, network/telemetry and native code;
- exercised OS, architecture and hardware support in the allocated environment;
- numerical conformance cases, diagnostic coverage, deterministic/stochastic controls and known limitations;
- data/model format rights, alternative approach, removal/rollback and artifact migration.

The present architecture records candidates only. Exact engine/model rights, versions, supported hardware, numerical tolerances, data redistribution, and qualified engineering review are unresolved.
