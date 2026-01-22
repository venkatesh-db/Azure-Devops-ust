import json
import sys

def optimize_devops(config_file):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        
        # Example logic for DevOps optimization
        print("Optimizing DevOps tasks...")
        for task in config.get("tasks", []):
            print(f"Task {task.get('name', 'Unknown')}: Optimization applied")
    except Exception as e:
        print(f"Error optimizing DevOps tasks: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--config":
        print("Usage: python ml_devops_optimization.py --config <config_file>")
        sys.exit(1)

    optimize_devops(sys.argv[2])