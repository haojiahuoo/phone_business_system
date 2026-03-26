# database_mysql.py - MySQL 完整版
import pymysql
from datetime import datetime, date
import uuid
from pymysql.cursors import DictCursor  

class PhoneBusinessSystem:
    def __init__(self, host='localhost', user='phone_user', password='phone123456', database='phone_business'):
        """初始化 MySQL 连接"""
        try:
            self.conn = pymysql.connect(
                host='localhost',      # MySQL 服务器地址
                port=3306,             # MySQL 默认端口
                user='phone_user',  # 数据库用户名
                password='phone123456',  # 数据库密码
                database='phone_business',  # 数据库名
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            self.cursor = self.conn.cursor()
            print(f"✓ MySQL 连接成功 - 数据库: {database}")
        except Exception as e:
            print(f"✗ MySQL 连接失败: {e}")
            print("  请检查:")
            print("  1. MySQL 服务是否启动")
            print("  2. 用户名密码是否正确")
            print("  3. 数据库是否存在")
            raise
    
    def generate_order_no(self, prefix):
        """生成订单号"""
        today = datetime.now().strftime('%Y%m%d')
        random_num = str(uuid.uuid4().int)[:4]
        return f"{prefix}{today}{random_num}"
    
    # ========== 客户管理模块 ==========
    def add_customer(self, name, phone, wechat=None, address=None, customer_type='retail'):
        """添加客户"""
        try:
            self.cursor.execute('''
                INSERT INTO customers (name, phone, wechat, address, customer_type, register_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, phone, wechat, address, customer_type, date.today()))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"添加客户失败: {e}")
            self.conn.rollback()
            return None
    
    def get_all_customers(self):
        """获取所有客户"""
        self.cursor.execute('SELECT * FROM customers ORDER BY id DESC')
        return self.cursor.fetchall()
    
    def get_customer(self, customer_id):
        """获取客户信息"""
        self.cursor.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
        return self.cursor.fetchone()
    
    def search_customers(self, keyword):
        """搜索客户"""
        self.cursor.execute('''
            SELECT * FROM customers 
            WHERE name LIKE %s OR phone LIKE %s OR wechat LIKE %s
            ORDER BY id DESC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()
    
    # ========== 库存管理模块 ==========
    def add_inventory(self, product_code, product_name, category, brand, model, 
                      cost_price, sell_price, wholesale_price, quantity=0, 
                      imei=None, location=None, min_stock=0):
        """添加库存商品"""
        try:
            self.cursor.execute('''
                INSERT INTO inventory 
                (product_code, product_name, category, brand, model, imei, 
                 quantity, cost_price, sell_price, wholesale_price, location, min_stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (product_code, product_name, category, brand, model, imei, 
                  quantity, cost_price, sell_price, wholesale_price, location, min_stock))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"添加库存失败: {e}")
            self.conn.rollback()
            return None
    
    def update_stock(self, inventory_id, quantity_change):
        """更新库存数量"""
        try:
            self.cursor.execute('''
                UPDATE inventory 
                SET quantity = quantity + %s 
                WHERE id = %s
            ''', (quantity_change, inventory_id))
            self.conn.commit()
            
            # 检查库存预警
            self.cursor.execute('SELECT product_name, quantity, min_stock FROM inventory WHERE id = %s', 
                               (inventory_id,))
            product = self.cursor.fetchone()
            if product and product['quantity'] <= product['min_stock']:
                print(f"⚠️ 警告：{product['product_name']} 库存不足！当前库存：{product['quantity']}，最低库存：{product['min_stock']}")
            return True
        except Exception as e:
            print(f"更新库存失败: {e}")
            self.conn.rollback()
            return False
    
    def get_all_inventory(self):
        """获取所有库存"""
        self.cursor.execute('SELECT * FROM inventory ORDER BY id DESC')
        return self.cursor.fetchall()
    
    def search_inventory(self, keyword=None, category=None):
        """搜索库存"""
        query = "SELECT * FROM inventory WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND (product_name LIKE %s OR product_code LIKE %s OR model LIKE %s)"
            params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        query += " ORDER BY id DESC"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    # ========== 维修管理模块 ==========
    def get_all_technicians(self):
        """获取所有技师列表"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, phone, status FROM technicians ORDER BY name")
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"获取技师列表失败: {e}")
            return []
    
    def get_technician_by_id(self, technician_id):
        """根据ID获取技师信息"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, phone, status FROM technicians WHERE id = %s", (technician_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取技师信息失败: {e}")
            return None
        
    def create_repair_order(self, customer_id, device_brand, device_model, problem_desc,
                            repair_type, repair_cost, parts_cost, deposit=0, notes=None):
        """创建维修订单"""
        order_no = self.generate_order_no('R')
        total_cost = repair_cost + parts_cost
        
        try:
            self.cursor.execute('''
                INSERT INTO repair_orders 
                (order_no, customer_id, device_brand, device_model, problem_desc,
                 repair_type, repair_cost, parts_cost, total_cost, deposit,
                 receive_date, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (order_no, customer_id, device_brand, device_model, problem_desc,
                  repair_type, repair_cost, parts_cost, total_cost, deposit,
                  datetime.now(), 'pending', notes))
            self.conn.commit()
            
            order_id = self.cursor.lastrowid
            
            # 记录定金流水
            if deposit > 0:
                self.add_transaction('income', 'repair_deposit', deposit, 
                                    'repair_order', order_id, 'cash')
            
            return order_no
        except Exception as e:
            print(f"创建维修订单失败: {e}")
            self.conn.rollback()
            return None
    
    def get_all_repair_orders(self):
        """获取所有维修订单"""
        self.cursor.execute('''
            SELECT r.*, c.name as customer_name 
            FROM repair_orders r
            LEFT JOIN customers c ON r.customer_id = c.id
            ORDER BY r.id DESC
        ''')
        return self.cursor.fetchall()
    
    def complete_repair(self, order_id):
        """完成维修"""
        try:
            self.cursor.execute('''
                SELECT total_cost, deposit FROM repair_orders WHERE id = %s
            ''', (order_id,))
            order = self.cursor.fetchone()
            
            if order:
                remaining = order['total_cost'] - order['deposit']
                
                self.cursor.execute('''
                    UPDATE repair_orders 
                    SET status = 'completed', finish_date = %s
                    WHERE id = %s
                ''', (datetime.now(), order_id))
                
                if remaining > 0:
                    self.add_transaction('income', 'repair', remaining, 
                                        'repair_order', order_id, 'cash')
                
                self.conn.commit()
                return remaining
            return None
        except Exception as e:
            print(f"完成维修失败: {e}")
            self.conn.rollback()
            return None
    
    # ========== 销售管理模块 ==========
    def create_sales_order(self, customer_id, order_type, items, discount=0, 
                          platform=None, payment_method='cash'):
        """创建销售订单"""
        order_no = self.generate_order_no('S')
        
        try:
            # 开始事务
            self.conn.begin()
            
            # 计算总金额
            total_amount = 0
            for item in items:
                self.cursor.execute('SELECT sell_price FROM inventory WHERE id = %s', 
                                   (item['inventory_id'],))
                price = self.cursor.fetchone()['sell_price']
                subtotal = price * item['quantity']
                total_amount += subtotal
            
            actual_amount = total_amount - discount
            
            # 创建订单
            self.cursor.execute('''
                INSERT INTO sales_orders 
                (order_no, customer_id, order_type, platform, total_amount, 
                 discount, actual_amount, paid_amount, payment_method, status, order_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (order_no, customer_id, order_type, platform, total_amount, 
                  discount, actual_amount, 0, payment_method, 'pending', datetime.now()))
            
            order_id = self.cursor.lastrowid
            
            # 添加订单明细并更新库存
            for item in items:
                self.cursor.execute('SELECT sell_price FROM inventory WHERE id = %s', 
                                   (item['inventory_id'],))
                unit_price = self.cursor.fetchone()['sell_price']
                subtotal = unit_price * item['quantity']
                
                self.cursor.execute('''
                    INSERT INTO sales_order_items (order_id, inventory_id, quantity, unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (order_id, item['inventory_id'], item['quantity'], unit_price, subtotal))
                
                # 减少库存
                self.update_stock(item['inventory_id'], -item['quantity'])
            
            self.conn.commit()
            return order_no, actual_amount
            
        except Exception as e:
            self.conn.rollback()
            print(f"创建订单失败: {e}")
            return None, None
    
    def receive_payment(self, order_id, amount):
        """收取货款"""
        try:
            self.cursor.execute('''
                UPDATE sales_orders 
                SET paid_amount = paid_amount + %s, 
                    status = CASE WHEN paid_amount + %s >= actual_amount THEN 'paid' ELSE 'pending' END
                WHERE id = %s
            ''', (amount, amount, order_id))
            self.conn.commit()
            
            self.add_transaction('income', 'sale', amount, 'sales_order', order_id, 'cash')
            return True
        except Exception as e:
            print(f"收款失败: {e}")
            self.conn.rollback()
            return False
    
    def get_all_sales_orders(self):
        """获取所有销售订单"""
        self.cursor.execute('''
            SELECT s.*, c.name as customer_name 
            FROM sales_orders s
            LEFT JOIN customers c ON s.customer_id = c.id
            ORDER BY s.id DESC
        ''')
        return self.cursor.fetchall()
    
    # ========== 供应商管理模块 ==========
    def add_supplier(self, name, phone, address=None, contact_person=None):
        """添加供应商"""
        try:
            self.cursor.execute('''
                INSERT INTO suppliers (name, phone, address, contact_person)
                VALUES (%s, %s, %s, %s)
            ''', (name, phone, address, contact_person))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"添加供应商失败: {e}")
            self.conn.rollback()
            return None
    
    def get_all_suppliers(self):
        """获取所有供应商"""
        self.cursor.execute('SELECT * FROM suppliers ORDER BY id DESC')
        return self.cursor.fetchall()
    
    # ========== 资金管理模块 ==========
    def add_transaction(self, trans_type, category, amount, reference_type, reference_id, payment_method):
        """添加资金流水"""
        try:
            self.cursor.execute('''
                INSERT INTO transactions 
                (transaction_date, type, category, amount, reference_type, reference_id, payment_method)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (datetime.now(), trans_type, category, amount, reference_type, reference_id, payment_method))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"添加流水失败: {e}")
            self.conn.rollback()
            return False
    
    def get_profit_loss(self, start_date=None, end_date=None):
        """获取利润统计"""
        where_clause = ""
        params = []
        
        if start_date:
            where_clause += " AND transaction_date >= %s"
            params.append(start_date)
        if end_date:
            where_clause += " AND transaction_date <= %s"
            params.append(end_date)
        
        # 总收入
        self.cursor.execute(f'''
            SELECT COALESCE(SUM(amount), 0) as total FROM transactions 
            WHERE type = 'income' {where_clause}
        ''', params)
        total_income = self.cursor.fetchone()['total']
        
        # 总支出
        self.cursor.execute(f'''
            SELECT COALESCE(SUM(amount), 0) as total FROM transactions 
            WHERE type = 'expense' {where_clause}
        ''', params)
        total_expense = self.cursor.fetchone()['total']
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'profit': total_income - total_expense
        }
    
    def get_sales_report(self, start_date=None, end_date=None):
        """销售报表统计"""
        query = '''
            SELECT 
                order_type,
                COUNT(*) as order_count,
                SUM(actual_amount) as total_sales,
                SUM(paid_amount) as total_paid,
                AVG(actual_amount) as avg_order_amount
            FROM sales_orders
            WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += " AND order_date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND order_date <= %s"
            params.append(end_date)
        
        query += " GROUP BY order_type"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_inventory_value(self):
        """获取库存总价值"""
        self.cursor.execute('''
            SELECT SUM(quantity * cost_price) as total FROM inventory WHERE status = 'available'
        ''')
        result = self.cursor.fetchone()
        return result['total'] if result and result['total'] else 0
    
    def close(self):
        """关闭数据库连接"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("✓ 数据库连接已关闭")