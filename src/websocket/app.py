import json
import signal
import sys

from fastapi import FastAPI, WebSocket
import asyncio
import uvicorn

from ledcube.core.remote import get_cube_ip
from samples.web_sockets.example1.MyApplication import ThreadedMyApplication

# FastAPI app instance
app = FastAPI()

# Active WebSocket connections set
active_connections = set()


# Signal handler function
def signal_handler(sig, frame):
    print("Signal received, shutting down")
    my_app_instance.stop()
    # Any other cleanup
    sys.exit(0)


# signal.signal(signal.SIGINT, signal_handler)


# Function to broadcast messages to all WebSocket connections
def broadcast_message(message):
    print("broadcast_message", message)
    for connection in active_connections:
        asyncio.run(connection.send_json({"message": message}))


# Function to broadcast progress
# def broadcast_progress(progress):
#     broadcast_message(f"progress: {progress}")


# Create an instance of ThreadedMyApplication with the broadcast_message function
my_app_instance = ThreadedMyApplication(message_callback=broadcast_message)


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("enter websocket_endpoint")
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
            print("ws_rubik: received text", message, m)
            # my_app_instance.task_commands.put(m['command'])
            if m['command'] == "reset":
                # if not my_app_instance.task_running:
                #     threading.Thread(target=my_app_instance.long_running_task, args=(broadcast_progress,)).start()
                # start_auto_solve()
                my_app_instance.enqueue_command("reset")
            elif m['command'] == "shuffle":
                my_app_instance.enqueue_command("shuffle")
            elif m['command'] == "solve":
                my_app_instance.enqueue_command("solve")
            elif m['command'] == "stop":
                my_app_instance.enqueue_command("stop")
    except Exception as e:
        # https://www.rfc-editor.org/rfc/rfc6455#section-7.4.1
        # https://github.com/javaee/websocket-spec/blob/master/api/client/src/main/java/javax/websocket/CloseReason.java
        print("websocket_endpoint Exception", e)
    finally:
        active_connections.remove(websocket)
    print("exit websocket_endpoint")
    # In a FastAPI WebSocket endpoint, you typically don't need to explicitly call await websocket.close() at the end
    # of the function. FastAPI handles the closing of the WebSocket connection automatically when the client disconnects
    # or when the endpoint function exits.



# Function to start the Uvicorn server
# def start():
#     uvicorn.run(app, host="localhost", port=8042)
#
# if __name__ == "__main__":
#     start()

if __name__ == "__main__":
    # https://www.uvicorn.org/settings/
    try:
        host_ip = get_cube_ip()
        uvicorn.run(app, host=f'{host_ip}', port=5042)
    except KeyboardInterrupt:
        print("Shutting down gracefully")
        my_app_instance.stop()

