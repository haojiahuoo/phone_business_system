# gui/sales_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class SalesView:
    def __init__(self, parent, system):
        self.system = system
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="销售管理")
        
        # 存储订单明细
        self.order_items = []
        
        self.setup_ui()
        self.load_customers()
        self.load_products()
    
    def setup_ui(self):
        # 创建销售订单区域
        ttk.Label(self.frame, text="创建销售订单", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # 表单框架
        form_frame = ttk.LabelFrame(self.frame, text="订单信息", padding=10)
        form_frame.pack(pady=10, padx=20, fill='x')
        
        # 第1行：客户选择
        ttk.Label(form_frame, text="客户:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.customer_combo = ttk.Combobox(form_frame, width=35)
        self.customer_combo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(form_frame, text="新客户", command=self.add_customer_dialog).grid(row=0, column=2, padx=5, pady=5)
        
        # 第2行：订单类型
        ttk.Label(form_frame, text="订单类型:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.order_type = ttk.Combobox(form_frame, values=['retail', 'wholesale', 'online'], width=33)
        self.order_type.grid(row=1, column=1, padx=5, pady=5)
        self.order_type.set('retail')
        self.order_type.bind('<<ComboboxSelected>>', self.on_order_type_change)
        
        # 第3行：平台（网络销售时显示）
        ttk.Label(form_frame, text="平台:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.platform = ttk.Entry(form_frame, width=37)
        self.platform.grid(row=2, column=1, padx=5, pady=5)
        self.platform.grid_remove()  # 默认隐藏
        
        # 第4行：支付方式
        ttk.Label(form_frame, text="支付方式:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.payment_method = ttk.Combobox(form_frame, values=['现金', '微信', '支付宝', '银行卡'], width=33)
        self.payment_method.grid(row=3, column=1, padx=5, pady=5)
        self.payment_method.set('现金')
        
        # 第5行：商品选择
        ttk.Label(form_frame, text="商品:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.product_combo = ttk.Combobox(form_frame, width=35)
        self.product_combo.grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(form_frame, text="添加商品", command=self.add_order_item).grid(row=4, column=2, padx=5, pady=5)
        
        # 订单明细列表
        columns = ('商品名称', '数量', '单价', '小计')
        self.order_items_tree = ttk.Treeview(form_frame, columns=columns, show='headings', height=6)
        for col in columns:
            self.order_items_tree.heading(col, text=col)
            self.order_items_tree.column(col, width=120)
        self.order_items_tree.grid(row=5, column=0, columnspan=3, pady=10, sticky='ew')
        
        # 右键菜单
        self.create_context_menu()
        
        # 折扣和总计
        ttk.Label(form_frame, text="折扣金额:").grid(row=6, column=0, sticky='e', padx=5, pady=5)
        self.discount = ttk.Entry(form_frame, width=37)
        self.discount.grid(row=6, column=1, padx=5, pady=5)
        self.discount.insert(0, "0")
        self.discount.bind('<KeyRelease>', self.calculate_total)
        
        ttk.Label(form_frame, text="订单总额:").grid(row=7, column=0, sticky='e', padx=5, pady=5)
        self.total_label = ttk.Label(form_frame, text="0.00", font=('Arial', 14, 'bold'), foreground='green')
        self.total_label.grid(row=7, column=1, sticky='w', padx=5, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="创建订单", command=self.create_order, width=15).pack(side='left', padx=10)
        ttk.Button(button_frame, text="清空订单", command=self.clear_order, width=15).pack(side='left', padx=10)
        
        # 订单列表区域
        self.create_order_list_frame()
    
    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.order_items_tree, tearoff=0)
        self.context_menu.add_command(label="删除", command=self.delete_order_item)
        self.order_items_tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        item = self.order_items_tree.identify_row(event.y)
        if item:
            self.order_items_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def delete_order_item(self):
        """删除订单明细"""
        selected = self.order_items_tree.selection()
        if selected:
            index = self.order_items_tree.index(selected[0])
            del self.order_items[index]
            self.order_items_tree.delete(selected[0])
            self.calculate_total()
            messagebox.showinfo("成功", "商品已从订单中移除")
    
    def create_order_list_frame(self):
        """创建订单列表区域"""
        list_frame = ttk.LabelFrame(self.frame, text="历史订单", padding=10)
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # 搜索框
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', pady=5)
        
        ttk.Label(search_frame, text="搜索:").pack(side='left', padx=5)
        self.order_search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.order_search_var, width=20).pack(side='left', padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_orders).pack(side='left', padx=5)
        ttk.Button(search_frame, text="刷新", command=self.refresh_orders).pack(side='left', padx=5)
        
        # 订单列表
        columns = ('订单号', '客户', '类型', '总金额', '已付', '状态', '日期')
        self.orders_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 双击查看详情
        self.orders_tree.bind('<Double-Button-1>', self.view_order_detail)
        
        # 加载订单
        self.refresh_orders()
    
    def on_order_type_change(self, event):
        """订单类型改变时的处理"""
        if self.order_type.get() == 'online':
            self.platform.grid()
        else:
            self.platform.grid_remove()
    
    def load_customers(self):
        """加载客户列表"""
        customers = self.system.get_all_customers()
        self.customer_combo['values'] = [f"{c[0]}-{c[1]} ({c[5]})" for c in customers]
    
    def load_products(self):
        """加载商品列表"""
        products = self.system.get_all_inventory()
        available_products = [p for p in products if p[8] > 0]  # 只显示有库存的
        self.product_combo['values'] = [f"{p[0]}-{p[2]} (库存:{p[8]} 售价:¥{p[10]})" for p in available_products]
    
    def add_customer_dialog(self):
        """添加客户对话框"""
        dialog = tk.Toplevel()
        dialog.title("添加客户")
        dialog.geometry("350x350")
        dialog.transient(self.frame.winfo_toplevel())
        dialog.grab_set()
        
        fields = {}
        labels = ['姓名', '电话', '微信', '地址', '客户类型']
        types = ['retail', 'wholesale', 'online']
        
        for i, label in enumerate(labels):
            ttk.Label(dialog, text=f"{label}:").grid(row=i, column=0, padx=10, pady=5, sticky='e')
            if label == '客户类型':
                entry = ttk.Combobox(dialog, values=types, width=27)
                entry.set('retail')
            elif label == '地址':
                entry = tk.Text(dialog, width=30, height=3)
                entry.grid(row=i, column=1, padx=10, pady=5)
                fields[label] = entry
                continue
            else:
                entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            fields[label] = entry
        
        def save():
            try:
                address = fields['地址'].get('1.0', 'end-1c') if isinstance(fields['地址'], tk.Text) else fields['地址'].get()
                self.system.add_customer(
                    name=fields['姓名'].get(),
                    phone=fields['电话'].get(),
                    wechat=fields['微信'].get(),
                    address=address,
                    customer_type=fields['客户类型'].get()
                )
                messagebox.showinfo("成功", "客户添加成功！")
                dialog.destroy()
                self.load_customers()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{e}")
        
        ttk.Button(dialog, text="保存", command=save).grid(row=len(labels), column=1, pady=20)
    
    def add_order_item(self):
        """添加订单明细"""
        product_str = self.product_combo.get()
        if not product_str:
            messagebox.showwarning("警告", "请选择商品")
            return
        
        product_id = int(product_str.split('-')[0])
        
        # 获取商品信息
        self.system.cursor.execute('SELECT product_name, sell_price, quantity FROM inventory WHERE id = ?', 
                                   (product_id,))
        product = self.system.cursor.fetchone()
        
        if product:
            # 弹出数量对话框
            quantity = simpledialog.askinteger("数量", f"请输入购买数量（最多{product[2]}）：", 
                                               minvalue=1, maxvalue=product[2])
            if quantity:
                # 检查是否已添加相同商品
                for item in self.order_items:
                    if item['inventory_id'] == product_id:
                        # 更新数量
                        item['quantity'] += quantity
                        item['subtotal'] = item['unit_price'] * item['quantity']
                        self.update_order_items_tree()
                        self.calculate_total()
                        messagebox.showinfo("成功", f"已增加 {quantity} 件 {product[0]}")
                        return
                
                # 添加新商品
                self.order_items.append({
                    'inventory_id': product_id,
                    'product_name': product[0],
                    'quantity': quantity,
                    'unit_price': product[1],
                    'subtotal': product[1] * quantity
                })
                
                self.update_order_items_tree()
                self.calculate_total()
                messagebox.showinfo("成功", f"已添加 {quantity} 件 {product[0]}")
    
    def update_order_items_tree(self):
        """更新订单明细树形视图"""
        # 清空现有数据
        for item in self.order_items_tree.get_children():
            self.order_items_tree.delete(item)
        
        # 重新添加
        for item in self.order_items:
            self.order_items_tree.insert('', 'end', values=(
                item['product_name'], 
                item['quantity'], 
                f"¥{item['unit_price']:.2f}", 
                f"¥{item['subtotal']:.2f}"
            ))
    
    def calculate_total(self, event=None):
        """计算订单总额"""
        total = sum(item['subtotal'] for item in self.order_items)
        discount = float(self.discount.get() or 0)
        final_total = total - discount
        self.total_label.config(text=f"¥{final_total:.2f}")
    
    def clear_order(self):
        """清空订单"""
        if self.order_items:
            if messagebox.askyesno("确认", "确定要清空当前订单吗？"):
                self.order_items = []
                self.update_order_items_tree()
                self.discount.delete(0, 'end')
                self.discount.insert(0, "0")
                self.total_label.config(text="¥0.00")
                self.product_combo.set('')
    
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
        payment_method = self.payment_method.get()
        platform = self.platform.get() if order_type == 'online' and self.platform.get() else None
        
        items = [{'inventory_id': item['inventory_id'], 'quantity': item['quantity']} 
                 for item in self.order_items]
        
        try:
            order_no, amount = self.system.create_sales_order(
                customer_id=customer_id,
                order_type=order_type,
                items=items,
                discount=discount,
                platform=platform,
                payment_method=payment_method
            )
            
            # 询问是否收款
            result = messagebox.askyesno("收款", 
                                        f"订单创建成功！\n订单号：{order_no}\n金额：¥{amount:.2f}\n\n是否现在收款？")
            if result:
                amount_paid = simpledialog.askfloat("收款", "请输入收款金额：", 
                                                    initialvalue=amount, minvalue=0, maxvalue=amount)
                if amount_paid and amount_paid > 0:
                    # 获取订单ID
                    self.system.cursor.execute('SELECT id FROM sales_orders WHERE order_no = ?', (order_no,))
                    order_id = self.system.cursor.fetchone()[0]
                    self.system.receive_payment(order_id, amount_paid)
                    messagebox.showinfo("成功", f"收款成功！收款金额：¥{amount_paid:.2f}")
            
            # 清空订单
            self.clear_order()
            
            # 刷新库存和订单列表
            self.load_products()
            self.refresh_orders()
            
            messagebox.showinfo("成功", f"订单 {order_no} 创建成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"创建订单失败：{e}")
    
    def refresh_orders(self):
        """刷新订单列表"""
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        orders = self.system.get_all_sales_orders()
        status_map = {'pending': '待付款', 'paid': '已付款', 'shipped': '已发货', 'completed': '已完成'}
        
        for order in orders:
            status_text = status_map.get(order[10], order[10])
            self.orders_tree.insert('', 'end', values=(
                order[1],  # 订单号
                order[13] if len(order) > 13 else '',  # 客户名
                order[3],  # 订单类型
                f"¥{order[7]:.2f}",  # 实际金额
                f"¥{order[8]:.2f}",  # 已付金额
                status_text,  # 状态
                order[11][:10] if order[11] else ''  # 日期
            ))
    
    def search_orders(self):
        """搜索订单"""
        keyword = self.order_search_var.get()
        if not keyword:
            self.refresh_orders()
            return
        
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # 简单的前端搜索
        orders = self.system.get_all_sales_orders()
        status_map = {'pending': '待付款', 'paid': '已付款', 'shipped': '已发货', 'completed': '已完成'}
        
        for order in orders:
            order_no = order[1]
            customer_name = order[13] if len(order) > 13 else ''
            
            if keyword in order_no or keyword in customer_name:
                status_text = status_map.get(order[10], order[10])
                self.orders_tree.insert('', 'end', values=(
                    order_no, customer_name, order[3], 
                    f"¥{order[7]:.2f}", f"¥{order[8]:.2f}", 
                    status_text, order[11][:10] if order[11] else ''
                ))
    
    def view_order_detail(self, event):
        """查看订单详情"""
        selected = self.orders_tree.selection()
        if not selected:
            return
        
        values = self.orders_tree.item(selected[0], 'values')
        order_no = values[0]
        
        # 获取订单详情
        self.system.cursor.execute('''
            SELECT soi.*, i.product_name 
            FROM sales_order_items soi
            JOIN inventory i ON soi.inventory_id = i.id
            WHERE soi.order_id = (SELECT id FROM sales_orders WHERE order_no = ?)
        ''', (order_no,))
        
        items = self.system.cursor.fetchall()
        
        # 创建详情窗口
        detail_dialog = tk.Toplevel()
        detail_dialog.title(f"订单详情 - {order_no}")
        detail_dialog.geometry("500x400")
        detail_dialog.transient(self.frame.winfo_toplevel())
        
        # 显示订单信息
        info_text = f"订单号：{order_no}\n客户：{values[1]}\n类型：{values[2]}\n总额：{values[3]}\n状态：{values[5]}"
        ttk.Label(detail_dialog, text=info_text, font=('Arial', 10)).pack(pady=10)
        
        # 商品列表
        columns = ('商品名称', '数量', '单价', '小计')
        tree = ttk.Treeview(detail_dialog, columns=columns, show='headings', height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for item in items:
            tree.insert('', 'end', values=(
                item[5], item[3], f"¥{item[4]:.2f}", f"¥{item[4] * item[3]:.2f}"
            ))
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Button(detail_dialog, text="关闭", command=detail_dialog.destroy).pack(pady=10)