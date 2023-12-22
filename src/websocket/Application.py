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


valid_commands = ('reset', 'shuffle', 'solve', 'stop')


class Application:

    def __init__(self, message_callback):
        self.message_callback = message_callback
        self.task_commands = Queue()

    def reset_cube(self):
        print("    Application.reset_cube()")
        self.message_callback("cube reset")

    def shuffle_cube(self):
        print("    Application.shuffle_cube()")
        self.message_callback("cube shuffled")

    def long_running_task(self):
        print("        Application.long_running_task enter")
        self.message_callback("long_running_task started")
        try:
            abort = False
            total_steps = 30
            for step in range(total_steps):
                print("            Application.long_running_task", step)

                while not abort and self.task_commands.qsize() > 0:
                    print("            Application.long_running_task task_commands not empty")
                    command = self.task_commands.get()
                    print("            Application.long_running_task command is", command)
                    if command == "stop":
                        print("                Application.long_running_task STOP requested")
                        self.message_callback("long_running_task stopped")
                        abort = True

                if abort:
                    # Do any cleanup and exit the for loop
                    break

                # Simulate task work
                progress = (step + 1) / total_steps * 100

                print("            Application.long_running_task progress", progress)
                self.message_callback(f"{progress}")

                # Pause to simulate work
                time.sleep(1)

            self.message_callback(f"long_running_task {'completed' if not abort else 'aborted'}")
        finally:
            self.message_callback("ready")
        print("        Application.long_running_task exit")


class ThreadedApplication(Application):

    def __init__(self, message_callback):
        super().__init__(message_callback)
        self.command_queue = Queue()
        self.current_task = None    # to keep track of the long running task
        self.running = True
        # the application starts itself:
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        print("ThreadedApplication.run starting...")
        while self.running:
            command, args = self.command_queue.get()
            print("    ThreadedApplication.run: command={}, args={}".format(command, args))

            if self.current_task is None:
                print("        ThreadedApplication.run: current_task is None")
            elif self.current_task.is_alive():
                print("        ThreadedApplication.run: current_task not None and alive")
            else:
                print("        ThreadedApplication.run: current_task not None and not alive")

            busy = self.current_task is not None and self.current_task.is_alive()

            # if self.current_task is None or not self.current_task.is_alive():
            if busy and command == "stop":
                print("        ThreadedApplication.run: put stop command into task_commands")
                self.task_commands.put("stop")
                # if self.current_task is not None and self.current_task.is_alive():
                #     self.current_task.join()  # Wait for the current task to finish
            elif busy:
                print("        ThreadedApplication.run: busy, command ignored")
            else:
                if command == "reset":
                    self.reset_cube()
                elif command == "shuffle":
                    self.shuffle_cube()
                elif command == "solve":
                    print("        ThreadedApplication.run: start long_running_task thread (1)")
                    self.current_task = threading.Thread(target=self.long_running_task, args=())
                    self.current_task.start()
                    print("        ThreadedApplication.run: start long_running_task thread (2)")
                else:
                    print("        ThreadedApplication.run: invalid command")

            print("    ThreadedApplication.run command handling completed")

    def enqueue_command(self, command, args=()):
        print("        enqueue_command", command)
        self.command_queue.put((command, args))

    def stop(self):
        self.running = False
        self.thread.join()
        if self.current_task is not None and self.current_task.is_alive():
            self.current_task.join()  # Wait for the current task to finish
        # Any other cleanup
