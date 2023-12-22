from fastapi import FastAPI
from interface import get_main_app_data, increment_main_app_counter, set_main_app_message

app = FastAPI()


@app.get("/data")
async def read_data():
    return get_main_app_data()


@app.post("/increment-counter")
async def increment_counter():
    increment_main_app_counter()
    return {"status": "counter incremented"}


@app.post("/set-message")
async def write_message(message: str):
    set_main_app_message(message)
    return {"status": "message set"}
