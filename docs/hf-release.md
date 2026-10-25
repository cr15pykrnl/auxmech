# KNet2 data release 0.1.1

The public [KNet2 partial recovery](https://huggingface.co/datasets/cr15pykrnl/knet2-auxetic-deformation-partial)
is related unpublished extension data, not the published KNet1 study's
reproduction dataset. The owner authorized the audited fixes on 2026-10-25.

- Repaired data/schema revision: `1b2ba3915a38410cfb3dcbafb71e41f1a7c426d0`.
- Download/card revision: `66364b17837e107555870e7b1df802db9caedaf3` (pinned in `hf-dataset.json`).
- Account/namespace verified: `cr15pykrnl`; repository type: dataset; public.
- Licence: dataset CC BY 4.0; newly authored maintenance Python script MIT.
- Original content: 2,482 grayscale samples, ten registration composites,
  seven raw force/displacement tables, one video, 24 cluster IDs and 38
  recovered clustering-score rows.

The nullable `image.path` Arrow field was changed from null type to string.
All rows, numeric values and embedded PNG bytes are unchanged. Both Parquet
files were reread and every decoded image checked. Local datasets 3.6.0 loading
recognizes the HF Image feature and decodes all 2,492 images/composites; sample
pixel hashes match. Checks used Python 3.12.9, NumPy 1.26.4, pandas 2.2.3,
PyArrow 19.0.1 and Pillow 11.3.0.

The card replaces the deleted Deformvis link with the maintained AuxMech
companion, adds immutable download and client-loading examples, and distinguishes
data revisions from later documentation commits. Matching maintenance source is versioned here; its SHA-256 is recorded in HF
validation metadata. No original KNet2 training pipeline is claimed as released.

The original raw assets were not altered. Missing raw pairs, unresolved physical
units, proposed notebook labels, duplicates and split leakage limitations remain
explicit in the card. No training, inference or accuracy reproduction was run.

Both live viewer configurations now expose Image features. Their first sample
and composite previews were fetched and decoded at the source dimensions. HF
serves JPEG previews; these can differ from the lossless embedded PNGs, which
remain unchanged and must be used for pixel analysis. A fresh download of every
released file passed size/SHA-256 verification; all sample pixel hashes passed.
