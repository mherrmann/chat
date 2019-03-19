from fbs_runtime.application_context import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import QSound
from requests import Session
from threading import Thread
from time import sleep

import sys

name = 'Michael' # Enter your name here!
chat_url = 'https://build-system.fman.io/chat'
server = Session()

class AppContext(ApplicationContext):
    def run(self):
        self.window.show()
        self.timer.start(1000)
        self.thread.start()
        return self.app.exec_()
    @cached_property
    def window(self):
        result = QWidget()
        result.setLayout(self.layout)
        result.setWindowTitle('Chat')
        return result
    @cached_property
    def layout(self):
        result = QVBoxLayout()
        result.addWidget(self.text_area)
        result.addWidget(self.message)
        return result
    @cached_property
    def text_area(self):
        result = QTextEdit()
        result.setFocusPolicy(Qt.NoFocus)
        return result
    @cached_property
    def message(self):
        result = QLineEdit()
        result.returnPressed.connect(self._send_message)
        return result
    def _send_message(self):
        data = {'name': name, 'message': self.message.text()}
        server.post(chat_url, data)
        self.message.clear()
    @cached_property
    def timer(self):
        result = QTimer()
        result.timeout.connect(self._display_new_messages)
        return result
    def _display_new_messages(self):
        if self.new_messages:
            QSound.play(self.get_resource('Alert.wav'))
        while self.new_messages:
            self.text_area.append(self.new_messages.pop(0))
    @cached_property
    def thread(self):
        return Thread(target=self._fetch_new_messages, daemon=True)
    def _fetch_new_messages(self):
        while True:
            try:
                response = server.get(chat_url).text
            except:
                pass
            else:
                if response:
                    self.new_messages.append(response)
            sleep(.5)
    @cached_property
    def new_messages(self):
        return []

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)