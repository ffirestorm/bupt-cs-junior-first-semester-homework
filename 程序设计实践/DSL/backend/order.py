# 保存订单的类
class Order:
    def __init__(self, order_id, order_name, order_amount, order_date) :
        self.order_id = order_id        # 订单号
        self.order_type = order_name    # 订单类型
        self.order_amount = order_amount# 订单金额
        self.order_date = order_date    # 订单时间
    
    def __str__(self):
        return f"订单ID: {self.order_id}   商品: {self.order_type}   订单金额: {self.order_amount}   订单日期: {self.order_date}  "