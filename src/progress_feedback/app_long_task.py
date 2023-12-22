import json
import threading
import time

from fastapi import FastAPI, WebSocket
import uvicorn
import asyncio
from queue import Queue

from src.utils import get_cube_ip


# https://chat.openai.com/g/g-8iui73B2J-eliza/c/10a8a294-2379-4a70-9897-f2a85354d5d0

def broadcast_message(message):
    for connection in active_connections:
        # asyncio.run(connection.send_text(message))
        asyncio.run(connection.send_json({"message": message}))


def broadcast_progress(progress):
    broadcast_message(f"{progress}")


class MyApplication:
    def __init__(self, message_callback):
        self.task_running = False
        self.task_commands = Queue()
        self.message_callback = message_callback

    def long_running_task(self, progress_callback=None):
        self.message_callback("long running task starting")
        self.task_running = True
        try:
            total_steps = 100
            for step in range(total_steps):
                print("long_running_task", step)
                # Check for new commands
                if not self.task_commands.empty():
                    command = self.task_commands.get()
                    print("long_running_task: received command", command)
                    if command == "stop":
                        # Handle stop command
                        broadcast_message("task stopped")
                        break
                # Your task logic here
                time.sleep(1)  # or your actual task logic

                # Send progress update
                if progress_callback:
                    progress = (step + 1) / total_steps * 100
                    progress_callback(f"{progress}")
            self.message_callback("long running task completed")
        finally:
            self.task_running = False
            self.message_callback("long running task exit")


app = FastAPI()
my_app_instance = MyApplication(message_callback=broadcast_message)
# Set for active WebSocket connections
active_connections = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        # The primary function of this loop is to keep the WebSocket connection open. Without this loop, the connection
        # would close immediately after being established. The await websocket.receive_text() call waits for a message
        # from the client, keeping the connection alive.
        while True:
            message = await websocket.receive_text()
            # Handle incoming message (e.g., stop command)
            m = json.loads(message)
            print("received texte", message, m)
            if m['command'] == "start":
                # if not my_app_instance.task_running:
                #     threading.Thread(target=my_app_instance.long_running_task, args=(broadcast_progress,)).start()
                start_task()
            elif m['command'] == "stop":
                my_app_instance.task_commands.put("stop")
    except Exception as e:
        # https://www.rfc-editor.org/rfc/rfc6455#section-7.4.1
        print("websocket_endpoint Exception", e)
        pass
    finally:
        active_connections.remove(websocket)


@app.get("/start")
def start_task():
    if my_app_instance.task_running:
        return {"error": "Task is already running"}
    threading.Thread(target=my_app_instance.long_running_task, args=(broadcast_progress,)).start()
    return {"message": "Task started"}


@app.get("/stop")
def stop_task():
    if not my_app_instance.task_running:
        return {"error": "No task is currently running"}

    my_app_instance.task_commands.put("stop")
    return {"message": "Stopping task"}


if __name__ == "__main__":
    # Import string "app" must be in format "<module>:<attribute>".
    host_ip = get_cube_ip()
    uvicorn.run("app_long_task:app", host=f'{host_ip}', port=5042, reload=True)
