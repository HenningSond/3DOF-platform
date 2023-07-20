import cvxpy as cp
import numpy as np

# define dimensions
H, n, m = 10, 4, 2

# define variables
U = cp.Variable((m, H), name='U')
S = cp.Variable((n, H+1), name='S')

# define parameters
Q = cp.Parameter((n, n), name='Qsqrt')
R = cp.Parameter((m, m), name='Rsqrt')
A = cp.Parameter((n, n), name='A')
B = cp.Parameter((n, m), name='B')
s_error = cp.Parameter((n, 1), name='s_error')
dt = 0.05


# discrete-time dynamics
Apar = np.array([[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 0.0]])
Bpar = np.array([[0.0, 0.0], [7000.0, 0.0], [0.0, 0.0], [0.0, 7000.0]])
A.value = Apar
B.value = Bpar

# cost
Q.value = np.diag([1.0, 0.1, 1.0, 0.1])
R.value = np.diag([0.0000, 0.0000])

# measurement
s_error.value = np.array([[20], [0], [20], [0]])


cost = 0.0
constr = []
# define objective
for t in range(H):
    #Make the Cost Function in terms of total error from reference point + control angle
    cost += cp.sum_squares(Q@(S[:, t:t+1]))
    cost += cp.sum_squares(R@(U[:, t]))
    #Update position and velocity states for the next timestep
    constr.append(S[:, t+1] == S[:, t] + dt*(A @ S[:, t] + B@U[:, t]))
    #Constrain the control angle in radians
    constr += [U[:, t] <= 0.43]
    constr += [U[:, t] >= -0.43]
constr += [S[:, 0] == s_error[:, 0]]

#Solve the problem based on the optimal trajectory and input angle from the MPC
problem = cp.Problem(cp.Minimize(cost), constr)


val = problem.solve()


print(val)
print(U.value)
from cvxpygen import cpg

cpg.generate_code(problem, code_dir='MPC_code')