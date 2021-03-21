#!/usr/bin/env python3

import h5py
import numpy as np
import sys

sys.argv.pop(0)
try:
    path = sys.argv.pop(0)
except IndexError:
    sys.stderr.write("explore.py: needs h5 file\n")
    sys.exit(2)
try:
    f = h5py.File(path, "r")
except OSError:
    sys.stderr.write("explore.py: fail to open '%s'\n" % path)
    sys.exit(2)

climbs = f["climbs"]
t0 = climbs["all"]["start_time"]
print(climbs["all"]["duration"])

print(climbs["0"]["moves_LH"]["start_time"] - t0)
print(climbs["0"]["moves_LH"]["end_time"] - t0)

        
f.close()
