# gui/report_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class ReportView:
    def __init__(self, parent, system):
        self.system = system
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="报表统计")
        
        self.setup_ui()
        self.refresh_all()
    
    def setup_ui(self):
        # 日期选择区域
        date_frame = ttk.LabelFrame(self.frame, text="日期范围", padding=10)
        date_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(date_frame, text="开始日期:").pack(side='left', padx=5)
        self.start_date = ttk.Entry(date_frame, width=12)
        self.start_date.pack(side='left', padx=5)
        self.start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        ttk.Label(date_frame, text="结束日期:").pack(side='left', padx=5)
        self.end_date = ttk.Entry(date_frame, width=12)
        self.end_date.pack(side='left', padx=5)
        self.end_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ttk.Button(date_frame, text="查询", command=self.refresh_all).pack(side='left', padx=10)
        ttk.Button(date_frame, text="本月", command=self.set_this_month).pack(side='left', padx=5)
        ttk.Button(date_frame, text="上月", command=self.set_last_month).pack(side='left', padx=5)
        ttk.Button(date_frame, text="本年度", command=self.set_this_year).pack(side='left', padx=5)
        
        # 利润统计
        profit_frame = ttk.LabelFrame(self.frame, text="利润统计", padding=10)
        profit_frame.pack(pady=10, padx=20, fill='x')
        
        self.income_label = ttk.Label(profit_frame, text="总收入：¥0.00", font=('Arial', 12))
        self.income_label.pack(anchor='w', pady=5)
        
        self.expense_label = ttk.Label(profit_frame, text="总支出：¥0.00", font=('Arial', 12))
        self.expense_label.pack(anchor='w', pady=5)
        
        self.profit_label = ttk.Label(profit_frame, text="利润：¥0.00", font=('Arial', 14, 'bold'), foreground='green')
        self.profit_label.pack(anchor='w', pady=5)
        
        # 销售报表
        sales_frame = ttk.LabelFrame(self.frame, text="销售报表（按类型）", padding=10)
        sales_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns = ('订单类型', '订单数量', '总销售额', '已收款', '平均订单金额')
        self.sales_tree = ttk.Treeview(sales_frame, columns=columns, show='headings', height=5)
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=120)
        self.sales_tree.pack(fill='both', expand=True)
        
        # 库存统计
        inventory_frame = ttk.LabelFrame(self.frame, text="库存统计", padding=10)
        inventory_frame.pack(pady=10, padx=20, fill='x')
        
        self.inventory_value_label = ttk.Label(inventory_frame, text="库存总价值：¥0.00", font=('Arial', 12))
        self.inventory_value_label.pack(anchor='w', pady=5)
        
        # 库存预警
        warning_frame = ttk.LabelFrame(self.frame, text="库存预警（低于最低库存）", padding=10)
        warning_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        columns_warning = ('商品编码', '商品名称', '当前库存', '最低库存', '缺货数量')
        self.warning_tree = ttk.Treeview(warning_frame, columns=columns_warning, show='headings', height=5)
        for col in columns_warning:
            self.warning_tree.heading(col, text=col)
            self.warning_tree.column(col, width=120)
        self.warning_tree.pack(fill='both', expand=True)
    
    def set_this_month(self):
        """设置为本月"""
        today = datetime.now()
        self.start_date.delete(0, 'end')
        self.start_date.insert(0, today.replace(day=1).strftime('%Y-%m-%d'))
        self.end_date.delete(0, 'end')
        self.end_date.insert(0, today.strftime('%Y-%m-%d'))
        self.refresh_all()
    
    def set_last_month(self):
        """设置为上月"""
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        
        self.start_date.delete(0, 'end')
        self.start_date.insert(0, first_day_last_month.strftime('%Y-%m-%d'))
        self.end_date.delete(0, 'end')
        self.end_date.insert(0, last_day_last_month.strftime('%Y-%m-%d'))
        self.refresh_all()
    
    def set_this_year(self):
        """设置为本年度"""
        today = datetime.now()
        self.start_date.delete(0, 'end')
        self.start_date.insert(0, today.replace(month=1, day=1).strftime('%Y-%m-%d'))
        self.end_date.delete(0, 'end')
        self.end_date.insert(0, today.strftime('%Y-%m-%d'))
        self.refresh_all()
    
    def refresh_all(self):
        """刷新所有报表"""
        try:
            start_date = self.start_date.get()
            end_date = self.end_date.get()
            
            # 利润统计
            profit = self.system.get_profit_loss(start_date, end_date)
            self.income_label.config(text=f"总收入：¥{profit['total_income']:.2f}")
            self.expense_label.config(text=f"总支出：¥{profit['total_expense']:.2f}")
            
            profit_color = 'green' if profit['profit'] >= 0 else 'red'
            self.profit_label.config(text=f"利润：¥{profit['profit']:.2f}", foreground=profit_color)
            
            # 销售报表
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)
            
            sales_data = self.system.get_sales_report(start_date, end_date)
            type_map = {'retail': '零售', 'wholesale': '批发', 'online': '网络销售'}
            
            for row in sales_data:
                self.sales_tree.insert('', 'end', values=(
                    type_map.get(row[0], row[0]),
                    row[1],
                    f"¥{row[2]:.2f}",
                    f"¥{row[3]:.2f}",
                    f"¥{row[4]:.2f}"
                ))
            
            # 库存价值
            inv_value = self.system.get_inventory_value()
            self.inventory_value_label.config(text=f"库存总价值：¥{inv_value:.2f}")
            
            # 库存预警
            for item in self.warning_tree.get_children():
                self.warning_tree.delete(item)
            
            self.system.cursor.execute('''
                SELECT product_code, product_name, quantity, min_stock 
                FROM inventory 
                WHERE quantity <= min_stock AND min_stock > 0
                ORDER BY quantity ASC
            ''')
            
            warnings = self.system.cursor.fetchall()
            for w in warnings:
                shortage = w[3] - w[2]
                self.warning_tree.insert('', 'end', values=(
                    w[0], w[1], w[2], w[3], shortage
                ))
            
            if not warnings:
                self.warning_tree.insert('', 'end', values=('', '无库存预警', '', '', ''))
            
        except Exception as e:
            messagebox.showerror("错误", f"刷新报表失败：{e}")