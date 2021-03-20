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

try:
    hand = sys.argv.pop(0)
    acc = f[{"l" : "acc_LH", "r" : "acc_RH"}[hand]]
except IndexError:
    sys.stderr.write("explore.py: needs l or r\n")
    sys.exit(2)
except KeyError:
    sys.stderr.write("explore.py: unknown hand '%s'\n" % hand)
    sys.exit(2)    
AP = acc["AP"]
UR = acc["UR"]
DP = acc["DP"]
for i in range(AP.size):
    try:
        print("%.16e %.16e %.16e" % (AP[i], UR[i], DP[i]))
    except BrokenPipeError:
        sys.exit(0)
        
f.close()
