#!/bin/sh

set -e
for i in overhang traverse vertical
do for h in l r
   do o=`./origin $i | awk '{print $2}'`
      v=`./video $i | awk '{print $2}'`
      gnuplot <<!
      set term png size 1280, 640
      set output "$i.$h.png"
      set title "$i($h)"
      set xlabel "seconds"
      set xtics 120
      set xtics add ("Origin" $o)
      set xtics add ("End" $o + $v)
      set yrange [-6:6]
      s = "<./text.py $i.h5 $h"
      plot s u (\$0*0.02):1 w l lt rgb "#0ffdff" t "AP", \
	   s u (\$0*0.02):2 w l lt rgb "#fa652b" t "UR", \
	   s u (\$0*0.02):3 w l lt rgb  "#19ff68" t "DP"
!
   done
done
