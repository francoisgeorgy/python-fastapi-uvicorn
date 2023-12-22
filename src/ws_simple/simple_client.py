import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    print(message)
                except websockets.exceptions.ConnectionClosed as e:
                    if e.code == 1000:
                        print("WebSocket connection closed normally")
                    else:
                        print(f"WebSocket connection closed with error: {e.code}")
                    break
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")

asyncio.run(test_websocket())
