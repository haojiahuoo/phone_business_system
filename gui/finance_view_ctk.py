# gui/finance_view_ctk.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

class FinanceView:
    def __init__(self, parent, system):
        self.system = system
        self.parent = parent
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """设置财务管理界面"""
        self.main_frame = ctk.CTkScrollableFrame(self.parent, fg_color="#1e1e2e")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 财务概览卡片
        self.create_overview_card()
        
        # 收支明细卡片
        self.create_transaction_card()
        
        # 图表区域（简化版）
        self.create_chart_card()
    
    def create_overview_card(self):
        """创建财务概览卡片"""
        card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2d2d2d")
        card.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="💰 财务概览",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title.pack(pady=15)
        
        # 统计信息 - 三列布局
        stats_frame = ctk.CTkFrame(card, fg_color="transparent")
        stats_frame.pack(pady=10, padx=20, fill="x")
        
        # 总收入
        income_frame = ctk.CTkFrame(stats_frame, fg_color="#27ae60", corner_radius=10)
        income_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(income_frame, text="总收入", font=ctk.CTkFont(size=12), text_color="white").pack(pady=5)
        self.income_label = ctk.CTkLabel(
            income_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.income_label.pack(pady=10)
        
        # 总支出
        expense_frame = ctk.CTkFrame(stats_frame, fg_color="#e74c3c", corner_radius=10)
        expense_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(expense_frame, text="总支出", font=ctk.CTkFont(size=12), text_color="white").pack(pady=5)
        self.expense_label = ctk.CTkLabel(
            expense_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.expense_label.pack(pady=10)
        
        # 净利润
        profit_frame = ctk.CTkFrame(stats_frame, fg_color="#3498db", corner_radius=10)
        profit_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(profit_frame, text="净利润", font=ctk.CTkFont(size=12), text_color="white").pack(pady=5)
        self.profit_label = ctk.CTkLabel(
            profit_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        self.profit_label.pack(pady=10)
    
    def create_transaction_card(self):
        """创建收支明细卡片"""
        card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2d2d2d")
        card.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="📋 近期收支明细",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        title.pack(pady=10)
        
        # 日期选择
        date_frame = ctk.CTkFrame(card, fg_color="transparent")
        date_frame.pack(pady=10)
        
        ctk.CTkLabel(date_frame, text="开始日期:", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        self.start_date = ctk.CTkEntry(date_frame, width=120, font=ctk.CTkFont(size=12))
        self.start_date.pack(side="left", padx=5)
        self.start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        ctk.CTkLabel(date_frame, text="结束日期:", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        self.end_date = ctk.CTkEntry(date_frame, width=120, font=ctk.CTkFont(size=12))
        self.end_date.pack(side="left", padx=5)
        self.end_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ctk.CTkButton(
            date_frame,
            text="查询",
            command=self.refresh,
            width=60
        ).pack(side="left", padx=10)
        
        # 交易记录表格
        columns = ("日期", "类型", "类别", "金额", "支付方式", "备注")
        self.transaction_tree = ctk.CTkScrollableFrame(card, height=300)
        self.transaction_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题行
        header = ctk.CTkFrame(self.transaction_tree, fg_color="#3c3c3c")
        header.pack(fill="x", pady=1)
        
        for i, col in enumerate(columns):
            label = ctk.CTkLabel(header, text=col, width=120, font=ctk.CTkFont(size=12, weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5)
        
        self.transaction_container = ctk.CTkFrame(self.transaction_tree, fg_color="transparent")
        self.transaction_container.pack(fill="x")
        
        self.transaction_rows = []
    
    def create_chart_card(self):
        """创建图表卡片（简化版）"""
        card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2d2d2d")
        card.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="📊 月度趋势",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        title.pack(pady=10)
        
        # 简化的趋势显示
        trend_frame = ctk.CTkFrame(card, fg_color="transparent")
        trend_frame.pack(pady=20)
        
        months = ["1月", "2月", "3月", "4月", "5月", "6月"]
        self.trend_bars = []
        
        for i, month in enumerate(months):
            month_frame = ctk.CTkFrame(trend_frame, fg_color="transparent")
            month_frame.pack(side="left", fill="both", expand=True)
            
            ctk.CTkLabel(month_frame, text=month, font=ctk.CTkFont(size=10)).pack()
            bar = ctk.CTkFrame(month_frame, height=100, width=30, fg_color="#3498db", corner_radius=5)
            bar.pack(pady=5)
            # 初始高度为0
            bar.configure(height=0)
            self.trend_bars.append(bar)
            
            value_label = ctk.CTkLabel(month_frame, text="0", font=ctk.CTkFont(size=9))
            value_label.pack()
            self.trend_bars.append(value_label)
    
    def refresh(self):
        """刷新财务数据"""
        # 这里需要从数据库获取实际数据
        # 示例数据
        self.income_label.configure(text="¥12,345.67")
        self.expense_label.configure(text="¥8,234.56")
        self.profit_label.configure(text="¥4,111.11")