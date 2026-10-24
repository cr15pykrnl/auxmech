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

This downloads 20 files (58,521,549 bytes) into ignored `data/knet2/`, including
2,482 grayscale images in Parquet. The `recovered` split is an inventory, not a
training/evaluation partition. The workflow needs no HF token or private files.
See the dataset card for units, labels, missing-input and split limitations.
