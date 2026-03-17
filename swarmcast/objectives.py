"""Built-in objective functions for benchmarking."""
import numpy as np

def rastrigin(x: np.ndarray) -> float:
    A = 10
    return A * len(x) + np.sum(x**2 - A * np.cos(2 * np.pi * x))

def rosenbrock(x: np.ndarray) -> float:
    return sum(100 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x)-1))

def ackley(x: np.ndarray) -> float:
    n = len(x)
    return -20 * np.exp(-0.2 * np.sqrt(np.sum(x**2) / n)) - \
           np.exp(np.sum(np.cos(2 * np.pi * x)) / n) + 20 + np.e

def sphere(x: np.ndarray) -> float:
    return np.sum(x**2)

BENCHMARKS = {"rastrigin": rastrigin, "rosenbrock": rosenbrock, "ackley": ackley, "sphere": sphere}
