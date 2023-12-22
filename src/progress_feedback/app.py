import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

from src.utils import get_cube_ip

app = FastAPI()
clients = set()
counter = 0


async def broadcast(message):
    for client in clients:
        await client.send_json(message)


async def counter_task():
    global counter
    while True:
        await asyncio.sleep(1)
        counter += 1
        await broadcast({"counter": counter})


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(counter_task())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global counter
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "reset":
                counter = 0
                await broadcast({"counter": counter})
    except WebSocketDisconnect:
        clients.remove(websocket)


if __name__ == "__main__":
    host_ip = get_cube_ip()
    uvicorn.run("app_long_task:app", host=f'{host_ip}', port=5042, reload=True)
