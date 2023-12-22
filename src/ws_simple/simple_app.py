from fastapi import FastAPI, WebSocket
import asyncio
import uvicorn
from websockets.exceptions import ConnectionClosedOK

from src.utils import get_cube_ip

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        for progress in range(10):
            await asyncio.sleep(0.5)
            await websocket.send_json({"progress": progress})
    except ConnectionClosedOK:
        print("WebSocket connection closed normally")
    finally:
        await websocket.close()

if __name__ == "__main__":
    host_ip = get_cube_ip()
    uvicorn.run(app, host=f'{host_ip}', port=5042)
