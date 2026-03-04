import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --------------------------------------------------
# 1️⃣ Control Points (3D)
# --------------------------------------------------

P = np.array([
    [0, 0, 0],
    [1, 2, 1],
    [3, 3, 2],
    [4, 0, 3],
    [6, 2, 2],
    [8, 1, 4]
])

n = len(P)
k = 3  # cubic degree

# --------------------------------------------------
# 2️⃣ Open Uniform Knot Vector
# --------------------------------------------------
# length = n + k + 1

def generate_open_uniform_knots(n, k):
    knots = np.zeros(n + k + 1)
    
    # first k+1 knots = 0
    knots[:k+1] = 0
    
    # last k+1 knots = 1
    knots[-(k+1):] = 1
    
    # internal knots uniformly spaced
    if n - k - 1 > 0:
        internal = np.linspace(0, 1, n - k + 1)[1:-1]
        knots[k+1:n] = internal
    
    return knots

T = generate_open_uniform_knots(n, k)

# --------------------------------------------------
# 3️⃣ Cox-de Boor Recursive Basis Function
# --------------------------------------------------

def N(i, k, t, T):
    if k == 0:
        if T[i] <= t < T[i+1]:
            return 1.0
        return 0.0

    denom1 = T[i+k] - T[i]
    denom2 = T[i+k+1] - T[i+1]

    term1 = 0
    term2 = 0

    if denom1 != 0:
        term1 = (t - T[i]) / denom1 * N(i, k-1, t, T)

    if denom2 != 0:
        term2 = (T[i+k+1] - t) / denom2 * N(i+1, k-1, t, T)

    return term1 + term2

# --------------------------------------------------
# 4️⃣ Compute B-Spline Curve
# --------------------------------------------------

t_values = np.linspace(T[k], T[n], 300)
curve = []

for t in t_values:
    point = np.zeros(3)
    for i in range(n):
        point += N(i, k, t, T) * P[i]
    curve.append(point)

curve = np.array(curve)

# --------------------------------------------------
# 5️⃣ 3D Visualization
# --------------------------------------------------

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Control polygon
ax.plot(P[:,0], P[:,1], P[:,2], 'ro--', label="Control Polygon")

# B-Spline curve
ax.plot(curve[:,0], curve[:,1], curve[:,2], 'b', linewidth=2, label="Cubic B-Spline")

ax.set_title("3D Cubic B-Spline")
ax.legend()

plt.show()