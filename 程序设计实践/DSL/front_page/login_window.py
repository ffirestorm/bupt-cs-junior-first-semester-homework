import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout, QPushButton, QVBoxLayout, QMessageBox
from chat_window import ChatWindow
import json
from client import SocketManager
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.chat_window = None 
        self.socket_manager = SocketManager()
        self.socket_manager.connect_to_server("localhost", 8888)

        self.setWindowTitle('Login')

        self.setGeometry(200, 200, 500, 350)
        self.title = QLabel('登录')
        self.username_label = QLabel('用户名:')
        self.username_edit = QLineEdit()

        self.password_label = QLabel('密码  :')
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('登录')
        self.login_button.clicked.connect(self.on_login_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_edit)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_edit)
        layout.addSpacing(40)
        layout.addLayout(username_layout)
        layout.addSpacing(40)
        layout.addLayout(password_layout)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 40px;
                qproperty-alignment: AlignCenter; /* 让 QLabel 居中 */
            }
        """)
        self.username_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                height: 40px; /* 设置高度 */
            }
        """)
        self.username_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px; /* 增加内边距 */
                font-size: 30px;
                height: 30px; /* 设置高度 */
            }
        """)
        self.password_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                height: 40px; /* 设置高度 */
            }
        """)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px; /* 增加内边距 */
                font-size: 30px;
                height: 30px; /* 设置高度 */
            }
        """)
        self.login_button.setStyleSheet("""
            padding: 10px;
                font-size: 30px;
                height: 30px; 
                width: 60px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
        """)
        self.socket_manager.set_message_received_callback(self.recv_message)


    def on_login_clicked(self):
        # 在这里可以添加登录验证逻辑
        # 示例中假设用户名为'user'，密码为'pass'
        username = self.username_edit.text()
        password = self.password_edit.text()
        data = {
            "type":"login",
            "username":username,
            "password":password
        }
        self.socket_manager.send_message(json.dumps(data))
        self.password_edit.clear()
        

    def recv_message(self, message):
        print("recv:"+message)
        parsed_data = json.loads(message)
        success = parsed_data.get("login")
        if success is True:
            self.chat_window = ChatWindow(self.socket_manager)
            self.hide()
            self.login_button.setEnabled(False)
            self.chat_window.show()
        elif success is False:
            QMessageBox.critical(self, "登录失败", "请检查您的用户名或密码")
            self.password_edit.clear()
            self.username_edit.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.on_login_clicked()

def main():
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()