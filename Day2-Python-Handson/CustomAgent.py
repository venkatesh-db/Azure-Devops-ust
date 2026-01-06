# custom_agent.py
import psutil
import time
import subprocess
import logging

CPU_LIMIT = 80
CHECK_INTERVAL = 10  # seconds
PROCESS_NAME = "vlc"

logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

logging.info("Custom Agent started. Monitoring CPU usage and process status.")
print("Custom Agent started. Monitoring CPU usage and process status.")

def is_process_running(name):
    for p in psutil.process_iter(['name']):
        if name.lower() in (p.info['name'] or "").lower():
            return True
    logging.info(f"Process '{name}' not found.")
    print(f"Process '{name}' not found.")
    return False

def restart_process():
    logging.warning("Restarting VLC due to high CPU")
    subprocess.run(["pkill", "-f", PROCESS_NAME])
    subprocess.Popen([PROCESS_NAME])

while True:
    cpu = psutil.cpu_percent(interval=3)
    logging.info(f"CPU usage: {cpu}%")
    print(f"CPU usage: {cpu}%")

    if cpu > CPU_LIMIT and is_process_running(PROCESS_NAME):
        restart_process()

    time.sleep(CHECK_INTERVAL)
