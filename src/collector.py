import psutil
import json
from datetime import datetime

def collect_metrics():
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "network": psutil.net_io_counters()._asdict()
    }
    return metrics

if __name__ == "__main__":
    data = collect_metrics()
    print(json.dumps(data, indent=2))