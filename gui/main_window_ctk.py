# gui/main_window_ctk.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

class MainWindow:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.current_view = None
        
        # 设置窗口
        self.root.title("手机门店管理系统")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        
        # 统一配色方案 - 深色科技感
        self.colors = {
            # 侧边栏
            'sidebar_bg': '#0f172a',
            'sidebar_hover': '#1e293b',
            'sidebar_selected': '#3b82f6',
            'sidebar_text': '#94a3b8',
            'sidebar_text_active': '#ffffff',
            
            # 主内容区
            'content_bg': '#0f172a',
            'content_bg_light': '#1e293b',
            'card_bg': '#1e293b',
            'card_border': '#334155',
            
            # 头部
            'header_bg': '#1e293b',
            'header_border': '#334155',
            
            # 主题色
            'accent': '#3b82f6',
            'accent_dark': '#2563eb',
            'accent_light': '#60a5fa',
            'success': '#22c55e',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            
            # 文字颜色
            'text_primary': '#f1f5f9',
            'text_secondary': '#94a3b8',
            'text_disabled': '#64748b',
            
            # 其他
            'border': '#334155',
            'hover': '#334155',
            'time_bg': '#0f172a'
        }
        
        # 设置字体
        self.fonts = {
            'logo': ctk.CTkFont(family="Microsoft YaHei", size=20, weight="bold"),
            'title': ctk.CTkFont(family="Microsoft YaHei", size=24, weight="bold"),
            'subtitle': ctk.CTkFont(family="Microsoft YaHei", size=12),
            'menu': ctk.CTkFont(family="Microsoft YaHei", size=14),
            'content_title': ctk.CTkFont(family="Microsoft YaHei", size=18, weight="bold"),
            'card_title': ctk.CTkFont(family="Microsoft YaHei", size=16, weight="bold"),
            'body': ctk.CTkFont(family="Microsoft YaHei", size=12),
            'body_small': ctk.CTkFont(family="Microsoft YaHei", size=11),
            'button': ctk.CTkFont(family="Microsoft YaHei", size=13, weight="bold"),
            'stat_number': ctk.CTkFont(family="Microsoft YaHei", size=28, weight="bold"),
            'time': ctk.CTkFont(family="Microsoft YaHei", size=14, weight="bold"),
            'date': ctk.CTkFont(family="Microsoft YaHei", size=12)
        }
        
        self.setup_ui()
        self.show_view("销售管理")
    
    def setup_ui(self):
        """设置用户界面"""
        
        # 创建主框架 - 左右紧贴无间隙
        self.main_container = ctk.CTkFrame(self.root, fg_color=self.colors['content_bg'])
        self.main_container.pack(fill="both", expand=True)
        
        # 创建左侧导航栏
        self.create_sidebar()
        
        # 创建右侧内容区域 - 紧贴左侧栏
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['content_bg']
        )
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # 创建顶部标题栏
        self.create_header()
        
        # 创建内容容器
        self.content_area = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.content_area.pack(fill="both", expand=True, padx=20, pady=15)
    
    def create_sidebar(self):
        """创建左侧导航栏"""
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=260,
            fg_color=self.colors['sidebar_bg'],
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # 系统Logo/标题区域
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=30)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="📱",
            font=ctk.CTkFont(size=36),
            text_color=self.colors['accent']
        )
        logo_label.pack()
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="手机管理系统",
            font=self.fonts['logo'],
            text_color=self.colors['sidebar_text_active']
        )
        title_label.pack(pady=(10, 5))
        
        subtitle = ctk.CTkLabel(
            logo_frame,
            text="Mobile Business System",
            font=self.fonts['subtitle'],
            text_color=self.colors['sidebar_text']
        )
        subtitle.pack()
        
        # 分隔线 - 更细
        separator = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=self.colors['sidebar_text']
        )
        separator.pack(fill="x", padx=25, pady=20)
        
        # 导航菜单项
        self.menu_items = {}
        menu_list = [
            ("📊 销售管理", "销售管理", "销售订单管理"),
            ("📦 库存管理", "库存管理", "商品库存管理"),
            ("🔧 维修管理", "维修管理", "维修工单管理"),
            ("🏢 单位管理", "单位管理", "单位信息管理"),
            ("🛒 采购管理", "采购管理", "采购订单管理"),
            ("💰 财务管理", "财务管理", "财务收支管理"),
            ("📈 报表统计", "报表统计", "数据分析报表"),
        ]
        
        for icon_name, view_name, tooltip in menu_list:
            btn = ctk.CTkButton(
                self.sidebar,
                text=icon_name,
                font=self.fonts['menu'],
                fg_color="transparent",
                hover_color=self.colors['sidebar_hover'],
                anchor="w",
                height=44,
                corner_radius=8,
                text_color=self.colors['sidebar_text']
            )
            btn.pack(fill="x", padx=15, pady=2)
            btn.configure(command=lambda v=view_name: self.show_view(v))
            
            # 添加tooltip效果
            def on_enter(e, t=tooltip):
                self.status_label.configure(text=t)
            
            def on_leave(e):
                self.status_label.configure(text="就绪")
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            self.menu_items[view_name] = btn
        
        # 底部信息区域
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=20)
        
        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="就绪",
            font=self.fonts['body_small'],
            text_color=self.colors['sidebar_text']
        )
        self.status_label.pack(pady=5)
        
        version_label = ctk.CTkLabel(
            bottom_frame,
            text="版本 v1.0",
            font=self.fonts['body_small'],
            text_color=self.colors['sidebar_text']
        )
        version_label.pack()
    
    def create_header(self):
        """创建顶部标题栏"""
        self.header = ctk.CTkFrame(
            self.content_frame,
            height=70,
            fg_color=self.colors['header_bg'],
            corner_radius=0
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        # 添加底部边框
        border = ctk.CTkFrame(
            self.header,
            height=1,
            fg_color=self.colors['header_border']
        )
        border.pack(side="bottom", fill="x")
        
        header_inner = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        header_inner.pack(fill="both", expand=True, padx=25, pady=12)
        
        # 左侧 - 当前页面标题
        title_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        self.current_title = ctk.CTkLabel(
            title_frame,
            text="销售管理",
            font=self.fonts['title'],
            text_color=self.colors['text_primary']
        )
        self.current_title.pack(anchor="w")
        
        # 右侧 - 实时时间和用户信息
        right_frame = ctk.CTkFrame(header_inner, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        # 实时时间显示 - 大号字体
        self.time_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=ctk.CTkFont(family="Microsoft YaHei", size=18, weight="bold"),
            text_color=self.colors['accent']
        )
        self.time_label.pack(side="right", padx=15)
        
        # 日期显示
        self.date_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=self.fonts['date'],
            text_color=self.colors['text_secondary']
        )
        self.date_label.pack(side="right", padx=10)
        
        # 分隔线
        sep = ctk.CTkFrame(right_frame, width=1, height=30, fg_color=self.colors['border'])
        sep.pack(side="right", padx=10)
        
        # 用户信息
        user_name = ctk.CTkLabel(
            right_frame,
            text="👤 管理员",
            font=self.fonts['body'],
            text_color=self.colors['text_primary']
        )
        user_name.pack(side="right", padx=5)
        
        # 退出按钮
        exit_btn = ctk.CTkButton(
            right_frame,
            text="退出",
            width=60,
            height=32,
            fg_color="transparent",
            hover_color=self.colors['hover'],
            text_color=self.colors['accent'],
            font=self.fonts['body'],
            corner_radius=6,
            command=self.exit_app
        )
        exit_btn.pack(side="right", padx=10)
        
        self.update_datetime()
    
    def update_datetime(self):
        """更新日期和时间"""
        now = datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        time_str = now.strftime("%H:%M:%S")
        
        self.date_label.configure(text=date_str)
        self.time_label.configure(text=time_str)
        
        self.root.after(1000, self.update_datetime)
    
    def show_view(self, view_name):
        """显示对应的视图"""
        # 更新菜单选中状态
        for name, btn in self.menu_items.items():
            if name == view_name:
                btn.configure(
                    fg_color=self.colors['sidebar_selected'],
                    text_color=self.colors['sidebar_text_active']
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors['sidebar_text']
                )
        
        # 更新标题
        self.current_title.configure(text=view_name)
        
        # 清除当前内容
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        try:
            if view_name == "销售管理":
                from gui.sales_view_ctk import SalesView
                self.current_view = SalesView(self.content_area, self.system, self)
            elif view_name == "库存管理":
                from gui.inventory_view_ctk import InventoryView
                self.current_view = InventoryView(self.content_area, self.system)
            elif view_name == "维修管理":
                from gui.repair_view_ctk import RepairView
                self.current_view = RepairView(self.content_area, self.system, self)
            elif view_name == "单位管理":
                from gui.customer_view_ctk import CustomerView
                self.current_view = CustomerView(self.content_area, self.system, self)
            elif view_name == "采购管理":
                from gui.purchase_view_ctk import PurchaseView
                self.current_view = PurchaseView(self.content_area, self.system)
            elif view_name == "财务管理":
                from gui.finance_view_ctk import FinanceView
                self.current_view = FinanceView(self.content_area, self.system)
            elif view_name == "报表统计":
                from gui.report_view_ctk import ReportView
                self.current_view = ReportView(self.content_area, self.system)
        except Exception as e:
            error_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
            error_frame.pack(expand=True, fill="both")
            
            error_label = ctk.CTkLabel(
                error_frame,
                text=f"🏗️ {view_name}\n\n模块正在建设中...",
                font=self.fonts['title'],
                text_color=self.colors['text_secondary']
            )
            error_label.pack(expand=True)
            print(f"加载视图失败: {e}")
    
    def refresh_all_views(self):
        """刷新所有视图"""
        try:
            if hasattr(self.current_view, 'refresh'):
                self.current_view.refresh()
        except Exception as e:
            print(f"刷新视图失败: {e}")
    
    def exit_app(self):
        """退出应用"""
        if messagebox.askyesno("确认", "确定要退出系统吗？"):
            try:
                self.system.close()
            except:
                pass
            self.root.destroy()