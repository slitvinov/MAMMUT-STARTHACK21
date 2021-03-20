#!/bin/sh

for i in overhang traverse vertical
do ln -fs data/$i/*_raw.h5 $i.h5
done
