import numpy as np
import random as rnd


def project_linear(v,z):
    """
    Projecting vector of data on l1-ball by linear time
    :param v: vector of data
    :param z: scalar that represents constraint for norm
    :return: projected vector
    """
    N = len(v)
    v_abs = np.array([abs(v[i]) for i in range(N)])
    v_norm = v_abs.sum()
    """Taking care of case when ||v||<=z -> w=v"""
    if v_norm <= z:
        return v
    w = np.zeros(N)
    U = range(N)
    s = 0
    rho = 0
    iter = 0
    while len(U) > 0:
        iter += 1
        lenU = len(U)
        i = 0
        j = 0
        G = [-1] * N
        L = [-1] * N
        k = U[rnd.randint(0, lenU - 1)]
        ds = 0
        for m in U:
            if m == k:
                ds += v_abs[m]
                continue
            if v_abs[m] >= v_abs[k]:
                G[i] = m
                ds += v_abs[m]
                i += 1
            else:
                L[j] = m
                j += 1
        drho = i + 1
        if (s + ds) - (rho + drho) * v_abs[k] < z:
            s += ds
            rho += drho
            U = L[:j]
        else:
            U = G[:i]
    theta = (s - z) / rho
    for i in range(N):
        w[i] = np.sign(v[i]) * max(v_abs[i] - theta, 0)
    print('Iter',iter)
    return w