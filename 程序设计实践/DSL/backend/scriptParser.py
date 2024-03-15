import re
from scriptTree  import ScriptTree

# 跳过注释
def strip_annotate(line):
    return re.sub(r'#.*', '', line)

class ScriptError(Exception):
    def __init__(self, message="脚本文件有错"):
        self.message = message
        super().__init__(self.message)

class ScriptParser:
    def __init__(self, script_path):
        with open(script_path, 'r', encoding='utf-8') as file:
            self.script = file.read()
        self.script_tree = ScriptTree()
        self.parser_file()


    def get_entry(self):
        return self.script_tree.get_entry()
    
    # 从语法树获取回应
    def get_response(self, user_input, state_name):
        return self.script_tree.get_response(user_input, state_name, [])
    
    # 匹配entry,将entry加入到语法树中
    def parser_entry(self, line, row):
        pattern = r'entry "(.*?)"'
        match = re.match(pattern, line)
        if match:
            if self.script_tree.entry is not None:
                raise ScriptError("请检查脚本文件第{}行，一个脚本只能有一个entry".format(row))
            entry = match.group(1)
            self.script_tree.entry = entry
        else:
            raise ScriptError("请检查脚本文件的第{}行，entry后面请跟一个状态".format(row))
    
    # 匹配exit，将exit加入到语法树中
    def parser_exit(self, line, row):
        pattern = r'exit "(.*?)"'
        match = re.match(pattern, line)
        if match:
            if self.script_tree.exit is not None:
                raise ScriptError("请检查脚本文件第{}行，一个脚本只能有一个exit".format(row))
            exit = match.group(1)
            self.script_tree.exit = exit
        else:
            raise ScriptError("请检查脚本文件的第{}行，exit后面请跟一个状态".format(row))

    # 获取等待时间，加入到状态-时间字典中
    def parser_wait(self, line, current_state, row):
        pattern = r"wait (\d+)"
        match = re.match(pattern, line)
        if match:
            wait_time = match.group(1)
            if current_state in self.script_tree.wait and self.script_tree.wait[current_state] is not None:
                raise ScriptError("请检查脚本文件的第{}行, 一个状态只能有一个等待时间".format(row))
            self.script_tree.wait[current_state] = wait_time
        else:
            raise ScriptError("请检查脚本文件的第{}行, wait后只能跟等待时间, 单位为秒".format(row))        


    """
        当行开头为when时, 将匹配添加一个condition字典
        @param line 
        @param row 脚本的第几行
        @return condition 返回一个字典，类似
            {"trigger1":[{"act_type1":"act_result1"},{"act_type2":"act_result2"}]}
    """
    def parser_when(self, line, row):
        # 定义正则表达式模式
        pattern = r'when "(.*?)"(?: state_transfer "(.*?)")?(?: response "(.*?)")?'
        # 使用正则表达式匹配
        match = re.match(pattern, line)
        condition = {}
        if match:
            # 提取匹配到的信息
            trigger = match.group(1)
            state_trans = match.group(2) if match.group(2) else None
            response = match.group(3) if match.group(3) else None
            if state_trans is not None:
                act_type = "state_transfer"
                act_result = state_trans
                condition[act_type] = act_result
            if response is not None:
                act_type = "response"
                act_result = response
                condition[act_type] = act_result
        else:
            raise ScriptError("请检查脚本文件的第{}行, 有语法错误".format(row))

        return trigger,condition
    

    def parser_response(self, current_state, line, row):
        pattern = r'response "(.*?)"'
        match = re.match(pattern, line)
        if match:
            response = match.group(1)
            if self.script_tree.responses[current_state] is not None:
                raise ScriptError("脚本文件第{}行,状态的初始response只能有一个".format(row))
            self.script_tree.add_init_response(current_state, response)
        else:
            raise ScriptError("脚本文件第{}行,状态的默认response后只能跟一个回应".format(row))

    
    # 遇到state，将上一个状态的状态树加入语法树中，并初始化新的状态树
    def parser_state(self, current_state, cases, line, row):
        pattern = r'state "(.*?)"'
        match = re.match(pattern, line)
        if match:
            # 将cases赋值给当前的states，并重置cases
            self.script_tree.add_state(current_state, cases)
            current_state = match.group(1)
            self.script_tree.responses[current_state] = None
            return current_state
        else:
            raise ScriptError("请检查脚本文件的第{}行, state后仅可跟随一个状态".format(row))
        

    def parser_file(self):
        print("parser_file")
        current_state = "默认"
        cases = {}
        row = 0     # 计算行数
        for line in self.script.split('\n'):
            row = row + 1
            line = line.strip()
            line = strip_annotate(line)
            if line == "":
                continue
            # python没有switch，判断行开头
            if line.startswith("when"):
                trigger, condition = self.parser_when(line, row)
                cases[trigger] = condition 
            elif line.startswith("state"):
                current_state = self.parser_state(current_state, cases, line, row)
                cases = {}
            elif line.startswith("response"):
                self.parser_response(current_state, line, row)
            elif line.startswith("entry"):
                self.parser_entry(line, row)
            elif line.startswith("exit"):
                self.parser_exit(line, row)
            elif line.startswith("wait"):
                self.parser_wait(line, current_state, row)
            else:
                raise ScriptError("请检查脚本文件第{}行: {}".format(row, line))
            
        self.script_tree.add_state(current_state, cases)