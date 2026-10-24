#!/usr/bin/env python3
"""Verify and inspect the pinned KNet2 recovery, without loading any pickle.

Checks all sample pixels, metadata finiteness and release identity. Saves one
example PNG. Cluster IDs and notebook modes are unverified annotations.
"""
import argparse
import collections
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path

import pyarrow.parquet as pq
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=ROOT / 'data/knet2')
    parser.add_argument('--output', type=Path, default=ROOT / '.local/knet2-sample.png')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('hf_data', ROOT / 'scripts/hf-data.py')
    client = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(client)
    verification = client.verify(args.directory)
    table = pq.read_table(args.directory / 'processed/images.parquet')
    rows = table.to_pylist()
    if len(rows) != 2482:
        raise ValueError('Unexpected sample count for pinned release')
    hashes, angles, clusters, ids = [], collections.Counter(), collections.Counter(), set()
    for row in rows:
        if row['sample_id'] in ids:
            raise ValueError('Repeated sample ID')
        ids.add(row['sample_id'])
        for key in ['theta_degrees', 'recovered_stress', 'recovered_strain']:
            if not math.isfinite(row[key]):
                raise ValueError('Non-finite sample metadata')
        with Image.open(io.BytesIO(row['image']['bytes'])) as image:
            if image.mode != 'L' or image.size != (199, 126):
                raise ValueError('Unexpected image shape or pixel type')
            digest = hashlib.sha256(image.tobytes()).hexdigest()
            if digest != row['image_sha256']:
                raise ValueError('Decoded pixel hash mismatch')
        hashes.append(digest)
        angles[row['theta_degrees']] += 1
        clusters[row['cluster_id']] += 1
    if set(clusters) != set(range(24)):
        raise ValueError('Unexpected cluster coverage')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(rows[0]['image']['bytes'])
    print(json.dumps({**verification, 'samples': len(rows), 'grayscale_shape_height_width': [126, 199],
        'angle_counts': dict(sorted(angles.items())), 'cluster_counts': dict(sorted(clusters.items())),
        'repeated_pixel_hashes_beyond_first': len(hashes) - len(set(hashes)),
        'example_sample_id': rows[0]['sample_id'], 'example_png': str(args.output),
        'interpretation': 'Inventory only; annotations and evaluation independence are unverified.'}, indent=2))


if __name__ == '__main__':
    main()
