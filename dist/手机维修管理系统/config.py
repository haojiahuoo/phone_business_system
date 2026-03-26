# config.py
import os

# 数据库配置
DATABASE_PATH = 'data/phone_business.db'

# 应用配置
APP_NAME = '手机维修与二手机买卖管理系统'
APP_VERSION = '1.0.0'

# 订单号前缀
ORDER_PREFIX = {
    'repair': 'R',
    'sale': 'S',
    'purchase': 'P'
}

# 订单类型
ORDER_TYPES = {
    'retail': '零售',
    'wholesale': '批发',
    'online': '网络销售'
}

# 维修类型
REPAIR_TYPES = {
    'hardware': '硬件维修',
    'software': '软件维修',
    'water_damage': '进水维修'
}

# 支付方式
PAYMENT_METHODS = ['现金', '微信', '支付宝', '银行卡']

# 客户类型
CUSTOMER_TYPES = ['零售客户', '批发客户', '网络客户']

# 库存分类
INVENTORY_CATEGORIES = ['手机', '配件', '周边']