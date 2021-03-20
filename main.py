import h5py
import numpy as np
import math

f = h5py.File("a.h5", "r")
acc = f["acc_LH"]

def e(i, d0):
    d = math.sqrt(i[0]**2 + i[1]**2 + i[2]**2)
    return 2*(d0 - d)/d0  * i/d

def du(a, b, v, u):
    d = np.linalg.norm(b - a)
    return (u - v)  * (b - a)/d

def vec_cross(a, b):
    c = np.zeros(3)
    c[X] = a[Y] * b[Z] - b[Y] * a[Z];
    c[Y] = b[X] * a[Z] - a[X] * b[Z];
    c[Z] = a[X] * b[Y] - b[X] * a[Y];
    return c

def tri_normal(a, b, c):
    u = b - a
    v = c - a
    n = vec_cross(u, v)
    return vec_norm(n)

timestamp = acc["timestamp"]
AP = acc["AP"]
UR = acc["UR"]
DP = acc["DP"]

r0 = np.array([0.0, 0.0, 0.0])
r1 = np.array([1.0, 0.0, 0.0])
r2 = np.array([0.0, 1.0, 0.0])
r3 = np.array([0.0, 0.0, 1.0])

v0 = np.zeros_like(r0)
v1 = np.zeros_like(r1)
v2 = np.zeros_like(r2)
v3 = np.zeros_like(r3)

for i in range(300):
    k = 100
    dt = 0.02
    m = 100
    for j in range(m):
        g01 = k * e(r0 - r1, 1)
        g02 = k * e(r0 - r2, 1)
        g03 = k * e(r0 - r3, 1)

        g12 = k * e(r1 - r2, math.sqrt(2))
        g13 = k * e(r1 - r3, math.sqrt(2))
        g23 = k * e(r2 - r3, math.sqrt(2))

        h0 = g01 + g02 + g03
        h1 = -g01
        h2 = -g02
        h3 = -g03
        with open("%05d.off" % i, "w") as file:
            file.write("OFF\n")
            file.write("4 4 0\n")
            file.write("%g %g %g\n" % (r0[0], r0[1], r0[2]))
            file.write("%g %g %g\n" % (r1[0], r1[1], r1[2]))
            file.write("%g %g %g\n" % (r2[0], r2[1], r2[2]))
            file.write("%g %g %g\n" % (r3[0], r3[1], r3[2]))
            file.write("3 0 1 2\n")
            file.write("3 0 2 3\n")
            file.write("3 0 3 1\n")
            file.write("3 1 2 3\n")


print(np.linalg.norm(r1 - r0))
print(np.linalg.norm(r2 - r0))
print(np.linalg.norm(r3 - r0))

print(np.dot(r1 - r0, r2 - r0))
print(np.dot(r1 - r0, r3 - r0))
print(np.dot(r2 - r0, r3 - r0))
