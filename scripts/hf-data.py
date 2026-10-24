#!/usr/bin/env python3
"""Plan pinned public HF downloads and verify the exact release bytes.

The plan is a curl configuration, allowing the same public HTTPS workflow in
normal terminals and hosts where only curl is allowed to use the network.
Credentials and pickle loading are neither needed nor used.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def release():
    spec = json.loads((ROOT / 'hf-dataset.json').read_text())
    revision = spec['revision']
    if len(revision) != 40 or any(x not in '0123456789abcdef' for x in revision):
        raise ValueError('Expected a full immutable HF commit hash')
    if spec['repo_id'] != 'cr15pykrnl/knet2-auxetic-deformation-partial':
        raise ValueError('Unexpected dataset identity')
    names = set()
    for entry in spec['files']:
        name = PurePosixPath(entry['path'])
        if name.is_absolute() or '..' in name.parts or '\\' in entry['path']:
            raise ValueError('Unsafe release path')
        if str(name) in names:
            raise ValueError('Duplicate release path')
        names.add(str(name))
        if len(entry['sha256']) != 64 or entry['bytes'] < 0:
            raise ValueError('Invalid release checksum or size')
    return spec


def destination(base, name):
    path = base / name
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f'Destination escapes data directory: {name}')
    return path


def verify(base):
    """Verify every release file by SHA-256 and byte count; report all failures."""
    spec = release()
    problems = []
    for entry in spec['files']:
        path = destination(base, entry['path'])
        if not path.is_file():
            problems.append(entry['path'] + ': missing')
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if path.stat().st_size != entry['bytes'] or digest != entry['sha256']:
            problems.append(entry['path'] + ': size/checksum mismatch')
    if problems:
        raise ValueError('\n'.join(problems))
    return {'repo_id': spec['repo_id'], 'revision': spec['revision'],
            'verified_files': len(spec['files']), 'bytes': sum(x['bytes'] for x in spec['files'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['plan', 'verify'])
    parser.add_argument('--directory', type=Path, default=ROOT / 'data/knet2')
    parser.add_argument('--config', type=Path, default=ROOT / '.local/hf-download.conf')
    args = parser.parse_args()
    spec = release()
    if args.action == 'verify':
        print(json.dumps(verify(args.directory)))
        return
    base = args.directory.resolve()
    lines = ['# Public immutable release; no authentication required.',
             'fail', 'location', 'silent', 'show-error', 'max-time = 180']
    for entry in spec['files']:
        path = destination(base, entry['path'])
        path.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://huggingface.co/datasets/{spec['repo_id']}/resolve/{spec['revision']}/{entry['path']}"
        lines += ['url = ' + json.dumps(url), 'output = ' + json.dumps(str(path))]
    args.config.parent.mkdir(parents=True, exist_ok=True)
    args.config.write_text('\n'.join(lines) + '\n')
    print(json.dumps({'curl_config': str(args.config), 'files': len(spec['files']),
                      'revision': spec['revision']}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(str(error))
