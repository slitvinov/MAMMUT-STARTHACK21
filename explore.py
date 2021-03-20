#!/usr/bin/env python3

import h5py
import numpy as np
import sys

sys.argv.pop()
try:
    path = sys.argv.pop(0)
except IndexError:
    sys.stderr.write("explore.py: needs h5 file\n")
    sys.exit(2)

f = h5py.File(path, "r")
acc = f["acc_LH"]
AP = acc["AP"]
UR = acc["UR"]
DP = acc["DP"]

for i in range(AP.size):
    print(AP[i], UR[i], DP[i])
