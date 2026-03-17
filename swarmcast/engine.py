"""Core swarm intelligence engine with PSO, ACO, and Bee algorithms."""
import numpy as np
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

@dataclass
class Particle:
    position: np.ndarray
    velocity: np.ndarray
    best_position: np.ndarray = field(default=None)
    best_score: float = float("inf")
    
    def __post_init__(self):
        if self.best_position is None:
            self.best_position = self.position.copy()

class PSO:
    """Particle Swarm Optimization."""
    
    def __init__(self, objective: Callable, bounds: List[Tuple[float, float]],
                 n_particles: int = 50, w: float = 0.7, c1: float = 1.5, c2: float = 1.5):
        self.objective = objective
        self.bounds = np.array(bounds)
        self.n_particles = n_particles
        self.w, self.c1, self.c2 = w, c1, c2
        self.dim = len(bounds)
        self.global_best_position = None
        self.global_best_score = float("inf")
        self.history: List[float] = []
        self.particles = self._init_swarm()
    
    def _init_swarm(self) -> List[Particle]:
        particles = []
        for _ in range(self.n_particles):
            pos = np.random.uniform(self.bounds[:, 0], self.bounds[:, 1])
            vel = np.random.uniform(-1, 1, self.dim) * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1
            p = Particle(position=pos, velocity=vel)
            score = self.objective(pos)
            p.best_score = score
            p.best_position = pos.copy()
            if score < self.global_best_score:
                self.global_best_score = score
                self.global_best_position = pos.copy()
            particles.append(p)
        return particles
    
    def step(self):
        for p in self.particles:
            r1, r2 = np.random.random(self.dim), np.random.random(self.dim)
            p.velocity = (self.w * p.velocity +
                         self.c1 * r1 * (p.best_position - p.position) +
                         self.c2 * r2 * (self.global_best_position - p.position))
            p.position += p.velocity
            p.position = np.clip(p.position, self.bounds[:, 0], self.bounds[:, 1])
            score = self.objective(p.position)
            if score < p.best_score:
                p.best_score = score
                p.best_position = p.position.copy()
            if score < self.global_best_score:
                self.global_best_score = score
                self.global_best_position = p.position.copy()
        self.history.append(self.global_best_score)
    
    def optimize(self, max_iter: int = 200, tol: float = 1e-8) -> Tuple[np.ndarray, float]:
        for i in range(max_iter):
            self.step()
            if i > 10 and abs(self.history[-1] - self.history[-2]) < tol:
                logger.info(f"Converged at iteration {i}")
                break
        return self.global_best_position, self.global_best_score

class ACO:
    """Ant Colony Optimization for combinatorial problems."""
    
    def __init__(self, distances: np.ndarray, n_ants: int = 30,
                 alpha: float = 1.0, beta: float = 2.0, rho: float = 0.5):
        self.distances = distances
        self.n_cities = len(distances)
        self.n_ants = n_ants
        self.alpha, self.beta, self.rho = alpha, beta, rho
        self.pheromones = np.ones_like(distances) / self.n_cities
        self.best_path: Optional[List[int]] = None
        self.best_distance = float("inf")
        self.history: List[float] = []
    
    def _select_next(self, current: int, visited: set) -> int:
        unvisited = [c for c in range(self.n_cities) if c not in visited]
        if not unvisited:
            return -1
        tau = np.array([self.pheromones[current][j] for j in unvisited])
        eta = np.array([1.0 / max(self.distances[current][j], 1e-10) for j in unvisited])
        probs = (tau ** self.alpha) * (eta ** self.beta)
        probs /= probs.sum()
        return np.random.choice(unvisited, p=probs)
    
    def _path_distance(self, path: List[int]) -> float:
        return sum(self.distances[path[i]][path[i+1]] for i in range(len(path)-1)) + \
               self.distances[path[-1]][path[0]]
    
    def optimize(self, max_iter: int = 100) -> Tuple[List[int], float]:
        for _ in range(max_iter):
            all_paths = []
            for _ in range(self.n_ants):
                start = np.random.randint(self.n_cities)
                path, visited = [start], {start}
                for _ in range(self.n_cities - 1):
                    nxt = self._select_next(path[-1], visited)
                    if nxt == -1: break
                    path.append(nxt)
                    visited.add(nxt)
                dist = self._path_distance(path)
                all_paths.append((path, dist))
                if dist < self.best_distance:
                    self.best_distance = dist
                    self.best_path = path[:]
            self.pheromones *= (1 - self.rho)
            for path, dist in all_paths:
                deposit = 1.0 / dist
                for i in range(len(path) - 1):
                    self.pheromones[path[i]][path[i+1]] += deposit
                    self.pheromones[path[i+1]][path[i]] += deposit
            self.history.append(self.best_distance)
        return self.best_path, self.best_distance

class SwarmEngine:
    """Unified interface for swarm intelligence algorithms."""
    
    @staticmethod
    def pso(objective, bounds, **kwargs) -> PSO:
        return PSO(objective, bounds, **kwargs)
    
    @staticmethod
    def aco(distances, **kwargs) -> ACO:
        return ACO(distances, **kwargs)
    
    @staticmethod
    def optimize(objective, bounds, algorithm="pso", **kwargs):
        if algorithm == "pso":
            opt = PSO(objective, bounds, **kwargs)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        return opt.optimize()
