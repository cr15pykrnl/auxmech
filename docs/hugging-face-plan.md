# Hugging Face dataset preparation and release record

## Prepared package

Target dataset: `cr15pykrnl/knet2-auxetic-deformation-partial`.
Local-only package: `hf-staging/releases/knet2-partial-v0.1.0/` (not included in a source checkout).
[Published dataset card](https://huggingface.co/datasets/cr15pykrnl/knet2-auxetic-deformation-partial/blob/c9ff57794f7b40f7eed6499b3c0b23e3b918c14c/README.md).

The owner confirmed sharing rights, accepted an explicitly incomplete KNet2
release and selected CC BY 4.0 on 2026-10-24. The dataset is now public:
[HF dataset](https://huggingface.co/datasets/cr15pykrnl/knet2-auxetic-deformation-partial).
This does not clear manuscript editions or establish a validated benchmark.

Published immutable revision:
`c9ff57794f7b40f7eed6499b3c0b23e3b918c14c`.
The shared user login was verified as `cr15pykrnl`. The permanent `hf` CLI is
installed; credentials use the shared user store, not repository-local files.
The CLI's network request was blocked in the workspace sandbox, so the upload
used the HF HTTPS API via the permitted curl route. All three LFS objects passed
server verification before the atomic 20-file commit.

## What goes to HF

- 2,482 registered grayscale images, losslessly stored as embedded PNG bytes in
  Parquet, with source angle/frame IDs, recovered numeric values and cluster IDs.
- Ten registration composites and recovered bounding boxes in a separate config.
- The notebook's cluster-to-mode proposal, explicitly unverified rather than
  expert ground truth; source hashes and schema accompany the mapping.
- One unchanged raw video, seven unchanged force/displacement tables and original
  metadata. An availability table records all 20 expected raw inputs.
- Thirty-eight recovered clustering-score rows in CSV, not rerun benchmark scores.
- Dataset card, CC BY 4.0 legal text, provenance, validation results and checksums.

The registered and labelled image collections match in every image and metadata
value; the export stores their common images once. It retains all samples,
including 213 repeated pixel hashes beyond their first occurrence. No training,
validation or test split is asserted; `recovered` is an inventory split.

The package omits pickled dataloaders, balanced training copies, the unmatched
expert-label workbook, private source-path inventories and manuscript files.
No model checkpoint is available, so no model repository is prepared.

## Scientific scope and missing inputs

KNet2 is the separate neural-network extension draft. The published IJPS paper
(DOI `10.1177/20414196241281069`) concerns KNet1 logistic regression; its implementation
and a paper-matched dataset remain unidentified. Do not substitute this dataset
for the published experiment or attribute that paper's results to KNet2.

Nine raw videos and three force/displacement tables are absent. The sole available
video lacks its paired table. Although derived images cover ten angles, no full
raw video/table pair is available for reproducing acquisition. Features/PCA state,
original pre-registration images, the semantic-label pickle and checkpoint remain
missing. Three KNet2 manuscript figures are also absent, outside this data release.

Physical units of force, displacement and stress have not been independently
resolved; recovered numeric values are preserved without conversion. Strain is
intended to be dimensionless, but the calculation's unit consistency is unverified.
Mode assignments, simulation-sequence identity and split independence are unverified.
No training, inference, accuracy reproduction or generalisation claim is made.

## Rebuild and validation

The export script verifies source hashes against private recovery records before
restricted pandas/NumPy unpickling. This is a provenance-specific workflow, not a
safe general loader for arbitrary pickle files. Originals are not modified.

Use Python 3.12, dependencies in [requirements-hf.txt](../scripts/requirements-hf.txt)
and FFmpeg. Download the CC BY 4.0 legal text from Creative Commons, then build into
an absent output directory (the script refuses to overwrite an existing release):

```sh
curl -sSL https://creativecommons.org/licenses/by/4.0/legalcode.txt \
  -o /tmp/deformvis-cc-by-4.0.txt
python3 -I scripts/prepare-hf-dataset.py \
  --output hf-staging/releases/knet2-partial-v0.1.0 \
  --license-file /tmp/deformvis-cc-by-4.0.txt
```

Verified: source hashes; restricted-loader rejection of an unexpected constructor;
registered/labelled identity; unique angle/frame keys; numeric finiteness; all PNG
and Parquet image/metadata round trips; raw CSV schemas; full video decoding;
card metadata and data-file configurations; selected-file hashes; text privacy
checks. Three video frames were visually inspected for content and identifying
annotations. HF viewer split and first-row API responses were subsequently verified during
the [repository audit](audit.md). The HF datasets Python client remains untested.

Evidence is packaged in `metadata/validation.json`, `metadata/provenance.json`,
`metadata/schema.json`, `metadata/input-availability.csv` and `checksums.sha256`.
The card uses the [official HF dataset-card format](https://huggingface.co/docs/hub/datasets-cards).

## Original dataset release record

- Release: KNet2 partial recovery v0.1.0, prepared 2026-10-24.
- Intended destination: `cr15pykrnl/knet2-auxetic-deformation-partial`, dataset.
- Rights: owner confirmation in this session; CC BY 4.0 selected explicitly.
- Source revision: unavailable for the published dataset. Local Git was initialized
  during fix preparation on 2026-10-25, without a source commit or publication.
  The original source/exporter hashes remain recorded; no GitHub revision is claimed.
- Preservation: all 130 original manifest-listed artifacts still match recorded
  SHA-256 values. Of these, 116 have matching independent expected hashes; fourteen
  staged data candidates have only recorded copy hashes.
- Archive: existing provenance references private archived copies; backup/access
  state was not independently verified. No recovered originals were deleted.
- Code destination: reviewed source, exporter, notebooks and documentation belong
  on GitHub. No GitHub repository or history publication was performed here.
- Review: primary-agent artifact inspection; not independent scientific review.
- Publication: public dataset released under `cr15pykrnl`, immutable commit
  `c9ff57794f7b40f7eed6499b3c0b23e3b918c14c`.
- Post-upload checks: all 20 remote paths, sizes and Git/LFS object hashes match
  the local package. The remote card bytes match and HF parsed CC BY 4.0 plus both
  dataset configurations. The downloaded image table matches the local SHA-256;
  a sample decoded correctly at 126 × 199 and matched its pixel hash.
- Viewer status: subsequent audit verified both split configurations and 100
  first-row service records. Fresh public downloads, all 20 file hashes and all
  image loads were also checked. The HF datasets Python client remains untested.
- New audit evidence: the reconstructed balanced row split has source-frame
  overlap; the 22.5-degree raw table does not reproduce its recovered metadata.
  See [audit.md](audit.md) for quantified findings. Raw artifacts were preserved;
  at the original audit, the pinned HF card had not been amended with these findings.
  Publication does not establish scientific validity or reproduce results.

## Source and card publication, 2026-10-25

The owner authorized applying and publishing the prepared fixes, then selected
MIT for the newly authored Python scripts under `scripts/`. The license excludes
manuscripts, recovered originals, abstracts, figures and the HF dataset. Figure
rights/privacy inspections are bound to exact hashes in `release-manifest.json`.
Private provenance, bulk data and recovered originals were excluded from Git.

- Source: [cr15pykrnl/auxmech at `107168f`](https://github.com/cr15pykrnl/auxmech/tree/107168f5387c944fb08552379919003913cf53cd).
  This is the reviewed consumer/exporter source release, not the historical data
  conversion revision. The original conversion's exporter hash is preserved.
- Amended card: [`1af898e7baaa0c2a3194c309dd86c12228921de9`](https://huggingface.co/datasets/cr15pykrnl/knet2-auxetic-deformation-partial/blob/1af898e7baaa0c2a3194c309dd86c12228921de9/README.md).
  It links to the exact source revision above and adds the quantified split
  overlap and 22.5-degree metadata mismatch. The checksum manifest was updated
  atomically with the card; no dataset artifact changed.
- Data pin: `c9ff57794f7b40f7eed6499b3c0b23e3b918c14c` remains unchanged in
  `hf-dataset.json`. The original 20-file release and its checksums remain valid.
- Accounts: GitHub and shared HF authentication verified as `cr15pykrnl`.
  HF CLI network requests failed in this host; the amendment used the HTTPS API
  with shared authentication supplied through a private in-memory pipe.
- Source verification: all 17 hosted source blob IDs matched the reviewed commit.
  The central snapshot/history audit passed, with no withheld files or findings.
  Privacy, source-size and commit hooks passed; invalid identities and messages
  were rejected by the installed hooks.
- HF verification: downloaded card and checksum-manifest bytes match the prepared
  amendment. Both remote trees contain the same 20 paths; only `README.md` and
  `checksums.sha256` changed. All 19 checksum entries in the amended manifest
  verify against the amended card and unchanged original artifacts.
- Consumer verification: downloaded GitHub source archive contains the supported
  scripts and runs without private provenance or original pickles. With a copy
  of the already-verified pinned data, it verified all 20 files and inspected all
  2,482 images, 24 clusters and 213 repeated pixel hashes. This check did not
  download the bulk dataset anew or exercise the full HF datasets Python client.
- Limits: no training, model validation or reproduction of published accuracy.
  Original data/version issues, missing inputs and unverified units remain as
  documented in [the audit](audit.md). Archive backup state remains unverified.

## AuxMech rename and portability check, 2026-10-25

The owner selected AuxMech as the repository name and chose public source plus
HF data as the supported another-machine scope. The former GitHub repository
name redirects to `cr15pykrnl/auxmech`; Git history and data revisions are retained.
`AGENTS.md` and owner setup instructions are now tracked. Original figure paths
remain stable, including the `figures/deformvis/` directory.

A fresh source archive of commit `01e7529` was downloaded from GitHub into an
isolated directory without `provenance/`, `papers/`, `manuscripts/`, `related-work/`
or `hf-staging/`. A new Python 3.12 environment installed the two pinned consumer
dependencies from cached wheels. The documented download plan then fetched all
20 files afresh from the pinned public HF revision, without authentication.
Verification and inspection passed for all 2,482 images, 24 cluster IDs and 213
repeated pixel hashes. No original pickle or private inventory was required.

This host could not resolve GitHub through the Git CLI, so remote `git clone` was
not exercised successfully here. The source archive tests the exact published
files; the bootstrap also passed a separate relocated-sibling-workspace test.
This does not establish training or independent scientific reproducibility.

Local private recovery manifests retain their original destination strings. The
exporter's optional `--manifest-root` supports that historical root after a move;
all 130 relocated original artifacts still match their recorded hashes. These
owner-only materials remain outside the supported public checkout.
