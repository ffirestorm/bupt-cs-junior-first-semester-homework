class Vars:
    def __init__(self) -> None:
        pass
    
    # 环境变量有 用户名，用户密码，用户的状态
    def __init__(self, user_name, user_pwd, order_list, current_state=None):
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.order_list = order_list
        self.current_state = current_state

    def add_order(self, order):
        self.order_list.append(order)
    
    def get_order_list(self):
        return self.order_list
    
    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state

    def get_user_name(self):
        return self.user_name
    
    def get_password(self):
        return self.user_pwd
