#!/bin/sh

set -e
for i in overhang traverse vertical
do for h in l r
   do gnuplot <<!
      set term png
      set output "$i.$h.png"
      set title "$i($h)"
      set xlabel "seconds"
      s = "<./text.py $i.h5 $h"
      plot s u (\$0*0.02):1 w d lt rgb "red" t "AP", \
	   s u (\$0*0.02):2 w d lt rgb "green" t "UR", \
	   s u (\$0*0.02):3 w d lt rgb  "blue" t "DP"
!
   done
done
