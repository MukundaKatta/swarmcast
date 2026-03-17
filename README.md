# 🐝 SwarmCast

**Universal Swarm Intelligence Engine — Predict Anything**

SwarmCast provides PSO, ACO, and Bee algorithms for optimization and time-series prediction.

## Install
```bash
pip install -e .
```

## Quick Start
```python
from swarmcast import SwarmEngine
from swarmcast.objectives import rastrigin

pso = SwarmEngine.pso(rastrigin, bounds=[(-5,5)]*10, n_particles=50)
best_pos, best_score = pso.optimize(max_iter=200)

from swarmcast import SwarmPredictor
predictor = SwarmPredictor(n_harmonics=3)
predictor.fit(data)
future = predictor.predict(steps=30)
```

## Algorithms
- **PSO** — Particle Swarm Optimization
- **ACO** — Ant Colony Optimization (TSP)
- **Benchmarks** — Rastrigin, Rosenbrock, Ackley, Sphere

## License
© 2026 Officethree Technologies. All Rights Reserved.
