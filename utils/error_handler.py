#error_handler.py
from datetime import datetime
import traceback

def log_error(tag, e):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"[{now}] [{tag}] {str(e)}\n")
        f.write(traceback.format_exc() + "\n")