import socketserver
import json
import re
import time
from scriptParser import ScriptParser
from vars import Vars
from order import Order

# 环境变量
test_order1 = Order(1111111111, "手机", 1688, "2023-11-24")
test_order2 = Order(2222222222, "电脑", 6888, "2023-11-05")
test_order3 = Order(3333333333, "手表", 688, "2023-11-15")
test_order4 = Order(4444444444, "平板电脑", 2688, "2023-11-27")
test_order_list1 = [test_order1, test_order2]
test_user1 = Vars("1", "", test_order_list1)
test_order_list2 = [test_order3, test_order4]
test_user2 = Vars("2", "", test_order_list2)

# 导入用户数据的接口
def load_user_data():
    user_data = {"1":test_user1,"2":test_user2}
    return user_data

# 获取订单的测试桩接口
def get_user_order(username):
    variable = user_data[username]
    orderlist = variable.get_order_list()
    order_inform = "".join(str(order) for order in orderlist)
    return order_inform

# 测试桩
user_data = load_user_data()
chat_robot = ScriptParser("../script_file/chatScript.bot")
sockets_user = {}


class Server(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self):
        print(f"Accepted connection from {self.client_address}")
        while True:
            try:
                data = self.request.recv(1024).decode()
                if not data:
                    break
                print(f"Received message from {self.client_address}: {data}")
                # 处理接收到的消息
                parsed_data = json.loads(data)
                self.handle_message(parsed_data)
            except Exception as e:
                print(f"处理客户端的时候出错：{self.client_address}: {e}")
                del sockets_user[self.request]
                break
        print(f"Connection from {self.client_address} closed.")
    
    # 处理登录请求的消息
    def handle_login(self, recv_data):
        username = recv_data.get("username")
        password = recv_data.get("password")
        print("username: {}".format(username))
        if self.validate_login(username, password) is True:
            # 验证成功
            print("welcome :{}  login".format(recv_data["username"]))
            response = json.dumps({"login":True})
            self.request.send(response.encode())
            first_respo = "欢迎{}，我是您的客服机器人，您可以向我提问。".format(username)
            response = json.dumps({"bot-response":first_respo})
            self.set_init_state(username)
            # 将登录成功的存入到字典中 socket : username
            sockets_user[self.request] = username
            time.sleep(0.1)
        else:
            print("login flase...")
            response = json.dumps({"login":False})
        self.request.send(response.encode())

    # 处理聊天的消息
    def handle_chat(self, recv_data):
        username = sockets_user[self.request]
        data = recv_data["user-message"]
        print("receive from {} : {}".format(username, data))
        bot_resp_list, state = chat_robot.get_response(data, user_data[username].get_state())
        # 将返回的消息队列逐一发送
        for bot_response in bot_resp_list:
            bot_response = self.explain_mark(bot_response, username)
            print(f"bot_response: {bot_response}, state: {state}")
            response = json.dumps({"bot-response":bot_response})
            self.request.send(response.encode())
        # 重置用户状态
        user_data[username].set_state(state)


    # 处理接收到的消息
    def handle_message(self, data):
        recv_data = data
        message_type = recv_data.get("type")
        # 判断消息类型
        if message_type == "login":
            self.handle_login(recv_data)
        
        elif message_type == "chat":
            self.handle_chat(recv_data)

    # 验证登录能否成功
    def validate_login(self, username, password):
        print("validating...")
        try:
            if username in user_data and user_data[username].get_password() == password:
                return True 
        except Exception as e:
            print(f"处理客户端的时候出错：{self.client_address}: {e}")
        return False
    

    # 设置登录的用户初始状态
    def set_init_state(self, username):
        if chat_robot.get_entry() is None:
            user_data[username].set_state("默认")
            print("set state None")
        else:
            user_data[username].set_state(chat_robot.get_entry())
            print("entry not none")


    # 如果回应信息里有占位符，则要将占位符转换成相应字符串
    def explain_mark(self, response, username):
        username_pattern = re.compile(r'\$username')
        order_pattern = re.compile(r'\$order')
        username_match = username_pattern.search(response)
        order_match = order_pattern.search(response)
        if username_match:
            response = response.replace('$username', username)
        if order_match:
            order_str = get_user_order(username)
            response = response.replace('$order', order_str)
        return response
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8888

    server = socketserver.ThreadingTCPServer((HOST, PORT), Server)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down.")
        server.shutdown()