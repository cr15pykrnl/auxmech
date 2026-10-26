# Graphical abstracts

Plastic-hinge deformation images are clustered into labels and classified by logistic regression; the published 88.08 percent test accuracy concerns those cluster-derived labels.

## Figures

- [auxmech](assets/auxmech.svg): editable source `auxmech.tex`.

- [Standalone quantitative figure](assets/auxmech-plot.svg): gnuplot sources, CSV values and `plot-panel.tex`.

## Scientific evidence

Published Tables 1, 2 and 4 and the methods figures support the image pipeline. The input is a 7 by 8 re-entrant lattice represented by 64 by 64 pixel images. Eight K-means labels C0-C7 precede the KNet1 logistic-regression classifier. Training/validation/testing allocation is 60/20/20 percent. Table 2 test accuracies at learning rates 0.00001, 0.0001 and 0.001 are 46.29, 79.83 and 88.08 percent. Table 4 is described as the end-of-training confusion matrix; its diagonal entries, multiplied by 100, are recorded in class-results.csv. Four of six mechanisms were identified: V, X, V+Z+V and distorted X.

Table 4 does not explicitly establish which data split its matrix uses. The class-wise dot plot is therefore labeled confusion-matrix diagonal, not held-out class accuracy. The 70-103 percent dot axis is intentionally cropped for comparison; the test-accuracy bars start at zero. Class glyphs are illustrative reconstructions, not source images or measured centroids. Independent deformation-mode ground truth is unavailable. No new training or KNet2 result is implied.

Publication links: https://doi.org/10.1177/20414196241281069.

## Build and inspect

Requirements: Python 3, TeX/TikZ, Helvetica-compatible fonts, Ghostscript, Poppler
and a sibling research-ops checkout. Quantitative figures additionally require
gnuplot with the cairolatex terminal (tested with gnuplot 6.0.3). `GNUPLOT` can
select a compatible executable.

From the repository root:

```sh
sh figures/abstracts/build.sh
```

The script regenerates the selected SVGs and anti-aliased PNG fallbacks. Generated PDF intermediates, native
gnuplot exports and compiler logs stay in ignored `.local/figures/`; remove that
folder after checking the outputs. The published package retains editable TikZ,
plot scripts/data, required artwork, source evidence and checksums.

Abstracts use a 240 × 180 mm canvas and export at 2400 × 1800 px (4:3), with
960 × 720 px review views during builds. All native labels are 9 pt
Helvetica-compatible. Artwork and native labels remain black on white. PNG fallbacks use anti-aliased
greyscale edges; no one-bit threshold is applied. Original artwork inputs remain intact.
Informational dots, hatches, dash styles and markers encode categories.

Inspect full-size and README-size renders after editing. Check scientific
meaning, units, marker counts, label clearance, padding, legend scope and
bottom-right citations. A faithful replot is not an independent reproduction.
No publisher figures or manuscript PDFs are included, and no new asset reuse
license is asserted. Source data and illustrative content remain distinct.

## Selected export formats

The project README embeds the anti-aliased PNG with an opaque white background
for visibility in light and dark themes. Clicking the preview opens its SVG. PDF intermediates stay in ignored local storage;
no PDFs are published. Poppler's `pdftocairo` is required for SVG export.

These SVGs contain native vector geometry, plots and glyph outlines with no
embedded bitmap images. Keep the TeX sources for editable labels.

PNG fallbacks: [auxmech-plot](assets/auxmech-plot.png) · [auxmech](assets/auxmech.png)

Outer frames use equal 3 mm page margins on every side, with 4 mm gutters
between main panels/rows. Nested frames retain consistent visible clearances. Artwork proportions and native font sizes are preserved.

The data fields are centered horizontally in their panels, with axis titles, ticks
and direct labels checked separately for optical balance. Marker labels have a visible clearance
from the marker edge; captions/subtitles follow their panel centerline.

Learning-rate ticks use scientific e notation. The 60/20/20 allocation is shown
as a proportional strip; process arrows follow the top panels’ vertical midpoint.

Main frames use 1.5 pt borders; nested frames use 1 pt, with square miter joins. Plot axes and illustration
strokes retain their independent weights.
