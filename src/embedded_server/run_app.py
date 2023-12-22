import uvicorn

from src.utils import get_cube_ip
from web_app import app


if __name__ == "__main__":
    # Start the web server in a new thread
    host_ip = get_cube_ip()
    uvicorn.run(app, host=f'{host_ip}', port=5042)

