# Graphical abstract review, version 1

These 4:3 candidates are prepared for owner feedback. The previously selected
figure remains in place. Paper titles/authors/DOIs stay outside the artwork.

## Refined brief

Connect finite-element plastic-hinge images, eight K-means labels and logistic regression to detected deformation mechanisms; add the reported test-accuracy comparison without presenting cluster labels as independent ground truth.

Use source-supported categories and results, a 240 × 180 mm canvas, 9 pt native
labels and precise black linework. Preserve distinctions between demonstrations,
qualitative observations, simulations and measured outcomes. No paper PDFs are
added to the repository.

## Candidates

- [auxmech](assets/auxmech.png), editable source `auxmech.tex`.

## Source evidence

Accepted manuscript figures 2–4 and 7, Table 1 (p. 14), and Table 2 (p. 15). Replotted test accuracies for learning rates 0.00001, 0.0001 and 0.001 are 46.29%, 79.83% and 88.08%; reported-results.csv preserves the values. These are three model-setting results, not error bars or independent replications. The plot uses a common 0–100% scale.

KNet1 published study only. Four of six named mechanisms were identified. Test accuracy is against cluster-derived labels; the paper explicitly notes the absence of independent ground truth. No new training or KNet2 accuracy result is implied.

Sources: https://doi.org/10.1177/20414196241281069.
Source values, conditions, transformations and input/output hashes are recorded
in `provenance.json` and, where numeric values are replotted, `reported-results.csv`.
Existing reused artwork retains its original resolution and generation provenance
in the selected figure's original source directory.

## Rebuild and review

With TeX, Ghostscript, Poppler and a sibling research-ops checkout, run from the
repository root (replace NAME with a candidate stem above):

```sh
python3 -I ../research-ops/.agents/skills/tikz-graphical-abstracts/scripts/render.py \
  figures/review-v1/NAME.tex --out-dir .local/abstract-review-v1 \
  --build-dir .local/abstract-review-build
```

The current renderer defaults to 2400 × 1800 output and 960 × 720 review for this
physical 4:3 page. PNGs are selected review exports; PDFs and logs stay ignored.
Keep the 4:3 geometry when adjusting individual panels. Re-render and inspect
labels, numeric scales, counts and arrow endpoints after changes. These are
first review compositions, not a claim of venue-specific submission compliance.
