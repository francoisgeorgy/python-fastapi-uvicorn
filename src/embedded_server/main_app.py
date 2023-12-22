import threading


class MainApp:
    def __init__(self):
        self.counter = 0
        self.message = "Hello"
        self.lock = threading.Lock()

    def get_data(self):
        with self.lock:
            return {'counter': self.counter, 'message': self.message}

    def increment_counter(self):
        with self.lock:
            self.counter += 1

    def set_message(self, message):
        with self.lock:
            self.message = message
