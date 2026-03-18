"""Integration tests for Swarmcast."""
from src.core import Swarmcast

class TestSwarmcast:
    def setup_method(self):
        self.c = Swarmcast()
    def test_10_ops(self):
        for i in range(10): self.c.optimize(i=i)
        assert self.c.get_stats()["ops"] == 10
    def test_service_name(self):
        assert self.c.optimize()["service"] == "swarmcast"
    def test_different_inputs(self):
        self.c.optimize(type="a"); self.c.optimize(type="b")
        assert self.c.get_stats()["ops"] == 2
    def test_config(self):
        c = Swarmcast(config={"debug": True})
        assert c.config["debug"] is True
    def test_empty_call(self):
        assert self.c.optimize()["ok"] is True
    def test_large_batch(self):
        for _ in range(100): self.c.optimize()
        assert self.c.get_stats()["ops"] == 100
