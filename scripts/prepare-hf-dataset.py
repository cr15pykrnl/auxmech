#!/usr/bin/env python3
"""Export the hash-verified partial KNet2 recovery without publishing it.

Run with Python 3.12 in isolated mode. Recovered pickle loading accepts only
specific pandas/NumPy constructors after checking the private recovery manifest.
This reduces exposure; it is not a general-purpose safe pickle loader.
"""
import argparse
import ast
import collections
import csv
import hashlib
import importlib
import io
import json
import math
import pickle
import platform
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import PIL
import pyarrow
import pyarrow.parquet as pq
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'hf-staging/km4-neural-network-extension/datasets'
REPO_ID = 'cr15pykrnl/knet2-auxetic-deformation-partial'
ALLOWED = {
    'pandas.core.frame': {'DataFrame'},
    'pandas.core.internals.managers': {'BlockManager'},
    'pandas._libs.internals': {'_unpickle_block'},
    'numpy.core.multiarray': {'_reconstruct', 'scalar'},
    'numpy': {'ndarray', 'dtype'}, 'builtins': {'slice'},
    'pandas.core.indexes.base': {'_new_Index', 'Index'},
    'pandas.core.indexes.range': {'RangeIndex'},
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RecoveryUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name not in ALLOWED.get(module, set()):
            raise pickle.UnpicklingError(f'Unapproved constructor: {module}.{name}')
        return getattr(importlib.import_module(module), name)


def recover(name, manifest):
    path = BASE / 'processed' / name
    entry = manifest.get(path.relative_to(ROOT).as_posix())
    if not entry or sha(path) != entry['sha256']:
        raise ValueError(f'Recovery checksum missing or changed: {name}')
    with path.open('rb') as stream:
        result = RecoveryUnpickler(stream).load()
        if stream.read(1):
            raise ValueError(f'Trailing pickle content: {name}')
    return result


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def write_csv(path, rows, fields):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def png(array):
    if not isinstance(array, np.ndarray) or array.dtype != np.uint8 or array.ndim != 2:
        raise ValueError('Expected a two-dimensional uint8 image')
    stream = io.BytesIO()
    Image.fromarray(array).save(stream, format='PNG')
    payload = stream.getvalue()
    with Image.open(io.BytesIO(payload)) as decoded:
        if not np.array_equal(np.asarray(decoded), array):
            raise ValueError('PNG conversion changed pixels')
    return {'bytes': payload, 'path': None}


def write_images(path, rows, features, originals):
    frame = pd.DataFrame(rows)
    table = pyarrow.Table.from_pandas(frame, preserve_index=False)
    metadata = dict(table.schema.metadata or {})
    metadata[b'huggingface'] = json.dumps({'info': {'features': features}}).encode()
    table = table.replace_schema_metadata(metadata)
    pq.write_table(table, path, compression='zstd')
    loaded = pq.read_table(path).to_pandas()
    pd.testing.assert_frame_equal(frame.drop(columns='image'), loaded.drop(columns='image'))
    for image, original in zip(loaded.image, originals, strict=True):
        with Image.open(io.BytesIO(image['bytes'])) as decoded:
            if not np.array_equal(np.asarray(decoded), original):
                raise ValueError('Parquet round trip changed image pixels')
    return len(loaded)


def mapping_from_notebook(path):
    notebook = json.loads(path.read_text())
    for cell in notebook['cells']:
        source = ''.join(cell.get('source', []))
        if 'label_to_deformation_mode_map = {' not in source:
            continue
        values = {}
        for node in ast.parse(source).body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        values[target.id] = ast.literal_eval(node.value)
        return values['deformation_modes'], values['label_to_deformation_mode_map']
    raise ValueError('Notebook mapping not found')


def card(count, duplicates, shapes, modes):
    return f'''---
pretty_name: KNet2 Auxetic Deformation — Partial Recovery
license: cc-by-4.0
language:
- en
size_categories:
- 1K<n<10K
tags:
- materials-science
- auxetics
- simulation
- partial-recovery
configs:
- config_name: recovered-images
  data_files:
  - split: recovered
    path: processed/images.parquet
- config_name: registration-composites
  data_files:
  - split: recovered
    path: processed/registration-composites.parquet
---
# KNet2 auxetic deformation: partial recovery

Version 0.1.0. Intended repository: `{REPO_ID}`.
This release preserves available simulation-derived deformation images and
associated records from the separate KNet2 neural-network extension draft.
It is incomplete. It is not the published KNet1 paper's reproduction dataset,
not a verified benchmark, and contains no checkpoint or accuracy claim.

## Source and relationship to the paper

The recovered draft is titled *KNet2: Multi-layer Neural Network and k-means
Clustering for Detecting Deformation Mechanisms in Re-entrant Honeycomb Auxetics*,
by Gaurav Singh, Rahul Singh Dhari and Zia Javanbakht. No publication identifier
has been established for this draft.

Prior work: [Automated detection of deformation mechanisms in re-entrant
honeycomb auxetics using machine learning](https://doi.org/10.1177/20414196241281069),
International Journal of Protective Structures 16(4), 853–877 (2025).
That paper uses logistic regression; its results must not be attributed to this
KNet2 recovery. The exact source Git revision is unavailable.

## Contents and collection

- {count:,} recovered registered grayscale images, each {shapes[0]} pixels
  (height × width), with original frame references and loading-angle values.
- Ten per-angle registration composites, including recovered bounding boxes.
- All 24 recovered K-means cluster IDs; notebook mode mapping included as an
  explicitly unverified annotation proposal, not expert ground truth.
- One raw video and seven raw force/displacement CSV tables, plus the original
  metadata and an explicit availability inventory.
- Thirty-eight recovered clustering-score rows, not rerun evaluations.

Recovered code indicates grayscale conversion, inverse thresholding, rotation,
edge removal, dilation, scaling, per-angle bounding-box registration and intensity
normalisation. See `metadata/schema.json` for the recovered settings and caveats.
Raw assets were copied unchanged. Images were losslessly converted from two
hash-verified recovered pandas pickle sources into PNG bytes embedded in Parquet.
The two recovered image collections agree on all samples and pixels, so images
are stored once. Source file hashes are in `metadata/provenance.json`.

## Schema, labels and units

`processed/images.parquet` contains `sample_id`, `theta_degrees`, `frame_index`,
`recovered_stress`, `recovered_strain`, `cluster_id`, `notebook_mode_code`,
`notebook_mode_id`, `image_sha256` and `image`.
Angles are in degrees as indicated by recovered code/draft context; frame indices
are preserved without changing their original zero-based reference convention.
Images are uint8, range 0–255. Their original shape is retained; they are not
resized to the network's 64 × 64 input.

Physical units of the raw `dy`, `f` and recovered stress values have not been
independently established. `recovered_strain` is dimensionless by its intended
meaning, but its calculation's unit consistency has not been independently
established. Numeric values are preserved without conversion or a unit claim.
Do not combine these values with external physical measurements without resolving
units. All numeric output values were checked for finiteness.

The notebook mode codes are {', '.join(modes)}. Their integer IDs and the complete
cluster-to-code mapping are in `metadata/schema.json`. Codes are retained as
written in the source; expansions and scientific correctness are not asserted.

## Splits and limitations

`recovered` is an inventory split, not a training, validation or test partition.
No historical evaluation partition is reconstructed. Samples from one angle may
share a simulation sequence, and image duplicates may cross angles or frames.
There are {duplicates} repeated image hashes beyond their first occurrence.
Split by verified simulation/sequence identity and duplicate lineage before
training or evaluation; angle alone is not proven to identify an independent run.

Nine videos and three force/displacement tables named by raw metadata are absent.
The available video has no paired table. Thus no complete raw video/table pair
is available, and the raw pipeline cannot be reproduced end to end from this
release. The 2,482 derived samples cover ten angles despite missing raw assets;
existence of derived samples is not proof of complete raw provenance.

Features/PCA state, original input images, the semantic-label pickle and model
checkpoint are absent. Balanced data and pickled runtime dataloaders are excluded.
No model loading, training, accuracy reproduction or independent annotation
validation has been performed. Clustering scores lack the recovered feature
matrix needed to rerun them.

### Subsequent recovery audit (2026-10-24)

A reconstruction of the recovered helper's 80:20 seed-42 row split on the
6,000-row balanced collection found 574 shared source-frame keys. Of 1,200
validation rows, 1,018 have a source key also present in training. This is a
reconstruction from recovered code and data, not the saved historical runtime
split or a new performance measurement. The balanced collection is excluded
from this release. Split source sequences and duplicate lineage before resampling.

At 22.5 degrees, the available raw force/displacement table does not reproduce
the recovered image metadata under the supplied formulas. Among 488 records,
484 stress and 487 strain values differ exactly; maximum absolute differences
are approximately 0.05217647 and 0.01155979 in unresolved recovered units.
Six other available angles reproduce the arithmetic exactly. Both versions are
preserved; resolve their source/version relationship before physical analysis.
These checks establish neither physical units nor annotation correctness.

## Loading

The verified local loading path uses PyArrow and Pillow:

```python
import io
import pyarrow.parquet as pq
from PIL import Image
samples = pq.read_table("processed/images.parquet").to_pandas()
image = Image.open(io.BytesIO(samples.iloc[0]["image"]["bytes"]))
```

HF configuration `recovered-images` selects the `recovered` inventory split.
No executable dataset script is required. Format and every image round trip were checked with
Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__},
PyArrow {pyarrow.__version__} and Pillow {PIL.__version__}.
HF viewer rendering and the HF datasets client have not been independently tested.

## Licence and attribution

CC BY 4.0, selected by the rights-confirming dataset owner on 2026-10-24.
See `LICENSE`. Attribute the original research authors above and identify this
artifact as **KNet2 auxetic deformation: partial recovery, version 0.1.0**,
maintained by cr15pykrnl. Cite its immutable HF revision after publication.
The prior paper DOI is background, not a DOI for this dataset.

For schema, omissions and verification results see `metadata/`; for exact release
bytes see `checksums.sha256`. Checksums establish byte integrity, not scientific
validity or completeness.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--license-file', type=Path, required=True,
                        help='Downloaded CC BY 4.0 legalcode.txt from Creative Commons')
    parser.add_argument('--manifest-root', type=Path,
                        help='Historical checkout root recorded in the private recovery manifest')
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise FileExistsError('Refusing to overwrite an existing release directory')
    licence = args.license_file.read_text()
    if not licence.startswith('Attribution 4.0 International'):
        raise ValueError('Expected the CC BY 4.0 legal text')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(BASE / 'raw/videos/Deg_00.0.avi'),
                    '-f', 'null', '-'], check=True, capture_output=True)
    entries = json.loads((ROOT / 'provenance/organisation-manifest.json').read_text())
    manifest_root = args.manifest_root.resolve() if args.manifest_root else ROOT
    manifest = {Path(x['destination']).relative_to(manifest_root).as_posix(): x for x in entries}
    registered, composites = recover('registered-images.pkl', manifest)
    labelled = recover('labelled-images-2.pkl', manifest)
    scores = recover('scores.pkl', manifest)
    pd.testing.assert_frame_equal(registered.drop(columns='img'), labelled.drop(columns=['img', 'label']))
    if len(registered) != len(labelled):
        raise ValueError('Image collection lengths differ')
    for left, right in zip(registered.img, labelled.img, strict=True):
        if not np.array_equal(left, right):
            raise ValueError('Registered and labelled pixels differ')
    notebook = ROOT / 'related-work/km4-neural-network-extension/notebooks/process.ipynb'
    modes, mapping = mapping_from_notebook(notebook)
    if set(labelled.label.unique()) != set(mapping):
        raise ValueError('Notebook mapping does not cover exactly the recovered cluster IDs')
    numeric = labelled.drop(columns=['img']).astype(float)
    if not np.isfinite(numeric.to_numpy()).all():
        raise ValueError('Non-finite recovered metadata')
    if not labelled.ref.map(lambda x: int(x) == x).all():
        raise ValueError('Noninteger frame reference')
    if labelled.duplicated(['theta', 'ref']).any():
        raise ValueError('Ambiguous angle/frame key')
    for name in ['processed', 'metadata', 'raw/fd-data', 'raw/videos']:
        (out / name).mkdir(parents=True, exist_ok=True)
    rows, hashes = [], []
    for row in labelled.itertuples(index=False):
        label = int(row.label)
        digest = hashlib.sha256(row.img.tobytes()).hexdigest()
        hashes.append(digest)
        rows.append({'sample_id': f'angle-{row.theta:04.1f}-frame-{int(row.ref):06d}',
                     'theta_degrees': float(row.theta), 'frame_index': int(row.ref),
                     'recovered_stress': float(row.stress), 'recovered_strain': float(row.strain),
                     'cluster_id': label, 'notebook_mode_code': mapping[label],
                     'notebook_mode_id': modes[mapping[label]], 'image_sha256': digest,
                     'image': png(row.img)})
    features = {key: {'dtype': str(pd.DataFrame(rows[:1]).dtypes[key]), '_type': 'Value'}
                for key in rows[0] if key != 'image'}
    for key in ['sample_id', 'notebook_mode_code', 'image_sha256']:
        features[key]['dtype'] = 'string'
    features['image'] = {'_type': 'Image'}
    write_images(out / 'processed/images.parquet', rows, features, labelled.img)
    comp_rows = [{'theta_degrees': float(x.theta), 'x': int(x.x), 'y': int(x.y),
                  'width': int(x.w), 'height': int(x.h), 'image': png(x.img)}
                 for x in composites.itertuples(index=False)]
    comp_features = {k: {'dtype': 'float64' if k == 'theta_degrees' else 'int64', '_type': 'Value'}
                     for k in comp_rows[0] if k != 'image'}
    comp_features['image'] = {'_type': 'Image'}
    write_images(out / 'processed/registration-composites.parquet', comp_rows, comp_features, composites.img)
    score_rows = [{k: int(v) if k == 'n_clusters' else float(v) for k, v in x.items()} for x in scores]
    if not all(math.isfinite(v) for x in score_rows for v in x.values()):
        raise ValueError('Non-finite clustering scores')
    write_csv(out / 'processed/clustering-scores.csv', score_rows, list(score_rows[0]))
    source_paths = [BASE / 'processed' / x for x in ['registered-images.pkl', 'labelled-images-2.pkl', 'scores.pkl']]
    source_paths += [notebook, ROOT / 'related-work/km4-neural-network-extension/src/km4.py']
    availability, raw_summary = [], []
    with (BASE / 'raw/metadata.csv').open(newline='') as stream:
        metadata = [{k.strip(): v.strip() for k, v in row.items()} for row in csv.DictReader(stream)]
    for row in metadata:
        for kind, column in [('video', 'video_file'), ('force-displacement', 'fd_data_file')]:
            relative = row[column]
            path = BASE / 'raw' / relative
            exists = path.is_file()
            availability.append({'theta_degrees': row['theta'], 'kind': kind,
                                 'path': 'raw/' + relative, 'available': exists})
            if not exists:
                continue
            if kind == 'force-displacement':
                values = pd.read_csv(path)
                if list(values.columns) != ['ref', 'dy', 'f'] or not np.isfinite(values.to_numpy(dtype=float)).all():
                    raise ValueError(f'Invalid raw table: {relative}')
                raw_summary.append({'path': 'raw/' + relative, 'rows': len(values), 'columns': list(values.columns)})
            shutil.copyfile(path, out / 'raw' / relative)
            source_paths.append(path)
    shutil.copyfile(BASE / 'raw/metadata.csv', out / 'raw/metadata.csv')
    source_paths.append(BASE / 'raw/metadata.csv')
    provenance = []
    for path in source_paths:
        relative = path.relative_to(ROOT).as_posix()
        if sha(path) != manifest[relative]['sha256']:
            raise ValueError(f'Source changed: {relative}')
        provenance.append({'source': relative, 'sha256': sha(path), 'bytes': path.stat().st_size})
    write_csv(out / 'metadata/input-availability.csv', availability, ['theta_degrees', 'kind', 'path', 'available'])
    write_json(out / 'metadata/provenance.json', {'sources': provenance,
        'code_revision': None, 'export_script_sha256': sha(Path(__file__)),
        'conversion': 'Lossless embedded PNG images in Parquet; scores CSV; unchanged raw bytes.'})
    write_json(out / 'metadata/schema.json', {'schema_version': '1.0', 'sample_features': features,
        'image_shape_height_width': [126, 199], 'pixel_dtype': 'uint8',
        'raw_table_columns': {'ref': 'original frame reference', 'dy': 'displacement; units unresolved',
                              'f': 'force; units unresolved'},
        'stress_units': 'unresolved', 'strain_units': 'intended dimensionless; unit consistency unverified',
        'notebook_mode_ids': modes, 'notebook_cluster_to_mode': mapping,
        'annotation_status': 'Notebook-derived proposal; not independently validated',
        'recovered_code_settings': {'binary_threshold': 127, 'clean_width_pixels': 10,
            'resize_factor': 0.25, 'dilate_kernel': [11, 11], 'dilate_iterations': 3,
            'force_to_stress_divisor': 3557.6, 'displacement_to_strain_divisor': 91,
            'caveat': 'Recovered settings; not rerun or validated against all derived images.'}})
    duplicates = len(hashes) - len(set(hashes))
    shapes = sorted({str(x.shape) for x in labelled.img})
    if shapes != ['(126, 199)']:
        raise ValueError(f'Unexpected image shapes: {shapes}')
    report = {'checked_on': '2026-10-24', 'repo_id': REPO_ID, 'status': 'validated-local-export',
        'images': len(rows), 'registration_composites': len(comp_rows), 'cluster_score_rows': len(scores),
        'cluster_counts': {str(k): int(v) for k, v in labelled.label.value_counts().sort_index().items()},
        'angle_counts': {str(k): int(v) for k, v in labelled.theta.value_counts().sort_index().items()},
        'repeated_pixel_hashes_beyond_first': duplicates, 'raw_tables': raw_summary,
        'missing_inputs': [x['path'] for x in availability if not x['available']],
        'checks': ['source-checksums', 'restricted-pickle-constructors', 'metadata-finiteness',
            'registered-labelled-equality', 'unique-angle-frame-keys', 'all-image-png-parquet-roundtrips',
            'all-metadata-parquet-roundtrips', 'raw-table-schema-finiteness', 'score-finiteness',
            'raw-video-all-frame-decoding'],
        'not_checked': ['training', 'inference', 'performance', 'physical-units',
            'split-independence', 'annotation-correctness', 'hf-datasets-loader'],
        'environment': {'python': platform.python_version(), 'numpy': np.__version__,
            'pandas': pd.__version__, 'pyarrow': pyarrow.__version__, 'pillow': PIL.__version__}}
    write_json(out / 'metadata/validation.json', report)
    (out / 'README.md').write_text(card(len(rows), duplicates, shapes, modes))
    (out / 'LICENSE').write_text(licence)
    (out / '.gitattributes').write_text('*.avi filter=lfs diff=lfs merge=lfs -text\n'
                                      '*.parquet filter=lfs diff=lfs merge=lfs -text\n')
    files = sorted(p for p in out.rglob('*') if p.is_file())
    (out / 'checksums.sha256').write_text(''.join(
        f'{sha(p)}  {p.relative_to(out).as_posix()}\n' for p in files))
    print(json.dumps({'package': str(out.relative_to(ROOT)), 'images': len(rows),
                      'missing_inputs': len(report['missing_inputs']), 'duplicate_images': duplicates}))


if __name__ == '__main__':
    main()
