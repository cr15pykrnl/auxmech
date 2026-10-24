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

## Local release record

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
  the pinned original HF card has not been amended with these findings.
  Publication does not establish scientific validity or reproduce results.

## Prepared card amendment, 2026-10-25

The exporter now includes the quantified split-overlap and 22.5-degree metadata
findings from [the audit](audit.md). A complete amended card is prepared at
`.local/hf-card-amendment/README.md` for review and later upload. Its source is the
pinned release card with only the scientific limitations section amended.
No data files, release checksums or `hf-dataset.json` pins were changed.

After an authorized card upload, record its new immutable card revision separately
from the original data revision. The owner selected MIT for newly authored Python scripts; figure rights/privacy
reviews are recorded in `release-manifest.json`. Publication and reciprocal
GitHub/HF revisions are recorded below after verification.
