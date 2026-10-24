# Working on another machine

This checkout includes `AGENTS.md`. For owner development, clone the private
[research-ops repository](https://github.com/cr15pykrnl/research-ops) alongside
this repository and follow its [new-machine setup](../research-ops/readme.md#working-on-another-machine).
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
