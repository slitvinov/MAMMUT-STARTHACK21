#!/bin/sh

# better names for the h5 files

for i in overhang traverse vertical
do ln -fs data/$i/*_raw.h5 $i.h5
done
