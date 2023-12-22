import threading
import time

from fastapi import FastAPI, WebSocket
import asyncio


# https://chat.openai.com/g/g-8iui73B2J-eliza/c/10a8a294-2379-4a70-9897-f2a85354d5d0

class MyApplication:
    def __init__(self):
        self.shared_data = "Initial Value"

    def long_running_task(self, progress_callback=None):
        total_steps = 100
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
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        active_connections.remove(websocket)


@app.get("/start")
def start_task():
    threading.Thread(target=my_app_instance.long_running_task, args=(broadcast_progress,)).start()
    return {"message": "Task started"}


def broadcast_progress(progress):
    for connection in active_connections:
        asyncio.run(connection.send_json({"message": progress}))


# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await websocket.accept()
#     active_connections[client_id] = websocket
#     try:
#         while True:
#             await websocket.receive_text()  # Keep the connection open
#     except Exception as e:
#         pass
#     finally:
#         del active_connections[client_id]  # Clean up when done
#
#
# @app.get("/start-task/{client_id}")
# def start_task(client_id: str):
#     if client_id in active_connections:
#         # progress_callback = lambda progress: asyncio.run(
#         #     active_connections[client_id].send_json({"progress": progress}))
#         def progress_callback(progress):
#             asyncio.run(active_connections[client_id].send_json({"progress": progress}))
#         threading.Thread(target=my_app_instance.long_running_task, args=(progress_callback,)).start()
#         return {"message": "Task started"}
#     else:
#         return {"error": "Client not connected"}


import uvicorn

if __name__ == "__main__":
    # Import string "app" must be in format "<module>:<attribute>".
    uvicorn.run("app_long_task:app", host="localhost", port=8042, reload=True)

