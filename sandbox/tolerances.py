# %%
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# %%
expr = sp.parse_expr("(2 * t * (3 * p**2 - 6 * p * r + 3 * r**2 + t**2)) / 3 + 10/t")
# %%
r = sp.Symbol("r")
p = sp.Symbol("p")
t = sp.Symbol("t")

# %%
expr = expr.subs({r: 5})
expr
# %%
# plot our expression for 0 < p < 10, 0 < t < 1
p_vals = np.linspace(0.1, 10, 100)
t_vals = np.linspace(0.1, 1, 100)
expr_vals = np.zeros((100, 100))
for i, p_val in enumerate(p_vals):
    for j, t_val in enumerate(t_vals):
        expr_vals[i, j] = expr.subs({p: p_val, t: t_val})

plt.imshow(expr_vals, extent=[0, 1, 0, 10], origin="lower")
plt.colorbar()
plt.xlabel("t")
plt.ylabel("p")
plt.show()

# %%
# convert our expression to a function
def unpack_ax0(func):
    def _wrapper(x):
        return func(*x)
    return _wrapper

expr_func = unpack_ax0(sp.lambdify((p, t), expr, "numpy"))


# %%
minimize(expr_func, x0=[0, 0.1], bounds=[(0, 10), (0.1, 10)])

# %%
