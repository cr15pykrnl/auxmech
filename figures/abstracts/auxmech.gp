set terminal cairolatex pdf monochrome size 22cm,5.7cm font ",9"
set output "auxmech-plot.tex"
set datafile separator comma
set datafile columnheaders
unset key
unset grid
unset title
set border 3 linewidth 1.2 linecolor rgb "black"
set format x "%.0f"
set tics out nomirror scale .3
set multiplot layout 1,2
set lmargin at screen .10
set rmargin at screen .44
set bmargin at screen .23
set tmargin at screen .94
set xrange [70:103]
set yrange [.5:8.5]
set xtics 10
set ytics ("C0" 8,"C1" 7,"C2" 6,"C3" 5,"C4" 4,"C5" 3,"C6" 2,"C7" 1) scale 0
set xlabel "Confusion-matrix diagonal (percent)"
set ylabel "Image-cluster label" offset -2,0
plot "../../../figures/abstracts/class-results.csv" using 2:(8-$0) with points pointtype 7 pointsize .75 linecolor rgb "black", \
 "" using 2:(8-$0):(sprintf("%.1f",$2)) with labels left offset 1.0,0 textcolor rgb "black"
set lmargin at screen .65
set rmargin at screen .96
set xrange [0:100]
set yrange [.5:3.5]
set xtics 25
set ytics ("0.00001" 3,"0.0001" 2,"0.001" 1) scale 0
set xlabel "Test accuracy (percent)"
set ylabel "Learning rate" offset -1,0
plot "../../../figures/abstracts/reported-results.csv" every ::0::0 using ($2/2):(3):($2/2):(.32) with boxxyerrorbars fillstyle pattern 4 border linecolor rgb "black" linewidth 1.2, \
 "" every ::1::1 using ($2/2):(2):($2/2):(.32) with boxxyerrorbars fillstyle pattern 5 border linecolor rgb "black" linewidth 1.2, \
 "" every ::2::2 using ($2/2):(1):($2/2):(.32) with boxxyerrorbars fillstyle pattern 7 border linecolor rgb "black" linewidth 1.2, \
 "" using 2:(3-$0):(sprintf("%.2f",$2)) with labels left offset 1.0,0 textcolor rgb "black"
unset multiplot
set output
