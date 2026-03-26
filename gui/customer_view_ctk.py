# gui/customer_view_ctk.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime

class CustomerView:
    def __init__(self, parent, system, main_window=None):
        self.system = system
        self.parent = parent
        self.main_window = main_window  # 保存主窗口引用
        self.col_widths = [50, 100, 120, 120, 200, 100, 120]  # 定义列宽
        
        # 设置颜色方案
        self.colors = {
            'bg': '#1e1e1e',           # 主背景色
            'card_bg': '#2d2d2d',       # 卡片背景色
            'header_bg': '#3c3c3c',     # 表头背景色
            'row_even': '#2d2d2d',      # 偶数行背景色
            'row_odd': '#3a3a3a',       # 奇数行背景色
            'row_hover': '#4a4a4a',     # 鼠标悬停背景色
            'text': '#ffffff',          # 文字颜色
            'text_light': '#a0a0a0',    # 浅色文字
            'border': '#4a4a4a'         # 边框颜色
        }
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """设置客户管理界面"""
        
        # 创建主滚动区域
        self.main_frame = ctk.CTkScrollableFrame(
            self.parent,
            fg_color=self.colors['bg']
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 统计卡片
        self.create_stats_card()
        
        # 工具栏卡片
        self.create_toolbar_card()
        
        # 客户列表卡片
        self.create_customer_card()
    
    def create_stats_card(self):
        """创建统计卡片"""
        stats_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        stats_card.pack(fill="x", padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            stats_card,
            text="📊 客户统计",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text']
        )
        title.pack(pady=10)
        
        # 统计信息 - 四列布局
        stats_frame = ctk.CTkFrame(stats_card, fg_color="transparent")
        stats_frame.pack(pady=10, padx=20, fill="x")
        
        # 总客户数
        total_frame = ctk.CTkFrame(
            stats_frame,
            fg_color="#2c3e50",
            corner_radius=10
        )
        total_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            total_frame,
            text="👥 总客户数",
            font=ctk.CTkFont(size=12),
            text_color="#ecf0f1"
        ).pack(pady=5)
        
        self.total_count_label = ctk.CTkLabel(
            total_frame,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#3498db"
        )
        self.total_count_label.pack(pady=10)
        
        # 零售客户
        retail_frame = ctk.CTkFrame(
            stats_frame,
            fg_color="#27ae60",
            corner_radius=10
        )
        retail_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            retail_frame,
            text="🛒 零售客户",
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(pady=5)
        
        self.retail_count_label = ctk.CTkLabel(
            retail_frame,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.retail_count_label.pack(pady=10)
        
        # 批发客户
        wholesale_frame = ctk.CTkFrame(
            stats_frame,
            fg_color="#f39c12",
            corner_radius=10
        )
        wholesale_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            wholesale_frame,
            text="📦 批发客户",
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(pady=5)
        
        self.wholesale_count_label = ctk.CTkLabel(
            wholesale_frame,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.wholesale_count_label.pack(pady=10)
        
        # 网络客户
        online_frame = ctk.CTkFrame(
            stats_frame,
            fg_color="#9b59b6",
            corner_radius=10
        )
        online_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(
            online_frame,
            text="🌐 网络客户",
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(pady=5)
        
        self.online_count_label = ctk.CTkLabel(
            online_frame,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.online_count_label.pack(pady=10)
    
    def create_toolbar_card(self):
        """创建工具栏卡片"""
        toolbar_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        toolbar_card.pack(fill="x", padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            toolbar_card,
            text="🔍 客户管理",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text']
        )
        title.pack(pady=10)
        
        # 工具栏
        toolbar_frame = ctk.CTkFrame(toolbar_card, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=20, pady=10)
        
        # 搜索框
        ctk.CTkLabel(
            toolbar_frame,
            text="搜索:",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text']
        ).pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            toolbar_frame,
            textvariable=self.search_var,
            width=250,
            placeholder_text="姓名/电话/微信...",
            fg_color=self.colors['bg'],
            text_color=self.colors['text']
        )
        self.search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar_frame,
            text="🔍 搜索",
            command=self.search,
            width=80,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar_frame,
            text="📋 显示全部",
            command=self.refresh,
            width=100,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar_frame,
            text="➕ 添加客户",
            command=self.add_customer,
            width=120,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            toolbar_frame,
            text="📊 导出数据",
            command=self.export_customers,
            width=100,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        ).pack(side="right", padx=5)
    
    def create_customer_card(self):
        """创建客户列表卡片"""
        customer_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=15,
            fg_color=self.colors['card_bg']
        )
        customer_card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            customer_card,
            text="📋 客户列表",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text']
        )
        title.pack(pady=10)
        
        # 定义列名
        self.columns = ("ID", "姓名", "电话", "微信", "地址", "客户类型", "注册日期")
        
        # 创建表格容器
        self.table_frame = ctk.CTkScrollableFrame(
            customer_card,
            height=500,
            fg_color=self.colors['bg']
        )
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题行
        header_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color=self.colors['header_bg'],
            corner_radius=5
        )
        header_frame.pack(fill="x", pady=1)
        
        for i, col in enumerate(self.columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=self.col_widths[i],
                text_color=self.colors['text']
            )
            label.grid(row=0, column=i, padx=5, pady=10)
        
        # 添加操作列
        action_label = ctk.CTkLabel(
            header_frame,
            text="操作",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=120,
            text_color=self.colors['text']
        )
        action_label.grid(row=0, column=len(self.columns), padx=5, pady=10)
        
        # 数据行容器
        self.data_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.data_container.pack(fill="x")
        
        self.data_rows = []
    
    def update_table(self, customers):
        """更新表格显示 - 从上往下显示，交替行颜色"""
        # 清除现有行
        for row_widgets in self.data_rows:
            for widget in row_widgets:
                widget.destroy()
        self.data_rows.clear()
        
        # 统计各类客户数量
        retail_count = 0
        wholesale_count = 0
        online_count = 0
        
        # 从上往下显示（正常顺序）
        for idx, customer in enumerate(customers):
            # 交替行颜色
            if idx % 2 == 0:
                row_bg = self.colors['row_even']
            else:
                row_bg = self.colors['row_odd']
            
            row_frame = ctk.CTkFrame(
                self.data_container,
                fg_color=row_bg,
                corner_radius=3
            )
            row_frame.pack(fill="x", pady=1)
            
            # 绑定鼠标悬停效果
            def on_enter(e, f=row_frame):
                f.configure(fg_color=self.colors['row_hover'])
            
            def on_leave(e, f=row_frame):
                if idx % 2 == 0:
                    f.configure(fg_color=self.colors['row_even'])
                else:
                    f.configure(fg_color=self.colors['row_odd'])
            
            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            
            # 客户类型统计
            customer_type = customer.get('customer_type', 'retail')
            if customer_type == 'retail':
                retail_count += 1
                type_display = "零售客户"
                type_color = "#27ae60"
            elif customer_type == 'wholesale':
                wholesale_count += 1
                type_display = "批发客户"
                type_color = "#f39c12"
            else:
                online_count += 1
                type_display = "网络客户"
                type_color = "#9b59b6"
            
            # 格式化日期
            register_date = customer.get('register_date', '')
            if register_date and hasattr(register_date, 'strftime'):
                date_str = register_date.strftime('%Y-%m-%d')
            else:
                date_str = str(register_date)[:10] if register_date else ''
            
            values = [
                customer.get('id', ''),
                customer.get('name', ''),
                customer.get('phone', ''),
                customer.get('wechat', '') or '-',
                (customer.get('address', '') or '-')[:30],
                type_display,
                date_str
            ]
            
            widgets = []
            for i, value in enumerate(values):
                # 根据列设置不同样式
                if i == 1:  # 姓名列
                    text_color = "#3498db"
                    font = ctk.CTkFont(size=12, weight="bold")
                elif i == 5:  # 类型列
                    text_color = type_color
                    font = ctk.CTkFont(size=12)
                else:
                    text_color = self.colors['text']
                    font = ctk.CTkFont(size=12)
                
                label = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    width=self.col_widths[i],
                    text_color=text_color,
                    font=font
                )
                label.grid(row=0, column=i, padx=5, pady=8)
                widgets.append(label)
            
            # 操作按钮
            button_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            button_frame.grid(row=0, column=len(self.columns), padx=5, pady=4)
            
            edit_btn = ctk.CTkButton(
                button_frame,
                text="编辑",
                width=50,
                height=28,
                fg_color="#3498db",
                hover_color="#2980b9",
                font=ctk.CTkFont(size=11),
                command=lambda c=customer: self.edit_customer(c)
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(
                button_frame,
                text="删除",
                width=50,
                height=28,
                fg_color="#e74c3c",
                hover_color="#c0392b",
                font=ctk.CTkFont(size=11),
                command=lambda c=customer: self.delete_customer(c)
            )
            delete_btn.pack(side="left", padx=2)
            
            widgets.extend([edit_btn, delete_btn])
            self.data_rows.append(widgets)
        
        # 更新统计信息
        self.total_count_label.configure(text=str(len(customers)))
        self.retail_count_label.configure(text=str(retail_count))
        self.wholesale_count_label.configure(text=str(wholesale_count))
        self.online_count_label.configure(text=str(online_count))
    
    def refresh(self):
        """刷新客户列表"""
        customers = self.system.get_all_customers()
        # 按ID升序排列，确保从上往下显示
        customers = sorted(customers, key=lambda x: x.get('id', 0))
        self.update_table(customers)
    
    def search(self):
        """搜索客户"""
        keyword = self.search_var.get()
        if keyword:
            customers = self.system.search_customers(keyword)
        else:
            customers = self.system.get_all_customers()
        # 按ID升序排列
        customers = sorted(customers, key=lambda x: x.get('id', 0))
        self.update_table(customers)
    
    def add_customer(self):
        """添加客户对话框"""
        dialog = ctk.CTkToplevel()
        dialog.title("添加客户")
        dialog.geometry("500x600")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # 使窗口居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 500) // 2
        y = (dialog.winfo_screenheight() - 600) // 2
        dialog.geometry(f"500x600+{x}+{y}")
        
        fields = {}
        labels = [
            ('姓名', 'entry', True),
            ('电话', 'entry', True),
            ('微信', 'entry', False),
            ('地址', 'text', False),
            ('客户类型', 'combo', False)
        ]
        types = ['零售客户', '批发客户', '网络客户']
        type_map = {'零售客户': 'retail', '批发客户': 'wholesale', '网络客户': 'online'}
        
        scroll_frame = ctk.CTkScrollableFrame(dialog, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, (label, field_type, required) in enumerate(labels):
            # 标签
            label_text = f"{label}{' *' if required else ''}:"
            ctk.CTkLabel(scroll_frame, text=label_text, font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, padx=10, pady=10, sticky="e"
            )
            
            # 输入框
            if field_type == 'combo':
                entry = ctk.CTkComboBox(scroll_frame, values=types, width=250, font=ctk.CTkFont(size=14))
                entry.set('零售客户')
            elif field_type == 'text':
                entry = ctk.CTkTextbox(scroll_frame, width=250, height=80, font=ctk.CTkFont(size=14))
            else:
                entry = ctk.CTkEntry(scroll_frame, width=250, font=ctk.CTkFont(size=14))
            
            entry.grid(row=i, column=1, padx=10, pady=10)
            fields[label] = entry
        
        def save():
            try:
                # 获取数据
                name = fields['姓名'].get().strip()
                phone = fields['电话'].get().strip()
                
                # 验证必填字段
                if not name:
                    messagebox.showwarning("警告", "请填写客户姓名")
                    return
                if not phone:
                    messagebox.showwarning("警告", "请填写客户电话")
                    return
                
                # 获取地址
                if isinstance(fields['地址'], ctk.CTkTextbox):
                    address = fields['地址'].get("1.0", "end-1c").strip()
                else:
                    address = fields['地址'].get().strip()
                
                # 获取客户类型
                customer_type_cn = fields['客户类型'].get()
                customer_type = type_map.get(customer_type_cn, 'retail')
                
                # 添加客户
                result = self.system.add_customer(
                    name=name,
                    phone=phone,
                    wechat=fields['微信'].get().strip(),
                    address=address,
                    customer_type=customer_type
                )
                
                if result:
                    messagebox.showinfo("成功", f"客户 '{name}' 添加成功！")
                    dialog.destroy()
                    self.refresh()
                    
                    # 刷新其他页面（销售和维修）
                    if self.main_window:
                        self.main_window.refresh_all_views()
                        
                else:
                    messagebox.showerror("错误", "添加客户失败")
                    
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{e}")
        
        # 按钮区域
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="保存",
            command=save,
            width=100,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="取消",
            command=dialog.destroy,
            width=100,
            height=35,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def edit_customer(self, customer):
        """编辑客户信息"""
        dialog = ctk.CTkToplevel()
        dialog.title(f"编辑客户 - {customer.get('name', '')}")
        dialog.geometry("500x600")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # 使窗口居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 500) // 2
        y = (dialog.winfo_screenheight() - 600) // 2
        dialog.geometry(f"500x600+{x}+{y}")
        
        fields = {}
        labels = [
            ('姓名', 'entry', True),
            ('电话', 'entry', True),
            ('微信', 'entry', False),
            ('地址', 'text', False),
            ('客户类型', 'combo', False)
        ]
        types = ['零售客户', '批发客户', '网络客户']
        type_map = {'零售客户': 'retail', '批发客户': 'wholesale', '网络客户': 'online'}
        reverse_type_map = {'retail': '零售客户', 'wholesale': '批发客户', 'online': '网络客户'}
        
        scroll_frame = ctk.CTkScrollableFrame(dialog, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, (label, field_type, required) in enumerate(labels):
            # 标签
            label_text = f"{label}{' *' if required else ':'}"
            ctk.CTkLabel(scroll_frame, text=label_text, font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, padx=10, pady=10, sticky="e"
            )
            
            # 输入框
            if field_type == 'combo':
                entry = ctk.CTkComboBox(scroll_frame, values=types, width=250, font=ctk.CTkFont(size=14))
                current_type = reverse_type_map.get(customer.get('customer_type', 'retail'), '零售客户')
                entry.set(current_type)
            elif field_type == 'text':
                entry = ctk.CTkTextbox(scroll_frame, width=250, height=80, font=ctk.CTkFont(size=14))
                address = customer.get('address', '') or ''
                entry.insert("1.0", address)
            else:
                entry = ctk.CTkEntry(scroll_frame, width=250, font=ctk.CTkFont(size=14))
                if label == '姓名':
                    entry.insert(0, customer.get('name', ''))
                elif label == '电话':
                    entry.insert(0, customer.get('phone', ''))
                elif label == '微信':
                    entry.insert(0, customer.get('wechat', '') or '')
            
            entry.grid(row=i, column=1, padx=10, pady=10)
            fields[label] = entry
        
        def save():
            try:
                # 获取数据
                name = fields['姓名'].get().strip()
                phone = fields['电话'].get().strip()
                
                # 验证必填字段
                if not name:
                    messagebox.showwarning("警告", "请填写客户姓名")
                    return
                if not phone:
                    messagebox.showwarning("警告", "请填写客户电话")
                    return
                
                # 获取地址
                if isinstance(fields['地址'], ctk.CTkTextbox):
                    address = fields['地址'].get("1.0", "end-1c").strip()
                else:
                    address = fields['地址'].get().strip()
                
                # 获取客户类型
                customer_type_cn = fields['客户类型'].get()
                customer_type = type_map.get(customer_type_cn, 'retail')
                
                # 更新客户信息
                # 注意：需要先在 database_mysql.py 中添加 update_customer 方法
                success = self.system.update_customer(
                    customer_id=customer.get('id'),
                    name=name,
                    phone=phone,
                    wechat=fields['微信'].get().strip(),
                    address=address,
                    customer_type=customer_type
                )
                
                if success:
                    messagebox.showinfo("成功", f"客户 '{name}' 更新成功！")
                    dialog.destroy()
                    
                    # 刷新当前页面
                    self.refresh()
                    
                    # 刷新其他页面（销售和维修）
                    if self.main_window:
                        print("🔄 编辑客户后刷新所有视图...")
                        self.main_window.refresh_all_views()
                    else:
                        self.refresh_other_views()
                    
                else:
                    messagebox.showerror("错误", "更新客户失败")
                    
            except Exception as e:
                messagebox.showerror("错误", f"更新失败：{e}")
        
        # 按钮区域
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="保存",
            command=save,
            width=100,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="取消",
            command=dialog.destroy,
            width=100,
            height=35,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def delete_customer(self, customer):
        """删除客户"""
        result = messagebox.askyesno(
            "确认删除",
            f"确定要删除客户 '{customer.get('name')}' 吗？\n\n如果该客户有订单记录，建议仅标记为禁用而不是删除。"
        )
        
        if result:
            try:
                # 检查是否有订单
                orders = self.system.get_customer_orders(customer.get('id'))
                if orders and len(orders) > 0:
                    messagebox.showwarning(
                        "无法删除",
                        f"该客户有 {len(orders)} 个订单记录，无法直接删除。\n建议在数据库中标记为禁用状态。"
                    )
                    return
                
                # 删除客户
                success = self.system.delete_customer(customer.get('id'))
                
                if success:
                    messagebox.showinfo("成功", f"客户 '{customer.get('name')}' 已删除")
                    
                    # 刷新当前页面
                    self.refresh()
                    
                    # 刷新其他页面（销售和维修）
                    if self.main_window:
                        print("🔄 删除客户后刷新所有视图...")
                        self.main_window.refresh_all_views()
                    else:
                        # 如果没有主窗口引用，直接刷新销售和维修视图（如果存在）
                        self.refresh_other_views()
                    
                else:
                    messagebox.showerror("错误", "删除客户失败")
                    
            except Exception as e:
                messagebox.showerror("错误", f"删除失败：{e}")
                import traceback
                traceback.print_exc()

    def refresh_other_views(self):
        """刷新其他视图（当没有主窗口引用时的备用方案）"""
        try:
            # 尝试获取顶层窗口
            top = self.parent.winfo_toplevel()
            
            # 遍历顶层窗口的所有子窗口，查找其他视图
            for child in top.winfo_children():
                # 查找主窗口实例
                if hasattr(child, 'sales_view') and child.sales_view:
                    if hasattr(child.sales_view, 'load_customers'):
                        child.sales_view.load_customers()
                        print("  ✅ 销售视图客户列表已刷新")
                
                if hasattr(child, 'repair_view') and child.repair_view:
                    if hasattr(child.repair_view, 'load_customers'):
                        child.repair_view.load_customers()
                        print("  ✅ 维修视图客户列表已刷新")
                        
        except Exception as e:
            print(f"刷新其他视图失败: {e}")
    
    def export_customers(self):
        """导出客户数据"""
        try:
            from datetime import datetime
            import csv
            
            # 获取所有客户
            customers = self.system.get_all_customers()
            
            if not customers:
                messagebox.showinfo("提示", "没有客户数据可导出")
                return
            
            # 保存文件对话框
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"customers_{datetime.now().strftime('%Y%m%d')}.csv"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    # 写入表头
                    writer.writerow(['ID', '姓名', '电话', '微信', '地址', '客户类型', '注册日期'])
                    
                    # 写入数据
                    for c in customers:
                        writer.writerow([
                            c.get('id', ''),
                            c.get('name', ''),
                            c.get('phone', ''),
                            c.get('wechat', ''),
                            c.get('address', ''),
                            c.get('customer_type', ''),
                            c.get('register_date', '')
                        ])
                
                messagebox.showinfo("成功", f"已导出 {len(customers)} 条客户数据到：\n{filename}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{e}")