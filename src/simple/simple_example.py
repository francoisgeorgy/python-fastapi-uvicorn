import threading
import time
from fastapi import FastAPI
import uvicorn

from src.utils import get_cube_ip

app = FastAPI()

# Shared counter and lock
counter = 0
counter_lock = threading.Lock()


@app.get("/increment")
async def increment():
    global counter
    with counter_lock:
        counter += 1
    return {"counter": counter}


@app.get("/value")
async def value():
    global counter
    with counter_lock:
        current_value = counter
    return {"counter": current_value}


def run_server():
    host_ip = get_cube_ip()
    uvicorn.run(app, host=f'{host_ip}', port=5042)


def main_loop():
    global counter
    while True:
        with counter_lock:
            print("Counter:", counter)
        time.sleep(1)  # 100 ms


# Start the web server in a separate thread
thread = threading.Thread(target=run_server, daemon=True)
thread.start()

# Start the main loop
main_loop()
