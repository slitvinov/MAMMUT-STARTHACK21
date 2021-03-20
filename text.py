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
   
acc = f["acc_LH"]
AP = acc["AP"]
UR = acc["UR"]
DP = acc["DP"]
for i in range(AP.size):
    print(AP[i], UR[i], DP[i])
f.close()
