#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Repair HF image storage types without changing recovered values or pixels.

Inputs are trusted release Parquet files, not recovered pickle objects.
The nullable image path must have Arrow string type even when every value is
None. An Arrow null-typed path causes HF to infer a generic bytes/path record.
Outputs are new files; existing inputs and destinations are never overwritten.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from PIL import Image


def normalize(source, destination):
    """Return verification evidence for a value-preserving schema repair."""
    if source.resolve() == destination.resolve() or destination.exists():
        raise ValueError('Choose a new output path; source/destination are preserved.')
    original = pq.read_table(source)
    field = original.schema.field('image')
    if field.type != pa.struct([('bytes', pa.binary()), ('path', pa.null())]):
        raise ValueError('Expected original image storage: binary bytes, null path.')
    metadata = original.schema.metadata or {}
    features = json.loads(metadata[b'huggingface'])['info']['features']
    if features['image'] != {'_type': 'Image'}:
        raise ValueError('Expected the original HF Image feature declaration.')
    image_type = pa.struct([('bytes', pa.binary()), ('path', pa.string())])
    schema = original.schema.set(original.schema.get_field_index('image'),
                                 pa.field('image', image_type, nullable=field.nullable))
    repaired = original.cast(schema)
    destination.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(repaired, destination, compression='zstd')
    loaded = pq.read_table(destination)
    if original.to_pylist() != loaded.to_pylist():
        raise ValueError('Repaired Parquet values differ from the input.')
    pixel_hashes = []
    for row in loaded.to_pylist():
        with Image.open(io.BytesIO(row['image']['bytes'])) as image:
            digest = hashlib.sha256(image.tobytes()).hexdigest()
            if 'image_sha256' in row and digest != row['image_sha256']:
                raise ValueError('Decoded image checksum differs from stored metadata.')
            pixel_hashes.append(digest)
    return {'rows': loaded.num_rows, 'values_equal': True,
            'embedded_png_bytes_equal': True, 'decoded_images_checked': len(pixel_hashes),
            'image_storage': 'struct<bytes: binary, path: string>',
            'hf_feature': features['image'],
            'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'output_sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(json.dumps(normalize(args.source, args.destination), indent=2))


if __name__ == '__main__':
    main()
