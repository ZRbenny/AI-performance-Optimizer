# src/collector.py
import psutil
import time
import json
import os
from datetime import datetime

try:
    import GPUtil
except ImportError:
    GPUtil = None  # GPU support is optional

# File to store history
DATA_FILE = os.path.join("data", "metrics_history.json")


def collect_metrics():
    metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": dict(psutil.virtual_memory()._asdict()),
        "disk": dict(psutil.disk_usage('/')._asdict()),
        "network": dict(psutil.net_io_counters()._asdict()),
        "uptime": int(time.time() - psutil.boot_time()),  # seconds
    }

    # Disk I/O
    disk_io = psutil.disk_io_counters()
    metrics["disk_io"] = {
        "read_mb": disk_io.read_bytes // (1024 ** 2),
        "write_mb": disk_io.write_bytes // (1024 ** 2),
    }

    # Top processes
    processes = []
    for p in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_procs = sorted(processes, key=lambda p: p["cpu_percent"], reverse=True)[:5]
    metrics["top_processes"] = top_procs

    # GPU (if available)
    if GPUtil:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            metrics["gpu"] = {
                "name": gpu.name,
                "load": gpu.load * 100,
                "memory_used": gpu.memoryUsed,
                "memory_total": gpu.memoryTotal,
            }

    return metrics


def save_metrics(metrics, silent=False):
    """Save metrics to history file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    metrics["timestamp"] = datetime.now().isoformat()
    history.append(metrics)

    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=4)

    if not silent:
        print(f"[INFO] Metrics saved to {DATA_FILE}")


def load_history(limit=20):
    """Load last N history entries."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            return []

    return history[-limit:]
