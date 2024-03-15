from scriptParser import ScriptParser


# 自动测试脚本
class AutoTest:
    def __init__(self, input_path, output_path):
        print("init...")
        self.test_robot = ScriptParser("E:\\bupt-homework/程序设计实践/DSL/script_file/chatScript.bot")
        # 模拟运行环境
        self.user_states = self.test_robot.get_entry()
        self.input_path = input_path
        self.output_path = output_path
        # 输入文本
        self.input = []
        # 检验文本
        self.exam = []
        self.output = []

    # 导入输入文件和验证文件
    def load_file(self):
        with open(self.input_path, 'r', encoding='utf-8') as file:
            input_str = file.read()
        with open(self.output_path, 'r', encoding='utf-8') as file:
            output_str = file.read()
        for line in input_str.split('\n'):
            self.input.append(line.strip())
        for line in output_str.split('\n'):
            self.exam.append(line.strip())

    # 获取生成的输出
    def get_output(self):
        for line in self.input:
            responses, state = self.test_robot.get_response(line, self.user_states)
            for response in responses:
                self.output.append(response)
            self.user_states = state
        for response in self.output:
            print(response)

    # 检查输出是否正确
    def exam_output(self):
        # 1.检查生成语句的数量
        if len(self.output) != len(self.exam):
            return False
        # 2.逐一比较输出内容
        for i in range(len(self.output)):
            print("output: {} \texam:{}".format(self.output[i], self.exam[i]))
            if self.output[i] != self.exam[i]:
                return False
        return True

    # 运行自动测试
    def run(self):
        self.load_file()
        self.get_output()
        if self.exam_output() is not True:
            print("测试不通过")
        else:
            print("测试通过")


if __name__ == "__main__":
    input_path = "test_module/testInput3.txt"
    output_path = "test_module/testOutput3.txt"
    test_bot = AutoTest(input_path, output_path)
    test_bot.run()

