#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 08:01:41 2025

@author: junga1
"""

import numpy as np
import matplotlib.pyplot as plt

# Gradient Descent with learning rate 1/t for f(x) = x^4
def gradient_descent_x4(x0, T):
    x_values = []
    t_values = np.arange(1, T+1)
    
    x_t = x0
    for t in t_values:
        gradient = 4 * x_t**3
        eta_t = 1 / t
        x_t = x_t - eta_t * gradient
        x_values.append(x_t)
    
    return t_values, np.array(x_values)

# Run the demo for x0 = 1
T = 3
x0 = 1
t_values, x_values = gradient_descent_x4(x0, T)

# Plot the results
plt.figure(figsize=(8, 5))
plt.plot(t_values, x_values, marker="o", linestyle="-", label="x_t")
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
plt.xlabel("Iteration t")
plt.ylabel("x_t")
plt.title("Divergence of Gradient Descent for f(x) = x^4 with η_t = 1/t")
plt.legend()
plt.grid()
plt.show()
