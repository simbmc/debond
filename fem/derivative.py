'''
Created on 21.09.2016

@author: Yingxiong
'''
import numpy as np


def derivative(f, x, dx):
    return (f(x + dx) - f(x)) / dx


def f(x):
    return x ** 2

print derivative(f, np.array([0, 1, 2, 4]), 1e-8)
