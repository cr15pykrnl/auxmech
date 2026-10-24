# Deformvis audit

Primary-agent review, 2026-10-24. Scope: publication and artifact identity,
recovered code/notebooks, source hashes, data lineage, HF consumer workflow,
graphical abstract and source-publication readiness. This is not an independent
scientific review or a reproduced experiment. Recovered originals were preserved.

## Findings

| Severity | Location | Evidence and effect |
| --- | --- | --- |
| High | `related-work/km4-neural-network-extension/src/km4.py:315` and `:359` | Sampling with replacement precedes the random row split. Reconstructing the helper's 80:20 seed-42 split on recovered `balanced-images.pkl` gives 574 shared source-frame keys and 1,018 of 1,200 validation rows whose source key occurs in training. This cannot serve as evidence of independent generalisation. |
| High | HF `raw/fd-data/Deg_22.5.csv` versus `processed/images.parquet`, angle 22.5 | The staged raw table does not reproduce the recovered numeric metadata under the supplied formulas. Of 488 records, 484 stress values and 487 strain values differ exactly. Maximum absolute differences are about 0.05217647 and 0.01155979, in unresolved recovered units. Preserve both as distinct recovered artifacts; resolve the source/version before physical analysis. |
| High | Source hosting and recovered notebooks | At the original audit, no local Git repository existed and public `cr15pykrnl/deformvis` returned 404. Source release preparation initialized local Git and excluded the original training materials. See the release record for subsequent source revisions and hosting verification. A remote clone is not verified. Notebook `import km4` and `data/processed/*.pkl` paths also require the original environment/layout. The supported new workflow is portable data inspection, not executing those notebooks or reproducing training. |
| Medium | `related-work/km4-neural-network-extension/src/km4.py:242` | PCA component selection omits the full cumulative sum. If exceeding the threshold requires every component, `n_components` stays zero. For `[0.5, 0.5]` at 0.95, neither loop iteration selects a positive count. The control-flow edge case was reproduced from the recovered function with controlled PCA outputs. Actual recovered PCA state is missing, so this is an edge-case defect, not a demonstrated cause of the historical result. |
| Medium | Raw input inventory and checkpoint | Nine videos, three force/displacement tables, features/PCA state and checkpoint are missing. There is no complete staged raw video/table pair. KNet1 implementation identity remains unresolved. |
| Medium | Annotations and physical units | Cluster-to-mode labels come from the recovered notebook, not independently verified expert ground truth. Force, displacement and stress units remain unresolved. The expert workbook's experiment identity is unmatched. |

The reconstructed split uses the recorded helper's `test_size=0.2`,
`random_state=42` and ShuffleSplit permutation semantics on the recovered 6,000-row
balanced table. It is not a recovery of the saved runtime dataloaders or the exact
historical evaluation run. The balanced table has 1,724 unique source-frame keys;
all exist in the 2,482-sample source collection. Original code was not rewritten to
manufacture a new historical result. A future training implementation must split
verified source sequences/duplicate lineage before resampling.

For six of seven available raw tables (7.5, 10, 15, 17.5, 20 and 25 degrees),
`f / 3557.6` and `dy / 91` with the recovered per-angle strain offset reproduce
the derived metadata exactly at every available source frame. This supports that
specific arithmetic relationship; it does not independently establish units or
validate the mismatching 22.5-degree version.

## Checks completed

- All 130 original manifest-listed files still match their recorded hashes.
  Fourteen lack an independently recorded expected source hash; no false mismatch
  was inferred from those empty fields.
- Published KNet1 identity, authors, DOI, method, eight clusters and four reported
  modes checked against accepted manuscript and submission sources. The paper's
  88.77% validation and 88.08% test results were distinguished; neither is claimed
  as reproduced or applied to the KNet2 dataset.
- All 20 pinned HF files downloaded afresh and verified against source-controlled
  byte counts and SHA-256 values, including the checksum manifest itself.
- Fresh source-only copy, with no recovery archive or original pickles, successfully
  verified and inspected all 2,482 images using Python 3.12, PyArrow 19.0.1 and
  Pillow 11.3.0. All image shapes, grayscale modes, pixel hashes, unique IDs,
  numeric finiteness, 24 cluster IDs and 213 repeated pixel hashes checked.
- Deliberately corrupted download rejected. Traversal path in the release
  specification rejected. Fixtures restored after the negative checks.
- HF viewer now reports both `recovered` splits without pending or failed entries;
  first-rows API returns 100 records with the expected schema. This checks the
  viewer service response, not browser screenshot fidelity or the HF datasets
  Python client's full loading path.
- Graphical abstract: native vector geometry, 220 by 110 mm, uniform 9 pt
  Helvetica-compatible labels, grayscale PDF/PNG, font and page-bound checks.
  Source interpretation and representative symbols reviewed separately.

## Supported workflow and unresolved release work

The README documents a GitHub clone, pinned public HTTPS download, verification
and a concrete Parquet/Pillow inspection command. Its download/load portion was
exercised from a clean source copy during the original audit. Subsequent source
publication and source-download checks are recorded in the release record. The original
audit itself did not create a repository, commit or push.

The original HF data revision remains pinned in `hf-dataset.json`. The updated
exporter and the published card amendment now include the quantified scientific
caveats above. The new card revision and matching checksum-manifest update are
recorded in [the release record](hugging-face-plan.md). All data artifacts and the
original pinned release remain unchanged.

The exporter is a maintainer recovery tool requiring private provenance and
trusted original artifacts. It is not needed to use the released data. The
consumer scripts do not deserialize pickle or require tokens for public data.

Source preparation confirmed the MIT license for newly authored Python scripts
and recorded figure rights/privacy reviews in `release-manifest.json`. Publication
and reciprocal immutable GitHub/HF revision links are tracked in the release record. Root ignore rules keep originals, bulk data and private provenance out of
ordinary staging. No blanket claim that every manuscript builds, every recovered
function works or all historical results are reproducible is justified.

Machine-readable local check results are under ignored `.local/`; durable findings
and their scientific scope are recorded here. No extra contents index or task
board has been created.
