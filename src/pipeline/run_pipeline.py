import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
PYTHON = sys.executable

def run_pipeline():
    steps = [
        ROOT / "src" / "data" / "auto_update.py",
        ROOT / "src" / "run_preprocessing.py",
        ROOT / "src" / "features" / "build_features.py",
        ROOT / "src" / "modeling" / "train.py",
    ]
    for step in steps:
        print(f"[pipeline] Running {step.name}...")
        result = subprocess.run([PYTHON, str(step)], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[pipeline] FAILED: {result.stderr}")
            return False
        print(result.stdout)
    print("[pipeline] Done.")
    return True

if __name__ == "__main__":
    run_pipeline()