import threading
from pynput import mouse

__author__ = "Harvey Sama"
__date__ = '$17 June 2017 23:35:'


class MouseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mouse_listener = None
        self.cKeyboard = None

    def setClafricaController(self, cKeyboard):
        self.cKeyboard = cKeyboard

    def run(self):
        self.resume()

    def resume(self):

        with mouse.Listener(
                on_click=self.on_click
        ) as self.mouse_listener:
            self.mouse_listener.join()

    def pause(self):
        self.mouse_listener.stop()

    def on_click(self, x, y, button, pressed):
        self.cKeyboard.curr_input = []
