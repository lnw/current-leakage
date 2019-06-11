set terminal postscript color enhanced 'Palatino'
set output 'figgnu_benzene-plane0.ps'
# #show output
set key out horiz center top
set title "benzene, def-SVP/dft(bp/m3)/scfconv=6, z=0: {/Symbol D} J/V [10^3 nA T^{-1} au^{-3}]"
# #set yrange [0:20]
# #set xrange [-2:2]

set xlabel "[au]"
set ylabel "[au]"
set xtics out
set xtics mirror
set ytics out
set ytics mirror
set size ratio 1

set autoscale xfix
set autoscale yfix
set autoscale cbfix

set cbrange [-0.06:0.06]
set palette defined (-0.04 "red", 0 "white", 0.04 "blue")

# set label '' at 2.6235,0.0 point front
# set label '' at -2.6235,0.0 point front
# set label '' at 1.3118,2.2720 point front
# set label '' at 1.3118,-2.2720 point front
# set label '' at -1.3118,2.2720 point front 
# set label '' at -1.3118,-2.2720 point front 
# #set label '+' at 4.6518,0.0 point front tc ls 1
# #set label '+' at -4.6518,0.0 point front tc ls 1
# set label '' at 2.3258,4.0285 point front
# set label '' at 2.3258,-4.0285 point front
# set label '' at -2.3258,4.0285 point front 
# set label '' at -2.3258,-4.0285 point front 
plot "figgnu_benzene-plane0.dat" matrix nonuniform with image notitle

