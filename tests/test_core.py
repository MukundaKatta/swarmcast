from src.core import SwarmEngine
def test_init(): assert SwarmEngine().get_stats()["ops"] == 0
def test_op(): c = SwarmEngine(); c.optimize(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = SwarmEngine(); [c.optimize() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = SwarmEngine(); c.optimize(); c.reset(); assert c.get_stats()["ops"] == 0
