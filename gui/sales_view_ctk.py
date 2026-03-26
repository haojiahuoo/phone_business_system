# gui/sales_view_ctk.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog

class SalesView:
    def __init__(self, parent, system, main_window=None):
        self.system = system
        self.parent = parent
        self.main_window = main_window  # 保存主窗口引用
        self.order_items = []
        
        self.setup_ui()
        
        # 延迟加载
        self.parent.after(100, self.load_customers)
        self.parent.after(100, self.load_products)
        
    
    def setup_ui(self):
        """设置销售管理界面"""
        
        # 创建主滚动区域
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建订单表单卡片
        self.create_order_card()
        
        # 创建订单列表卡片
        self.create_order_list_card()
    
    def create_order_card(self):
        """创建订单表单卡片"""
        order_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=12,
            fg_color="#1e293b",           # 深色卡片背景
            border_width=1,
            border_color="#334155"         # 深色边框
        )
        order_card.pack(fill="x", padx=0, pady=10)
        
        # 卡片标题
        card_title = ctk.CTkLabel(
            order_card,
            text="📝 创建销售订单",
            font=ctk.CTkFont(family="Microsoft YaHei", size=16, weight="bold"),
            text_color="#f1f5f9"          # 亮色文字
        )
        card_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # 表单区域 - 使用网格布局
        form_frame = ctk.CTkFrame(order_card, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="x")
        
        # 客户选择
        ctk.CTkLabel(form_frame, text="客户:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.customer_combo = ctk.CTkComboBox(form_frame, width=300, font=ctk.CTkFont(size=14))
        self.customer_combo.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkButton(
            form_frame,
            text="新客户",
            command=self.add_customer,
            width=80,
            fg_color="#2196F3"
        ).grid(row=0, column=2, padx=10, pady=10)
        
        # 订单类型
        ctk.CTkLabel(form_frame, text="订单类型:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.order_type = ctk.CTkComboBox(
            form_frame,
            values=["retail", "wholesale", "online"],
            width=300,
            font=ctk.CTkFont(size=14)
        )
        self.order_type.grid(row=1, column=1, padx=10, pady=10)
        self.order_type.set("retail")
        
        # 商品选择
        ctk.CTkLabel(form_frame, text="商品:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.product_combo = ctk.CTkComboBox(form_frame, width=300, font=ctk.CTkFont(size=14))
        self.product_combo.grid(row=2, column=1, padx=10, pady=10)
        
        ctk.CTkButton(
            form_frame,
            text="添加商品",
            command=self.add_order_item,
            width=80,
            fg_color="#4CAF50"
        ).grid(row=2, column=2, padx=10, pady=10)
        
        # 折扣金额
        ctk.CTkLabel(form_frame, text="折扣金额:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.discount = ctk.CTkEntry(form_frame, width=300, font=ctk.CTkFont(size=14))
        self.discount.grid(row=3, column=1, padx=10, pady=10)
        self.discount.insert(0, "0")
        
        # 订单总额
        ctk.CTkLabel(form_frame, text="订单总额:", font=ctk.CTkFont(size=14)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.total_label = ctk.CTkLabel(
            form_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#4CAF50"
        )
        self.total_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # 订单明细表格
        self.create_items_table(order_card)
        
        # 按钮区域
        button_frame = ctk.CTkFrame(order_card, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="创建订单",
            command=self.create_order,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="清空订单",
            command=self.clear_order,
            width=150,
            height=40,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def create_items_table(self, parent):
        """创建订单明细表格"""
        # 表格标题
        columns = ("商品名称", "数量", "单价", "小计")
        
        # 创建表格
        self.items_tree = ctk.CTkScrollableFrame(parent, height=200)
        self.items_tree.pack(fill="x", padx=20, pady=10)
        
        # 标题行
        title_frame = ctk.CTkFrame(self.items_tree, fg_color="#f0f0f0")
        title_frame.pack(fill="x", pady=1)
        
        for i, col in enumerate(columns):
            label = ctk.CTkLabel(
                title_frame,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # 数据行容器
        self.items_container = ctk.CTkFrame(self.items_tree, fg_color="transparent")
        self.items_container.pack(fill="x")
        
        # 存储每行的控件
        self.item_rows = []
    
    def update_items_display(self):
        """更新订单明细显示"""
        # 清除现有行
        for row_widgets in self.item_rows:
            for widget in row_widgets:
                widget.destroy()
        self.item_rows.clear()
        
        # 显示每行数据
        for i, item in enumerate(self.order_items):
            row_frame = ctk.CTkFrame(self.items_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            product_label = ctk.CTkLabel(row_frame, text=item['product_name'], width=150)
            product_label.grid(row=0, column=0, padx=5, pady=2)
            
            qty_label = ctk.CTkLabel(row_frame, text=str(item['quantity']), width=150)
            qty_label.grid(row=0, column=1, padx=5, pady=2)
            
            price_label = ctk.CTkLabel(row_frame, text=f"¥{item['unit_price']:.2f}", width=150)
            price_label.grid(row=0, column=2, padx=5, pady=2)
            
            subtotal_label = ctk.CTkLabel(row_frame, text=f"¥{item['subtotal']:.2f}", width=150)
            subtotal_label.grid(row=0, column=3, padx=5, pady=2)
            
            delete_btn = ctk.CTkButton(
                row_frame,
                text="删除",
                width=60,
                height=25,
                fg_color="#f44336",
                command=lambda idx=i: self.delete_order_item(idx)
            )
            delete_btn.grid(row=0, column=4, padx=5, pady=2)
            
            self.item_rows.append([product_label, qty_label, price_label, subtotal_label, delete_btn])
        
        self.calculate_total()
    
    def create_order_list_card(self):
        """创建订单列表卡片"""
        list_card = ctk.CTkFrame(
            self.main_frame,
            corner_radius=12,
            fg_color="#ffffff",
            border_width=1,
            border_color="#e2e8f0"
        )
        list_card.pack(fill="both", expand=True, padx=0, pady=10)
        
        # 卡片标题
        card_title = ctk.CTkLabel(
            list_card,
            text="📋 历史订单",
            font=ctk.CTkFont(family="Microsoft YaHei", size=16, weight="bold"),
            text_color="#1e293b"
        )
        card_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # 搜索框区域
        search_frame = ctk.CTkFrame(list_card, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=15)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=200, placeholder_text="搜索订单号/客户...")
        self.search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            search_frame,
            text="搜索",
            command=self.search_orders,
            width=80
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            search_frame,
            text="刷新",
            command=self.refresh_orders,
            width=80,
            fg_color="#2196F3"
        ).pack(side="left", padx=5)
        
        # 订单表格
        columns = ("订单号", "客户", "类型", "总金额", "已付", "状态", "日期")
        self.orders_tree = ctk.CTkScrollableFrame(list_card, height=300)
        self.orders_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 标题行
        title_frame = ctk.CTkFrame(self.orders_tree, fg_color="#f0f0f0")
        title_frame.pack(fill="x", pady=1)
        
        for i, col in enumerate(columns):
            label = ctk.CTkLabel(
                title_frame,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=120
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # 数据行容器
        self.orders_container = ctk.CTkFrame(self.orders_tree, fg_color="transparent")
        self.orders_container.pack(fill="x")
        
        self.order_rows = []
    
    

    def load_customers(self):
        """加载客户列表"""
        try:
            print("🔄 正在加载客户列表...")  # 添加这行
            customers = self.system.get_all_customers()
            print(f"📋 获取到 {len(customers)} 个客户")  # 添加这行
            
            if customers:
                customer_list = []
                for c in customers:
                    customer_id = c.get('id', '')
                    customer_name = c.get('name', '')
                    customer_phone = c.get('phone', '')
                    customer_text = f"{customer_id}-{customer_name} ({customer_phone})"
                    customer_list.append(customer_text)
                    print(f"  添加: {customer_text}")  # 添加这行
                
                # 更新 Combobox
                self.customer_combo.configure(values=customer_list)
                print(f"✅ Combobox 已更新，共 {len(customer_list)} 个选项")  # 添加这行
                
                if customer_list:
                    self.customer_combo.set(customer_list[0])
                    print(f"✅ 默认选择: {customer_list[0]}")  # 添加这行
            else:
                self.customer_combo.configure(values=[])
                print("⚠️ 没有客户数据")  # 添加这行
                
        except Exception as e:
            print(f"❌ 加载客户失败: {e}")
            import traceback
            traceback.print_exc()
    
    def load_products(self):
        """加载商品列表"""
        products = self.system.get_all_inventory()
        available_products = [p for p in products if p.get('quantity', 0) > 0]
        self.product_combo['values'] = [f"{p.get('id')}-{p.get('product_name')} (库存:{p.get('quantity')})" for p in available_products]
    
    def add_customer(self):
        """添加客户对话框"""
        print("🔧 打开添加客户对话框")
        
        dialog = ctk.CTkToplevel()
        dialog.title("添加客户")
        dialog.geometry("450x550")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # 使窗口居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 450) // 2
        y = (dialog.winfo_screenheight() - 550) // 2
        dialog.geometry(f"450x550+{x}+{y}")
        
        fields = {}
        labels = ['姓名', '电话', '微信', '地址', '客户类型']
        types = ['零售客户', '批发客户', '网络客户']
        type_map = {'零售客户': 'retail', '批发客户': 'wholesale', '网络客户': 'online'}
        
        # 创建滚动区域
        scroll_frame = ctk.CTkScrollableFrame(dialog, height=400)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, label in enumerate(labels):
            ctk.CTkLabel(scroll_frame, text=f"{label}:", font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, padx=10, pady=10, sticky="e"
            )
            
            if label == '客户类型':
                entry = ctk.CTkComboBox(scroll_frame, values=types, width=250, font=ctk.CTkFont(size=14))
                entry.set('零售客户')
            elif label == '地址':
                entry = ctk.CTkTextbox(scroll_frame, width=250, height=80, font=ctk.CTkFont(size=14))
            else:
                entry = ctk.CTkEntry(scroll_frame, width=250, font=ctk.CTkFont(size=14))
            
            entry.grid(row=i, column=1, padx=10, pady=10)
            fields[label] = entry
        
        def save():
            try:
                print("💾 开始保存客户...")
                
                name = fields['姓名'].get().strip()
                phone = fields['电话'].get().strip()
                wechat = fields['微信'].get().strip()
                
                # 获取地址
                if isinstance(fields['地址'], ctk.CTkTextbox):
                    address = fields['地址'].get("1.0", "end-1c").strip()
                else:
                    address = fields['地址'].get().strip()
                
                # 获取客户类型（中文转英文）
                customer_type_cn = fields['客户类型'].get()
                customer_type = type_map.get(customer_type_cn, 'retail')
                
                print(f"   姓名: {name}")
                print(f"   电话: {phone}")
                print(f"   类型: {customer_type_cn} -> {customer_type}")
                
                # 验证必填字段
                if not name:
                    messagebox.showwarning("警告", "请填写客户姓名")
                    return
                
                if not phone:
                    messagebox.showwarning("警告", "请填写客户电话")
                    return
                
                # 添加客户
                result = self.system.add_customer(
                    name=name,
                    phone=phone,
                    wechat=wechat,
                    address=address,
                    customer_type=customer_type
                )
                
                print(f"   添加结果: {result}")
                
                if result:
                    messagebox.showinfo("成功", f"客户 '{name}' 添加成功！")
                    dialog.destroy()
                    
                    print("🔄 正在刷新客户列表...")
                    # 重新加载客户列表
                    self.load_customers()
                    print("✅ 客户列表刷新完成")
                else:
                    messagebox.showerror("错误", "添加客户失败，请检查数据库")
                    
            except Exception as e:
                print(f"❌ 保存失败: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror("错误", f"添加失败：{e}")
        
        # 按钮区域 - 确保有保存按钮
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # 保存按钮
        save_btn = ctk.CTkButton(
            button_frame,
            text="✅ 保存",
            command=save,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50"
        )
        save_btn.pack(side="left", padx=10)
        
        # 取消按钮
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ 取消",
            command=dialog.destroy,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#f44336"
        )
        cancel_btn.pack(side="left", padx=10)
        
        print("✅ 对话框已创建，等待用户输入")
        
    def add_order_item(self):
        """添加订单明细"""
        product_str = self.product_combo.get()
        if not product_str:
            messagebox.showwarning("警告", "请选择商品")
            return
        
        product_id = int(product_str.split('-')[0])
        product = self.system.get_product_by_id(product_id)
        
        if product:
            quantity = simpledialog.askinteger(
                "数量",
                f"请输入购买数量（最多{product.get('quantity')}）：",
                minvalue=1,
                maxvalue=product.get('quantity')
            )
            if quantity:
                # 检查是否已添加
                for item in self.order_items:
                    if item['inventory_id'] == product_id:
                        item['quantity'] += quantity
                        item['subtotal'] = item['unit_price'] * item['quantity']
                        self.update_items_display()
                        messagebox.showinfo("成功", f"已增加 {quantity} 件 {product.get('product_name')}")
                        return
                
                self.order_items.append({
                    'inventory_id': product_id,
                    'product_name': product.get('product_name'),
                    'quantity': quantity,
                    'unit_price': product.get('sell_price'),
                    'subtotal': product.get('sell_price') * quantity
                })
                
                self.update_items_display()
                messagebox.showinfo("成功", f"已添加 {quantity} 件 {product.get('product_name')}")
    
    def delete_order_item(self, index):
        """删除订单明细"""
        if index < len(self.order_items):
            del self.order_items[index]
            self.update_items_display()
            self.calculate_total()
    
    def calculate_total(self):
        """计算订单总额"""
        total = sum(item['subtotal'] for item in self.order_items)
        discount = float(self.discount.get() or 0)
        final_total = total - discount
        self.total_label.configure(text=f"¥{final_total:.2f}")
    
    def clear_order(self):
        """清空订单"""
        if self.order_items:
            if messagebox.askyesno("确认", "确定要清空当前订单吗？"):
                self.order_items = []
                self.update_items_display()
                self.discount.delete(0, "end")
                self.discount.insert(0, "0")
                self.total_label.configure(text="¥0.00")
    
    def create_order(self):
        """创建订单"""
        if not self.order_items:
            messagebox.showwarning("警告", "请至少添加一个商品")
            return
        
        customer_str = self.customer_combo.get()
        if not customer_str:
            messagebox.showwarning("警告", "请选择客户")
            return
        
        customer_id = int(customer_str.split('-')[0])
        order_type = self.order_type.get()
        discount = float(self.discount.get() or 0)
        
        items = [{'inventory_id': item['inventory_id'], 'quantity': item['quantity']} for item in self.order_items]
        
        try:
            order_no, amount = self.system.create_sales_order(
                customer_id=customer_id,
                order_type=order_type,
                items=items,
                discount=discount
            )
            
            messagebox.showinfo("成功", f"订单 {order_no} 创建成功！\n金额：¥{amount:.2f}")
            self.clear_order()
            self.refresh_orders()
            
        except Exception as e:
            messagebox.showerror("错误", f"创建订单失败：{e}")
    
    def refresh_orders(self):
        """刷新订单列表"""
        orders = self.system.get_all_sales_orders()
        
        # 清除现有行
        for row_widgets in self.order_rows:
            for widget in row_widgets:
                widget.destroy()
        self.order_rows.clear()
        
        status_map = {'pending': '待付款', 'paid': '已付款', 'completed': '已完成'}
        
        for order in orders:
            row_frame = ctk.CTkFrame(self.orders_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=1)
            
            order_no = order.get('order_no', '')
            customer_name = order.get('customer_name', '')
            order_type = order.get('order_type', '')
            actual_amount = order.get('actual_amount', 0)
            paid_amount = order.get('paid_amount', 0)
            status = order.get('status', 'pending')
            create_time = order.get('create_time', '')
            
            if create_time and hasattr(create_time, 'strftime'):
                date_str = create_time.strftime('%Y-%m-%d')
            else:
                date_str = str(create_time)[:10] if create_time else ''
            
            widgets = []
            for i, value in enumerate([order_no, customer_name, order_type, f"¥{actual_amount:.2f}", f"¥{paid_amount:.2f}", status_map.get(status, status), date_str]):
                label = ctk.CTkLabel(row_frame, text=value, width=120)
                label.grid(row=0, column=i, padx=5, pady=2)
                widgets.append(label)
            
            self.order_rows.append(widgets)
    
    def search_orders(self):
        """搜索订单"""
        keyword = self.search_entry.get()
        if not keyword:
            self.refresh_orders()
            return
        
        orders = self.system.get_all_sales_orders()
        
        # 清除现有行
        for row_widgets in self.order_rows:
            for widget in row_widgets:
                widget.destroy()
        self.order_rows.clear()
        
        status_map = {'pending': '待付款', 'paid': '已付款', 'completed': '已完成'}
        
        for order in orders:
            order_no = order.get('order_no', '')
            customer_name = order.get('customer_name', '')
            
            if keyword in order_no or keyword in customer_name:
                row_frame = ctk.CTkFrame(self.orders_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=1)
                
                actual_amount = order.get('actual_amount', 0)
                paid_amount = order.get('paid_amount', 0)
                status = order.get('status', 'pending')
                create_time = order.get('create_time', '')
                
                if create_time and hasattr(create_time, 'strftime'):
                    date_str = create_time.strftime('%Y-%m-%d')
                else:
                    date_str = str(create_time)[:10] if create_time else ''
                
                widgets = []
                values = [order_no, customer_name, order.get('order_type', ''), f"¥{actual_amount:.2f}", f"¥{paid_amount:.2f}", status_map.get(status, status), date_str]
                for i, value in enumerate(values):
                    label = ctk.CTkLabel(row_frame, text=value, width=120)
                    label.grid(row=0, column=i, padx=5, pady=2)
                    widgets.append(label)
                
                self.order_rows.append(widgets)