# Working on another machine

This checkout includes `AGENTS.md`. For owner development, clone the private
[research-ops repository](https://github.com/cr15pykrnl/research-ops) alongside
this repository and follow its [new-machine setup](https://github.com/cr15pykrnl/research-ops/blob/main/readme.md#working-on-another-machine).
Access uses the owner's research GitHub account; no credentials belong in Git.

From the directory containing both checkouts:

```sh
python3 -I research-ops/scripts/setup.py
python3 -I research-ops/scripts/setup-project.py --repo auxmech
python3 -I research-ops/scripts/setup-project.py --repo auxmech --check
```

Project setup configures the research Git identity and a relative path to shared
commit hooks. Shared rules stay in research-ops; each project keeps its own
scientific scope and limitations.

## Optional related data

The linked KNet2 inventory is a separate, incomplete extension. To download every
file at the reviewed immutable revision and inspect the image samples:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -I scripts/hf-data.py plan
curl -sSL --config .local/hf-download.conf
python -I scripts/hf-data.py verify
python -I scripts/inspect-hf-data.py
```

This downloads 20 files (58,527,509 bytes) into ignored `data/knet2/`, including
2,482 grayscale images in Parquet. The `recovered` split is an inventory, not a
training/evaluation partition. The workflow needs no HF token or private files.
See the dataset card for units, labels, missing-input and split limitations.

## Dataset maintenance

`scripts/normalize-hf-images.py` repairs the nullable Arrow image-path type in
trusted release Parquet files. It writes a new file and verifies every value,
embedded PNG byte and stored pixel hash. It never loads recovered pickle files.
This patch changes storage typing, not data content, labels or scientific claims.
The data/card revisions and verification are recorded in [the HF release note](docs/hf-release.md).

Selected figures use SVG with anti-aliased PNG fallbacks. Rebuilding SVG requires
Poppler's `pdftocairo`; PDF intermediates remain local and ignored.

## Paper 2 review

Continue the work-in-progress review in [papers/paper-2/](papers/paper-2/README.md).
Use its single candidate bibliography; preserve citation keys and document
metadata corrections and screening decisions. Its unverified records are separate
from the published Paper 1 reference list and the KNet2 partial dataset.
