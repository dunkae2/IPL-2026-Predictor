import sys
import threading
import schedule
import time
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from api.main import app

def run_nightly_pipeline():
    from pipeline.run_pipeline import run_pipeline
    print("[scheduler] Running nightly pipeline...")
    run_pipeline()
    from api.main import reload_models
    reload_models()
    print("[scheduler] Pipeline complete, models reloaded.")

def start_scheduler():
    schedule.every().day.at("00:00").do(run_nightly_pipeline)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    print("[scheduler] Nightly pipeline scheduled at midnight.")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)