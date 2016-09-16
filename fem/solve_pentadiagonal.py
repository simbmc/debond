'''
Created on 07.09.2016

@author: Yingxiong
'''
import numpy as np


def solve(n, d, a, b, c, e, y):

    alpha = np.zeros(n - 1)
    beta = np.zeros(n - 2)
    z = np.zeros(n)
    gamma = np.zeros(n - 1)
    mu = np.zeros(n)

    # step 3
    mu[0] = d[0]
    alpha[0] = a[0] / mu[0]
    beta[0] = b[0] / mu[0]
    z[0] = y[0] / mu[0]

    # step 4
    gamma[0] = c[0]
    mu[1] = d[1] - alpha[0] * gamma[0]
    alpha[1] = (a[1] - beta[0] * gamma[0]) / mu[1]
    beta[1] = b[1] / mu[1]
    z[1] = (y[1] - z[0] * gamma[0]) / mu[1]

    # step 5
    for i in np.arange(2, n - 2):
        gamma[i - 1] = c[i - 1] - alpha[i - 2] * e[i - 2]
        mu[i] = d[i] - beta[i - 2] * e[i - 2] - alpha[i - 1] * gamma[i - 1]
        alpha[i] = (a[i] - beta[i - 1] * gamma[i - 1]) / mu[i]
        beta[i] = b[i] / mu[i]
        z[i] = (y[i] - z[i - 2] * e[i - 2] - z[i - 1] * gamma[i - 1]) / mu[i]

    gamma[n - 3] = c[n - 3] - alpha[n - 4] * e[n - 4]
    mu[n - 2] = d[n - 2] - beta[n - 4] * e[n - 4] - alpha[n - 3] * gamma[n - 3]
    alpha[n - 2] = (a[n - 2] - beta[n - 3] * gamma[n - 3]) / mu[n - 2]

    gamma[n - 2] = c[n - 2] - alpha[n - 3] * e[n - 3]
    mu[n - 1] = d[n - 1] - beta[n - 3] * e[n - 3] - alpha[n - 2] * gamma[n - 2]
    z[n - 2] = (y[n - 2] - z[n - 4] * e[n - 4] - z[n - 3]
                * gamma[n - 3]) / mu[n - 2]
    z[n - 1] = (y[n - 1] - z[n - 3] * e[n - 3] - z[n - 2]
                * gamma[n - 2]) / mu[n - 1]

    # step 6
    x = np.zeros(n)
    x[n - 1] = z[n - 1]
    x[n - 2] = z[n - 2] - alpha[n - 2] * x[n - 1]
    for i in np.arange(n - 3, -1, -1):
        x[i] = z[i] - alpha[i] * x[i + 1] - beta[i] * x[i + 2]
    return x
