import threading
import time

class TimerThread:
    def __init__(self):
        self.timer_list = {}  # 计时器字典

    def add_timer(self, username, timer):
        self.timer_list[username] = timer

    def update_timer(self, username, new_timer):
        if username in self.timer_list:
            self.timer_list[username] = new_timer

    def remove_timer(self, username):
        if username in self.timer_list:
            del self.timer_list[username]

    def run(self):
        while True:
            self.update_timers()
            expired_users = self.extract_expired_users()
            print(f"Expired Users: {expired_users}")
            time.sleep(1)

    def update_timers(self):
        for username in list(self.timer_list.keys()):
            self.timer_list[username] -= 1

    def extract_expired_users(self):
        # 存放等待时间已到的用户信息的列表
        expired_users = []

        # 遍历每个用户的倒计时信息
        for username, remaining_time in self.timer_list.items():
            if remaining_time <= 0:
                expired_users.append(username)
                self.remove_timer(username)

        # 返回等待时间已到的用户信息列表
        return expired_users