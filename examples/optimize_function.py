"""Example: optimize benchmark functions with PSO."""
from swarmcast import SwarmEngine
from swarmcast.objectives import rastrigin, BENCHMARKS

for name, fn in BENCHMARKS.items():
    bounds = [(-5, 5)] * 5
    pso = SwarmEngine.pso(fn, bounds, n_particles=60)
    best_pos, best_score = pso.optimize(max_iter=200)
    print(f"{name:12s} | best={best_score:.6f} | pos={best_pos[:3].round(4)}...")
