# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from gui.inventory_view import InventoryView
from gui.sales_view import SalesView
from gui.repair_view import RepairView
from gui.report_view import ReportView

class MainWindow:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.root.title("手机维修与二手机买卖管理系统")
        self.root.geometry("1200x700")
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # 初始化各个页面
        self.inventory_view = InventoryView(self.notebook, system)
        self.sales_view = SalesView(self.notebook, system)
        self.repair_view = RepairView(self.notebook, system)
        self.report_view = ReportView(self.notebook, system)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="备份数据", command=self.backup_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def backup_data(self):
        """备份数据"""
        import shutil
        import os
        from datetime import datetime
        
        try:
            backup_dir = 'backups'
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_name = f"{backup_dir}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy('data/phone_business.db', backup_name)
            messagebox.showinfo("成功", f"数据已备份到：{backup_name}")
        except Exception as e:
            messagebox.showerror("错误", f"备份失败：{e}")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
        手机维修与二手机买卖管理系统使用说明
        
        【库存管理】
        - 添加商品：点击"添加商品"按钮，填写商品信息
        - 搜索商品：在搜索框输入关键词，点击搜索
        - 修改库存：双击商品可修改库存数量
        
        【销售管理】
        - 选择或添加客户
        - 选择商品和数量
        - 输入折扣，系统自动计算总价
        - 点击"创建订单"完成销售
        - 可立即收款或稍后收款
        
        【维修管理】
        - 选择客户
        - 填写设备信息和故障描述
        - 输入维修费用和定金
        - 系统自动生成维修订单号
        
        【报表统计】
        - 查看利润统计
        - 查看销售报表
        - 查看库存总价值
        
        【数据备份】
        - 点击"文件->备份数据"进行备份
        - 建议每天备份一次数据
        """
        messagebox.showinfo("使用说明", help_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
        手机维修与二手机买卖管理系统
        版本：1.0.0
        
        功能：
        ✓ 库存管理
        ✓ 销售管理（零售/批发/网络）
        ✓ 维修管理
        ✓ 客户管理
        ✓ 报表统计
        ✓ 数据备份
        
        技术支持：您的公司名称
        """
        messagebox.showinfo("关于", about_text)