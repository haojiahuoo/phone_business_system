# gui/report_view_ctk.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

class ReportView:
    def __init__(self, parent, system):
        self.system = system
        self.parent = parent
        
        self.setup_ui()
        self.refresh_all()
    
    def setup_ui(self):
        """设置报表统计界面"""
        
        # 创建主滚动区域
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 日期选择卡片
        self.create_date_card()
        
        # 利润统计卡片
        self.create_profit_card()
        
        # 销售报表卡片
        self.create_sales_card()
        
        # 库存统计卡片
        self.create_inventory_card()
    
    def create_date_card(self):
        """创建日期选择卡片"""
        date_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        date_card.pack(fill="x", padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            date_card,
            text="📅 日期范围",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # 日期选择区域
        date_frame = ctk.CTkFrame(date_card, fg_color="transparent")
        date_frame.pack(pady=10)
        
        # 开始日期
        ctk.CTkLabel(date_frame, text="开始日期:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        self.start_date = ctk.CTkEntry(date_frame, width=120, font=ctk.CTkFont(size=14))
        self.start_date.pack(side="left", padx=5)
        self.start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        # 结束日期
        ctk.CTkLabel(date_frame, text="结束日期:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        self.end_date = ctk.CTkEntry(date_frame, width=120, font=ctk.CTkFont(size=14))
        self.end_date.pack(side="left", padx=5)
        self.end_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # 按钮
        ctk.CTkButton(
            date_frame,
            text="查询",
            command=self.refresh_all,
            width=80
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            date_frame,
            text="本月",
            command=self.set_this_month,
            width=80,
            fg_color="#2196F3"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            date_frame,
            text="上月",
            command=self.set_last_month,
            width=80,
            fg_color="#2196F3"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            date_frame,
            text="本年度",
            command=self.set_this_year,
            width=80,
            fg_color="#2196F3"
        ).pack(side="left", padx=5)
    
    def create_profit_card(self):
        """创建利润统计卡片"""
        profit_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        profit_card.pack(fill="x", padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            profit_card,
            text="💰 利润统计",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # 统计信息区域 - 三列布局
        stats_frame = ctk.CTkFrame(profit_card, fg_color="transparent")
        stats_frame.pack(pady=10, padx=20, fill="x")
        
        # 总收入
        income_frame = ctk.CTkFrame(stats_frame, fg_color="#e8f5e9", corner_radius=10)
        income_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            income_frame,
            text="总收入",
            font=ctk.CTkFont(size=14),
            text_color="#4CAF50"
        ).pack(pady=5)
        
        self.income_label = ctk.CTkLabel(
            income_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CAF50"
        )
        self.income_label.pack(pady=10)
        
        # 总支出
        expense_frame = ctk.CTkFrame(stats_frame, fg_color="#ffebee", corner_radius=10)
        expense_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            expense_frame,
            text="总支出",
            font=ctk.CTkFont(size=14),
            text_color="#f44336"
        ).pack(pady=5)
        
        self.expense_label = ctk.CTkLabel(
            expense_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#f44336"
        )
        self.expense_label.pack(pady=10)
        
        # 利润
        profit_frame = ctk.CTkFrame(stats_frame, fg_color="#e3f2fd", corner_radius=10)
        profit_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            profit_frame,
            text="利润",
            font=ctk.CTkFont(size=14),
            text_color="#2196F3"
        ).pack(pady=5)
        
        self.profit_label = ctk.CTkLabel(
            profit_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#2196F3"
        )
        self.profit_label.pack(pady=10)
    
    def create_sales_card(self):
        """创建销售报表卡片"""
        sales_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        sales_card.pack(fill="x", padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            sales_card,
            text="📊 销售报表（按类型）",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # 定义列名
        self.sales_columns = ("订单类型", "订单数量", "总销售额", "已收款", "平均订单金额")
        
        # 表格
        self.sales_table = ctk.CTkScrollableFrame(sales_card, height=200)
        self.sales_table.pack(fill="x", padx=10, pady=10)
        
        # 标题行
        header_frame = ctk.CTkFrame(self.sales_table, fg_color="#f0f0f0")
        header_frame.pack(fill="x", pady=1)
        
        for i, col in enumerate(self.sales_columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150
            )
            label.grid(row=0, column=i, padx=5, pady=8)
        
        # 数据行容器
        self.sales_container = ctk.CTkFrame(self.sales_table, fg_color="transparent")
        self.sales_container.pack(fill="x")
        
        self.sales_rows = []
    
    def create_inventory_card(self):
        """创建库存统计卡片"""
        inventory_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        inventory_card.pack(fill="x", padx=10, pady=10)
        
        # 库存总价值
        value_frame = ctk.CTkFrame(inventory_card, fg_color="#fff3e0", corner_radius=10)
        value_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            value_frame,
            text="📦 库存总价值",
            font=ctk.CTkFont(size=14),
            text_color="#FF9800"
        ).pack(pady=5)
        
        self.inventory_value_label = ctk.CTkLabel(
            value_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FF9800"
        )
        self.inventory_value_label.pack(pady=10)
        
        # 库存预警标题
        ctk.CTkLabel(
            inventory_card,
            text="⚠️ 库存预警（低于最低库存）",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF9800"
        ).pack(pady=10)
        
        # 定义列名
        self.warning_columns = ("商品编码", "商品名称", "当前库存", "最低库存", "缺货数量")
        
        # 预警表格
        self.warning_table = ctk.CTkScrollableFrame(inventory_card, height=200)
        self.warning_table.pack(fill="x", padx=10, pady=10)
        
        # 标题行
        header_frame = ctk.CTkFrame(self.warning_table, fg_color="#f0f0f0")
        header_frame.pack(fill="x", pady=1)
        
        for i, col in enumerate(self.warning_columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=120
            )
            label.grid(row=0, column=i, padx=5, pady=8)
        
        # 数据行容器
        self.warning_container = ctk.CTkFrame(self.warning_table, fg_color="transparent")
        self.warning_container.pack(fill="x")
        
        self.warning_rows = []
    
    def set_this_month(self):
        """设置为本月"""
        today = datetime.now()
        self.start_date.delete(0, "end")
        self.start_date.insert(0, today.replace(day=1).strftime('%Y-%m-%d'))
        self.end_date.delete(0, "end")
        self.end_date.insert(0, today.strftime('%Y-%m-%d'))
        self.refresh_all()
    
    def set_last_month(self):
        """设置为上月"""
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        self.start_date.delete(0, "end")
        self.start_date.insert(0, first_day_last_month.strftime('%Y-%m-%d'))
        self.end_date.delete(0, "end")
        self.end_date.insert(0, last_day_last_month.strftime('%Y-%m-%d'))
        self.refresh_all()
    
    def set_this_year(self):
        """设置为本年度"""
        today = datetime.now()
        self.start_date.delete(0, "end")
        self.start_date.insert(0, today.replace(month=1, day=1).strftime('%Y-%m-%d'))
        self.end_date.delete(0, "end")
        self.end_date.insert(0, today.strftime('%Y-%m-%d'))
        self.refresh_all()
    
    def refresh_all(self):
        """刷新所有报表"""
        try:
            start_date = self.start_date.get()
            end_date = self.end_date.get()
            
            # 利润统计
            profit = self.system.get_profit_loss(start_date, end_date)
            self.income_label.configure(text=f"¥{profit.get('total_income', 0):.2f}")
            self.expense_label.configure(text=f"¥{profit.get('total_expense', 0):.2f}")
            
            profit_value = profit.get('profit', 0)
            profit_color = "#4CAF50" if profit_value >= 0 else "#f44336"
            self.profit_label.configure(text=f"¥{profit_value:.2f}", text_color=profit_color)
            
            # 销售报表
            for row_widgets in self.sales_rows:
                for widget in row_widgets:
                    widget.destroy()
            self.sales_rows.clear()
            
            sales_data = self.system.get_sales_report(start_date, end_date)
            type_map = {'retail': '零售', 'wholesale': '批发', 'online': '网络销售'}
            
            for row in sales_data:
                row_frame = ctk.CTkFrame(self.sales_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=1)
                
                values = [
                    type_map.get(row.get('order_type', ''), row.get('order_type', '')),
                    row.get('order_count', 0),
                    f"¥{row.get('total_sales', 0):.2f}",
                    f"¥{row.get('total_paid', 0):.2f}",
                    f"¥{row.get('avg_order_amount', 0):.2f}"
                ]
                
                widgets = []
                for i, value in enumerate(values):
                    label = ctk.CTkLabel(
                        row_frame,
                        text=str(value),
                        width=150,
                        font=ctk.CTkFont(size=12)
                    )
                    label.grid(row=0, column=i, padx=5, pady=6)
                    widgets.append(label)
                
                self.sales_rows.append(widgets)
            
            # 库存价值
            inv_value = self.system.get_inventory_value()
            self.inventory_value_label.configure(text=f"¥{inv_value:.2f}")
            
            # 库存预警
            for row_widgets in self.warning_rows:
                for widget in row_widgets:
                    widget.destroy()
            self.warning_rows.clear()
            
            self.system.cursor.execute('''
                SELECT product_code, product_name, quantity, min_stock 
                FROM inventory 
                WHERE quantity <= min_stock AND min_stock > 0
                ORDER BY quantity ASC
            ''')
            
            warnings = self.system.cursor.fetchall()
            for w in warnings:
                row_frame = ctk.CTkFrame(self.warning_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=1)
                
                quantity = w.get('quantity', 0)
                min_stock = w.get('min_stock', 0)
                shortage = min_stock - quantity
                
                values = [
                    w.get('product_code', ''),
                    w.get('product_name', ''),
                    quantity,
                    min_stock,
                    shortage
                ]
                
                widgets = []
                for i, value in enumerate(values):
                    # 库存数量标红
                    if i == 2:
                        text_color = "#f44336"
                        font = ctk.CTkFont(size=12, weight="bold")
                    else:
                        text_color = "#333333"
                        font = ctk.CTkFont(size=12)
                    
                    label = ctk.CTkLabel(
                        row_frame,
                        text=str(value),
                        width=120,
                        text_color=text_color,
                        font=font
                    )
                    label.grid(row=0, column=i, padx=5, pady=6)
                    widgets.append(label)
                
                self.warning_rows.append(widgets)
            
            if not warnings:
                row_frame = ctk.CTkFrame(self.warning_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=1)
                
                label = ctk.CTkLabel(
                    row_frame,
                    text="暂无库存预警",
                    width=500,
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                label.grid(row=0, column=0, padx=5, pady=6)
                self.warning_rows.append([label])
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("错误", f"刷新报表失败：{e}")