import re

class ScriptTree:       # 语法树
    def __init__(self) :
        self.states = {}    # 状态及动作树
        self.responses = {} # 各个状态的初始回应
        self.entry = None   # 语法入口
        self.exit = None
        self.wait = {}      # 各个状态的等待时间

    def get_entry(self):
        return self.entry
    
    def add_state(self, name, cases):
        self.states[name] = cases

    def add_init_response(self, name, response):
        self.responses[name] = response
        
    """
        在特定状态下查找单一的回应
        @param state_name 要查找的状态
        @user_input 用户输入
        @return 一个表示回应的字符串和一个转移后的状态名称
    """
    def find_single_resp(self, state_name, user_input):
        state = state_name
        response = None
        cases_dict = self.states[state_name]
        case_keys = list(cases_dict.keys())
        for trigger in case_keys:
            # 正则匹配输入串, 获取触发条件
            pattern = re.compile(trigger)
            if not pattern.search(user_input):
                continue
            # 查看所有的回应动作
            actions = cases_dict[trigger]
            action_keys = list(actions.keys())
            for act_type in action_keys:
                act_result = actions[act_type]
                # 状态转移
                if act_type == "state_transfer":
                    new_state = act_result
                    state = new_state
                elif act_type == "response":
                    response = act_result

        return response, state
    
    
    # 根据状态，输入，在本状态或默认状态下获取回应消息
    def find_response(self, state_name, user_input):
        response, state = self.find_single_resp(state_name, user_input)
        if response is None and state == state_name:
            response, state = self.find_single_resp("默认", user_input)
            if state == "默认":
                state = state_name
        return response, state

    """
        同时对内对外的程序接口，用来从用户输入中提取关键词，并返回相应回答
        @param user_input 用户输入
        @param state_name 要查找回应的状态
        @return response 回应
    """
    def get_response(self ,user_input, state_name, ret_list=[]):   
        response = None
        response, ret_state = self.find_response(state_name, user_input)
        if state_name == ret_state:
            # 状态没改变
            if response is not None:
                ret_list.append(response)
            else:
                ret_list.append("抱歉，我不明白您的意思")
        else:
            # 状态改变
            if response is not None:
                ret_list.append(response)
            ret_list.append(self.responses[ret_state])
        return ret_list, ret_state
                

    