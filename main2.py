import h5py
import math

X, Y, Z = 0, 1, 2

f = h5py.File("a.h5", "r")
acc = f["acc_LH"]

def vec_cross(a, b):
    return [a[Y] * b[Z] - b[Y] * a[Z],
            b[X] * a[Z] - a[X] * b[Z],
            a[X] * b[Y] - b[X] * a[Y]]

def vec_minus(a, b):
    return [a[X] - b[X], a[Y] - b[Y], a[Z] - b[Z]]

def tri_normal(a, b, c):
    u = vec_minus(b, a)
    v = vec_minus(c, a)
    n = vec_cross(u, v)
    return vec_norm(n)

def vec_dot(a, b):
    return a[X] * b[X] + a[Y] * b[Y] + a[Z] * b[Z]

def vec_abs(a):
    return math.sqrt(vec_dot(a, a))

def vec_norm(a):
    s = vec_abs(a)
    return vec_scalar(a, 1/s)

def vec_scalar(a, s):
    return [a[X]*s, a[Y]*s, a[Z]*s]

def dtri_area(a, b, c):
    n = tri_normal(a, b, c)
    n2 = vec_scalar(n, 0.5)
    ab, bc, ca = tri_edg(a, b, c)
    da = vec_cross(n2, bc)
    db = vec_cross(n2, ca)
    dc = vec_cross(n2, ab)
    return da, db, dc

def tri_edg(a, b, c):
    ab = vec_minus(b, a)
    bc = vec_minus(c, b)
    ca = vec_minus(a, c)
    return ab, bc, ca

def tri_area(a, b, c):
    u = vec_minus(b, a)
    v = vec_minus(c, a)
    n = vec_cross(u, v)
    return vec_abs(n) / 2

def dtri_force(a, b, c):
    A0 = 0.5
    A = tri_area(a, b, c)
    dA = A0 - A
    da, db, dc = dtri_area(a, b, c)
    return vec_scalar(da, dA), vec_scalar(db, dA), vec_scalar(dc, dA)

def vec_scalar_append(a, s, b):
    b[X] += s * a[X]
    b[Y] += s * a[Y]
    b[Z] += s * a[Z] 

timestamp = acc["timestamp"]
AP = acc["AP"]
UR = acc["UR"]
DP = acc["DP"]

r0 = [0.0, 0.0, 0.0]
r1 = [1.0, 0.0, 0.0]
r2 = [0.0, 1.0, 0.0]
r3 = [0.0, 0.0, 1.0]

v0 = [0, 0, 0]
v1 = [0, 0, 0]
v2 = [0, 0, 0]
v3 = [0, 0, 0]

K = 1000.0
dt = 0.02
for i in range(1000):
    r01 = vec_minus(r1, r0)
    r02 = vec_minus(r2, r0)
    r03 = vec_minus(r3, r0)

    m = 1000
    d = dt/m
    for j in range(m):
        k1 = AP[i]
        k2 = UR[i]
        k3 = DP[i]
        vec_scalar_append(r01, -k1*d, v0)
        vec_scalar_append(r02, -k2*d, v0)
        vec_scalar_append(r03, -k3*d, v0)
        vec_scalar_append(r01, k1*d, v1)
        vec_scalar_append(r02, k2*d, v2)
        vec_scalar_append(r03, k3*d, v3)

        g0, g1, g2 = dtri_force(r0, r1, r2)
        vec_scalar_append(g0, K*d,   v0)
        vec_scalar_append(g1, K*d,   v1)
        vec_scalar_append(g2, K*d,   v2)

        g0, g3, g1 = dtri_force(r0, r3, r1)
        vec_scalar_append(g0, K*d,   v0)
        vec_scalar_append(g3, K*d,   v3)
        vec_scalar_append(g1, K*d,   v1)

        g0, g3, g2 = dtri_force(r0, r3, r2)
        vec_scalar_append(g0, K*d,   v0)
        vec_scalar_append(g3, K*d,   v3)
        vec_scalar_append(g2, K*d,   v2)

        vec_scalar_append(v0, d, r0)
        vec_scalar_append(v1, d, r1)
        vec_scalar_append(v2, d, r2)
        vec_scalar_append(v3, d, r3)

    print(vec_dot(vec_minus(r0, r1), vec_minus(r0, r1)))        
    print(vec_dot(vec_minus(r0, r1), vec_minus(r0, r2)))
