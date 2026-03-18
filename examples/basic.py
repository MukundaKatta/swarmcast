"""Basic usage example for swarmcast."""
from src.core import Swarmcast

def main():
    instance = Swarmcast(config={"verbose": True})

    print("=== swarmcast Example ===\n")

    # Run primary operation
    result = instance.optimize(input="example data", mode="demo")
    print(f"Result: {result}")

    # Run multiple operations
    ops = ["optimize", "predict", "evolve_population]
    for op in ops:
        r = getattr(instance, op)(source="example")
        print(f"  {op}: {"✓" if r.get("ok") else "✗"}")

    # Check stats
    print(f"\nStats: {instance.get_stats()}")

if __name__ == "__main__":
    main()
