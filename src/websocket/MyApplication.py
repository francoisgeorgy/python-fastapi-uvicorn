import time
import threading
from queue import Queue

# Set for active WebSocket connections
# active_connections = set()

#
# def broadcast_message(message):
#     print("broadcast_message", message)
#     for connection in active_connections:
#         asyncio.run(connection.send_json({"message": message}))


# def broadcast_progress(progress):
#     broadcast_message(f"{progress}")


class MyApplication:

    def __init__(self, message_callback):
        self.message_callback = message_callback
        self.task_commands = Queue()

    def reset_cube(self):
        print("reset_cube()")
        self.message_callback("cube reset")

    def shuffle_cube(self):
        print("shuffle_cube()")
        self.message_callback("cube shuffled")

    def long_running_task(self, progress_callback=None):
        print("enter long_running_task")
        self.message_callback("long_running_task started")
        try:
            total_steps = 30
            for step in range(total_steps):
                print("long_running_task", step)
                while self.task_commands.qsize() > 0:
                    print("long_running_task task_commands not empty")
                    command = self.task_commands.get()
                    if command == "stop":
                        print("long_running_task STOP requested")
                        self.message_callback("long_running_task stopped")
                        return

                # Simulate task work
                # if self.message_callback:
                progress = (step + 1) / total_steps * 100
                print("long_running_task progress", progress)
                self.message_callback(f"{progress}")
                # Pause to simulate work
                # asyncio.sleep(1)
                time.sleep(1)

            self.message_callback("long_running_task completed")
        finally:
            self.message_callback("ready")
        print("leave long_running_task")


class ThreadedMyApplication(MyApplication):
    def __init__(self, message_callback):
        super().__init__(message_callback)
        self.command_queue = Queue()
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        print("run() starting...")
        while self.running:
            command, args = self.command_queue.get()
            print("run: command {}, args: {}".format(command, args))
            if command == "reset":
                self.reset_cube()
            elif command == "shuffle":
                self.shuffle_cube()
            elif command == "solve":
                print("run: command is SOLVE, starting thread")
                # if self.task_commands.empty():
                threading.Thread(target=self.long_running_task, args=()).start()
            elif command == "stop":
                self.task_commands.put("stop")
            print("run loop completed")

    def enqueue_command(self, command, args=()):
        print("enqueue_command", command)
        self.command_queue.put((command, args))

    def stop(self):
        self.running = False
        self.thread.join()
        # if self.current_task is not None and self.current_task.is_alive():
        #     self.current_task.join()  # Wait for the current task to finish
        # Any other cleanup

# # Create an instance of ThreadedMyApplication with the broadcast_message function
# my_app_instance = ThreadedMyApplication(message_callback=broadcast_message)

#
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     active_connections.add(websocket)
#     my_app_instance.message_callback("ready")
#     try:
#         while True:
#             message = await websocket.receive_text()
#             if message == "start":
#                 my_app_instance.enqueue_command("long_running_task", args=(broadcast_message,))
#             elif message == "stop":
#                 my_app_instance.enqueue_command("stop")
#             # ... handle other messages ...
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         active_connections.remove(websocket)

