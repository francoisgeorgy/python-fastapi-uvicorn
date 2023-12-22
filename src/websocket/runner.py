import json
import sys
from fastapi import FastAPI, WebSocket
import asyncio
import uvicorn
from utils import get_host_ip
from Application import ThreadedApplication, valid_commands

app = FastAPI()

# Active WebSocket connections set
active_connections = set()


def broadcast_message(message):
    """broadcast messages to all WebSocket connections
    """
    print("broadcast_message", message)
    for connection in active_connections:
        asyncio.run(connection.send_json({"message": message}))


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
            # Handle incoming message
            m = json.loads(message)
            print("    app: received text", message, m)
            if m['command'] in valid_commands:
                app_instance.enqueue_command(m['command'])
            else:
                print("    app: invalid command", m['command'])
    except Exception as e:
        # https://www.rfc-editor.org/rfc/rfc6455#section-7.4.1
        # https://github.com/javaee/websocket-spec/blob/master/api/client/src/main/java/javax/websocket/CloseReason.java
        print("websocket_endpoint Exception", e)
    finally:
        active_connections.remove(websocket)
    # In a FastAPI WebSocket endpoint, you typically don't need to explicitly call await websocket.close() at the end
    # of the function. FastAPI handles the closing of the WebSocket connection automatically when the client disconnects
    # or when the endpoint function exits.
    print("exit websocket_endpoint")


def signal_handler(sig, frame):
    print("Signal received, shutting down")
    app_instance.stop()
    # Any other cleanup
    sys.exit(0)


if __name__ == "__main__":

    # Create an instance of ThreadedMyApplication with the broadcast_message function
    app_instance = ThreadedApplication(message_callback=broadcast_message)

    # signal.signal(signal.SIGINT, signal_handler)

    try:
        host_ip = get_host_ip()
        # https://www.uvicorn.org/settings/
        uvicorn.run(app, host=f'{host_ip}', port=5042)
    except KeyboardInterrupt:
        print("Shutting down gracefully")
        app_instance.stop()

