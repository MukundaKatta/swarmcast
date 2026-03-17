"""Visualization utilities for swarm convergence."""
from typing import List

def plot_convergence(history: List[float], title: str = "Convergence"):
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.plot(history, linewidth=2)
        plt.xlabel("Iteration"); plt.ylabel("Best Score")
        plt.title(title); plt.grid(True, alpha=0.3)
        plt.yscale("log"); plt.tight_layout(); plt.show()
    except ImportError:
        print("Install matplotlib for visualization")
