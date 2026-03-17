import numpy as np
from swarmcast.engine import PSO, ACO
from swarmcast.objectives import sphere

def test_pso_sphere():
    pso = PSO(sphere, [(-5,5)]*3, n_particles=30)
    pos, score = pso.optimize(max_iter=100)
    assert score < 0.1

def test_aco():
    d = np.random.rand(5,5)*10; np.fill_diagonal(d,0); d = (d+d.T)/2
    aco = ACO(d, n_ants=10)
    path, dist = aco.optimize(max_iter=50)
    assert len(path) == 5
