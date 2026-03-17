"""Swarm-based time series predictor."""
import numpy as np
from typing import List, Optional
from .engine import PSO

class SwarmPredictor:
    """Use PSO to fit and predict time series data."""
    
    def __init__(self, lookback: int = 10, n_harmonics: int = 5):
        self.lookback = lookback
        self.n_harmonics = n_harmonics
        self.params: Optional[np.ndarray] = None
    
    def _model(self, params: np.ndarray, t: np.ndarray) -> np.ndarray:
        result = params[0] + params[1] * t
        for i in range(self.n_harmonics):
            idx = 2 + i * 3
            amp, freq, phase = params[idx], params[idx+1], params[idx+2]
            result += amp * np.sin(2 * np.pi * freq * t + phase)
        return result
    
    def fit(self, data: List[float], n_particles: int = 100, max_iter: int = 300):
        y = np.array(data)
        t = np.arange(len(y), dtype=float)
        n_params = 2 + self.n_harmonics * 3
        bounds = [(-10, 10), (-1, 1)] + [(-5, 5), (0, 2), (0, 2*np.pi)] * self.n_harmonics
        
        def objective(params):
            pred = self._model(params, t)
            return np.mean((pred - y) ** 2)
        
        pso = PSO(objective, bounds, n_particles=n_particles)
        self.params, _ = pso.optimize(max_iter=max_iter)
        return self
    
    def predict(self, steps: int) -> np.ndarray:
        if self.params is None:
            raise RuntimeError("Call fit() first")
        t_future = np.arange(steps, dtype=float) + self.lookback
        return self._model(self.params, t_future)
