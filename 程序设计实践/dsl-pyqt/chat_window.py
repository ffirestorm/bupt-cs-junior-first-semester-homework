import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QWidget, QHBoxLayout
import json
from client import SocketManager
class ChatWindow(QMainWindow):
    def __init__(self, socket_manager):
        super().__init__()
        self.socket_manager = socket_manager
        self.setWindowTitle('客服机器人')
        self.setGeometry(200, 200, 800, 1000)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.chat_layout = QVBoxLayout()
        self.message_browser = QTextBrowser()
        self.chat_layout.addWidget(self.message_browser)

        # 输入栏和发送按钮用水平布局
        self.input_layout = QHBoxLayout()  
        self.input_edit = QLineEdit()

        # 设置输入框高度和字体大小
        self.input_edit.setStyleSheet("height: 40px; font-size: 25px;")  
        self.input_layout.addWidget(self.input_edit)

        self.send_button = QPushButton('发送')
        self.send_button.setStyleSheet("height: 40px;")  
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        self.chat_layout.addLayout(self.input_layout)

        self.central_widget.setLayout(self.chat_layout)

        # 设置文本框字体大小
        self.message_browser.setStyleSheet("font-size: 25px;") 
        self.socket_manager.set_message_received_callback(self.recv_message)
        self.input_edit.returnPressed.connect(self.send_message)

    # 展示用户信息
    def display_user_message(self, message):
        self.message_browser.append(f'<div style="margin-bottom: 10px;"><span style="display: inline-block; background-color: #4CAF50; color: white; padding: 10px; border-radius: 10px;"> {message}</span></div>')

    # 展示客服信息
    def display_server_message(self, message):
        self.message_browser.append(f'<span style="background-color: #dcdcdc; color: black;"> {message}</span>')

    def send_message(self):
        # 获取输入栏内容
        message = self.input_edit.text()
        if message:    
            data = {
                "type":"chat",
                "user-message":message
            }
            self.socket_manager.send_message(json.dumps(data))
            self.display_user_message(message)
            # 清空输入栏
            self.input_edit.clear()

    def recv_message(self, message):
        parsed_data = json.loads(message)
        message = parsed_data.get("bot-response")
        self.display_server_message(message)

def main():
    app = QApplication(sys.argv)

    chat_window = ChatWindow()
    chat_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()