from main_app import MainApp

app_instance = MainApp()


def get_main_app_data():
    return app_instance.get_data()


def increment_main_app_counter():
    app_instance.increment_counter()


def set_main_app_message(message):
    app_instance.set_message(message)
