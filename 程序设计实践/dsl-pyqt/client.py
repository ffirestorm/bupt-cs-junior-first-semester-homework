import socket
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

class SocketManager(QObject):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.worker_thread = QThread(parent=self)
        self.moveToThread(self.worker_thread)

    def connect_to_server(self, host, port):
        try:
            self.socket.connect((host, port))
            self.connected = True
            self.worker_thread.started.connect(self.receive_messages)
            self.worker_thread.start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    @pyqtSlot()
    def receive_messages(self):
        while self.connected:
            try:
                message = self.socket.recv(1024).decode()
                self.message_received.emit(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.connected = False

    def send_message(self, message):
        try:
            self.socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def close_connection(self):
        self.connected = False
        self.worker_thread.quit()
        self.worker_thread.wait()

    def set_message_received_callback(self, callback):
        self.message_received.connect(callback)