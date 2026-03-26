# gui/inventory_view_ctk.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog

class InventoryView:
    def __init__(self, parent, system):
        self.system = system
        self.parent = parent
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """设置库存管理界面"""
        
        # 创建主滚动区域
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建工具栏卡片
        self.create_toolbar_card()
        
        # 创建商品列表卡片
        self.create_inventory_card()
    
    def create_toolbar_card(self):
        """创建工具栏卡片"""
        toolbar_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        toolbar_card.pack(fill="x", padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            toolbar_card,
            text="📦 库存管理",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=10)
        
        # 工具栏
        toolbar_frame = ctk.CTkFrame(toolbar_card, fg_color="transparent")
        toolbar_frame.pack(fill="x", padx=20, pady=10)
        
        # 搜索框
        ctk.CTkLabel(toolbar_frame, text="搜索:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(toolbar_frame, textvariable=self.search_var, width=200, placeholder_text="商品名称/编码...")
        self.search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar_frame,
            text="搜索",
            command=self.search,
            width=80
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar_frame,
            text="显示全部",
            command=self.refresh,
            width=100,
            fg_color="#2196F3"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar_frame,
            text="➕ 添加商品",
            command=self.add_product,
            width=120,
            fg_color="#4CAF50"
        ).pack(side="right", padx=5)
        
        # 统计信息
        stats_frame = ctk.CTkFrame(toolbar_card, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        self.total_count_label = ctk.CTkLabel(
            stats_frame,
            text="总商品数: 0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.total_count_label.pack(side="left", padx=10)
        
        self.total_value_label = ctk.CTkLabel(
            stats_frame,
            text="库存总价值: ¥0.00",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.total_value_label.pack(side="left", padx=10)
        
        self.warning_count_label = ctk.CTkLabel(
            stats_frame,
            text="⚠️ 库存预警: 0",
            font=ctk.CTkFont(size=12),
            text_color="#ff9800"
        )
        self.warning_count_label.pack(side="left", padx=10)
    
    def create_inventory_card(self):
        """创建商品列表卡片"""
        inventory_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        inventory_card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            inventory_card,
            text="📋 商品列表",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # 定义列名
        self.columns = ("ID", "商品编码", "商品名称", "品牌", "型号", "库存", "成本价", "售价", "位置")
        
        # 创建表格容器
        self.table_frame = ctk.CTkScrollableFrame(inventory_card, height=500)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题行
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#f0f0f0")
        header_frame.pack(fill="x", pady=1)
        
        for i, col in enumerate(self.columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=100
            )
            label.grid(row=0, column=i, padx=5, pady=8)
        
        # 数据行容器
        self.data_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.data_container.pack(fill="x")
        
        self.data_rows = []
    
    def update_table(self, products):
        """更新表格显示"""
        # 清除现有行
        for row_widgets in self.data_rows:
            for widget in row_widgets:
                widget.destroy()
        self.data_rows.clear()
        
        # 统计信息
        total_value = 0
        warning_count = 0
        
        for product in products:
            row_frame = ctk.CTkFrame(self.data_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=1)
            
            # 检查库存预警
            quantity = product.get('quantity', 0)
            min_stock = product.get('min_stock', 0)
            is_warning = quantity <= min_stock and min_stock > 0
            
            if is_warning:
                warning_count += 1
                row_frame.configure(fg_color="#fff3e0")
            
            # 计算库存价值
            total_value += product.get('quantity', 0) * product.get('cost_price', 0)
            
            values = [
                product.get('id', ''),
                product.get('product_code', ''),
                product.get('product_name', ''),
                product.get('brand', ''),
                product.get('model', ''),
                product.get('quantity', 0),
                f"¥{product.get('cost_price', 0):.2f}",
                f"¥{product.get('sell_price', 0):.2f}",
                product.get('location', '')
            ]
            
            widgets = []
            for i, value in enumerate(values):
                # 库存数量特殊处理颜色
                if i == 5 and is_warning:
                    text_color = "#f44336"
                    font = ctk.CTkFont(size=12, weight="bold")
                else:
                    text_color = "#333333"
                    font = ctk.CTkFont(size=12)
                
                label = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    width=100,
                    text_color=text_color,
                    font=font
                )
                label.grid(row=0, column=i, padx=5, pady=6)
                widgets.append(label)
            
            # 添加操作按钮
            edit_btn = ctk.CTkButton(
                row_frame,
                text="编辑库存",
                width=80,
                height=28,
                fg_color="#FF9800",
                command=lambda pid=product.get('id'), pname=product.get('product_name'), qty=product.get('quantity'): self.edit_stock(pid, pname, qty)
            )
            edit_btn.grid(row=0, column=len(self.columns), padx=5, pady=6)
            widgets.append(edit_btn)
            
            self.data_rows.append(widgets)
        
        # 更新统计信息
        self.total_count_label.configure(text=f"总商品数: {len(products)}")
        self.total_value_label.configure(text=f"库存总价值: ¥{total_value:.2f}")
        self.warning_count_label.configure(text=f"⚠️ 库存预警: {warning_count}")
    
    def refresh(self):
        """刷新商品列表"""
        products = self.system.get_all_inventory()
        self.update_table(products)
    
    def search(self):
        """搜索商品"""
        keyword = self.search_var.get()
        if keyword:
            products = self.system.search_inventory(keyword)
        else:
            products = self.system.get_all_inventory()
        self.update_table(products)
    
    def add_product(self):
        """添加商品对话框"""
        dialog = ctk.CTkToplevel()
        dialog.title("添加商品")
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
            ('商品编码', 'entry'), ('商品名称', 'entry'), ('类别', 'entry'),
            ('品牌', 'entry'), ('型号', 'entry'), ('成本价', 'entry'),
            ('售价', 'entry'), ('批发价', 'entry'), ('初始库存', 'entry'),
            ('位置', 'entry'), ('最低库存', 'entry')
        ]
        
        scroll_frame = ctk.CTkScrollableFrame(dialog, height=450)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, (label, _) in enumerate(labels):
            ctk.CTkLabel(scroll_frame, text=f"{label}:", font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, padx=10, pady=8, sticky="e"
            )
            entry = ctk.CTkEntry(scroll_frame, width=250, font=ctk.CTkFont(size=14))
            entry.grid(row=i, column=1, padx=10, pady=8)
            fields[label] = entry
        
        def save():
            try:
                self.system.add_inventory(
                    product_code=fields['商品编码'].get(),
                    product_name=fields['商品名称'].get(),
                    category=fields['类别'].get(),
                    brand=fields['品牌'].get(),
                    model=fields['型号'].get(),
                    cost_price=float(fields['成本价'].get() or 0),
                    sell_price=float(fields['售价'].get() or 0),
                    wholesale_price=float(fields['批发价'].get() or 0),
                    quantity=int(fields['初始库存'].get() or 0),
                    location=fields['位置'].get(),
                    min_stock=int(fields['最低库存'].get() or 0)
                )
                messagebox.showinfo("成功", "商品添加成功！")
                dialog.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{e}")
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="保存",
            command=save,
            width=120,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="取消",
            command=dialog.destroy,
            width=120,
            height=35,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def edit_stock(self, product_id, product_name, current_stock):
        """编辑库存数量"""
        dialog = ctk.CTkToplevel()
        dialog.title("修改库存")
        dialog.geometry("400x250")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # 使窗口居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 250) // 2
        dialog.geometry(f"400x250+{x}+{y}")
        
        # 商品信息
        info_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        info_frame.pack(pady=20)
        
        ctk.CTkLabel(
            info_frame,
            text=f"商品名称: {product_name}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text=f"当前库存: {current_stock}",
            font=ctk.CTkFont(size=14)
        ).pack(pady=5)
        
        # 新库存输入
        input_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        input_frame.pack(pady=20)
        
        ctk.CTkLabel(input_frame, text="新库存数量:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        quantity_entry = ctk.CTkEntry(input_frame, width=150, font=ctk.CTkFont(size=14))
        quantity_entry.pack(side="left", padx=5)
        quantity_entry.insert(0, str(current_stock))
        
        def save():
            try:
                new_quantity = int(quantity_entry.get())
                change = new_quantity - current_stock
                self.system.update_stock(product_id, change)
                messagebox.showinfo("成功", f"库存已更新为：{new_quantity}")
                dialog.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("错误", f"更新失败：{e}")
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="确定",
            command=save,
            width=100,
            height=35
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="取消",
            command=dialog.destroy,
            width=100,
            height=35,
            fg_color="gray"
        ).pack(side="left", padx=10)