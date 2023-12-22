import threading
import time

from fastapi import FastAPI, WebSocket
import asyncio

from src.utils import get_cube_ip


class MyApplication:
    def __init__(self):
        self.shared_data = "Initial Value"

    def long_running_task(self, progress_callback=None):
        total_steps = 10
        for step in range(total_steps):
            # Simulate a long-running task
            time.sleep(1)  # or your actual task logic
            # Update shared data or perform other operations
            # Send progress update
            if progress_callback:
                progress = (step + 1) / total_steps * 100
                progress_callback(f"{progress}")


app = FastAPI()
my_app_instance = MyApplication()
# Dictionary to store active WebSocket connections
active_connections = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket
    try:
        while True:
            await websocket.receive_text()  # Keep the connection open
    except Exception as e:
        pass
    finally:
        del active_connections[client_id]  # Clean up when done


@app.get("/start-task/{client_id}")
def start_task(client_id: str):
    if client_id in active_connections:
        # progress_callback = lambda progress: asyncio.run(
        #     active_connections[client_id].send_json({"progress": progress}))

        def progress_callback(progress):
            asyncio.run(active_connections[client_id].send_json({"message": progress}))

        threading.Thread(target=my_app_instance.long_running_task, args=(progress_callback,)).start()
        return {"message": "Task started"}
    else:
        return {"error": "Client not connected"}


import uvicorn

if __name__ == "__main__":
    # Import string "app" must be in format "<module>:<attribute>".
    host_ip = get_cube_ip()
    uvicorn.run("app_long_task_client_id:app", host=f'{host_ip}', port=5042, reload=True)

