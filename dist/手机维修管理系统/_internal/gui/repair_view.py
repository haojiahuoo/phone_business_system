# gui/repair_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class RepairView:
    def __init__(self, parent, system):
        self.system = system
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="维修管理")
        
        self.setup_ui()
        self.load_customers()
        self.refresh_orders()
    
    def setup_ui(self):
        # 创建维修订单区域
        ttk.Label(self.frame, text="创建维修订单", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # 表单框架
        form_frame = ttk.LabelFrame(self.frame, text="维修信息", padding=10)
        form_frame.pack(pady=10, padx=20, fill='x')
        
        self.fields = {}
        labels = ['客户', '设备品牌', '设备型号', 'IMEI', '问题描述', 
                  '维修类型', '维修费', '配件费', '定金', '备注']
        
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=f"{label}:").grid(row=i, column=0, sticky='e', padx=5, pady=5)
            
            if label == '客户':
                self.fields[label] = ttk.Combobox(form_frame, width=40)
                self.fields[label].grid(row=i, column=1, padx=5, pady=5, columnspan=2)
            elif label == '维修类型':
                self.fields[label] = ttk.Combobox(form_frame, values=['hardware', 'software', 'water_damage'], width=38)
                self.fields[label].set('hardware')
                self.fields[label].grid(row=i, column=1, padx=5, pady=5, columnspan=2)
            elif label == '问题描述':
                self.fields[label] = tk.Text(form_frame, width=40, height=3)
                self.fields[label].grid(row=i, column=1, padx=5, pady=5, columnspan=2)
            elif label == '备注':
                self.fields[label] = tk.Text(form_frame, width=40, height=2)
                self.fields[label].grid(row=i, column=1, padx=5, pady=5, columnspan=2)
            else:
                self.fields[label] = ttk.Entry(form_frame, width=42)
                self.fields[label].grid(row=i, column=1, padx=5, pady=5, columnspan=2)
        
        # 按钮
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="创建维修订单", command=self.create_repair_order, width=15).pack(side='left', padx=10)
        ttk.Button(button_frame, text="清空表单", command=self.clear_form, width=15).pack(side='left', padx=10)
        
        # 订单列表区域
        self.create_order_list_frame()
    
    def create_order_list_frame(self):
        """创建订单列表区域"""
        list_frame = ttk.LabelFrame(self.frame, text="维修订单列表", padding=10)
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # 状态筛选
        filter_frame = ttk.Frame(list_frame)
        filter_frame.pack(fill='x', pady=5)
        
        ttk.Label(filter_frame, text="状态筛选:").pack(side='left', padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['全部', 'pending', 'repairing', 'completed', 'delivered'], width=15)
        self.status_filter.set('全部')
        self.status_filter.pack(side='left', padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_orders())
        
        ttk.Button(filter_frame, text="刷新", command=self.refresh_orders).pack(side='left', padx=10)
        ttk.Button(filter_frame, text="完成维修", command=self.complete_repair).pack(side='left', padx=10)
        ttk.Button(filter_frame, text="交付客户", command=self.deliver_phone).pack(side='left', padx=10)
        
        # 订单列表
        columns = ('订单号', '客户', '设备', '故障', '总费用', '定金', '状态', '接修日期')
        self.orders_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 双击查看详情
        self.orders_tree.bind('<Double-Button-1>', self.view_repair_detail)
    
    def load_customers(self):
        """加载客户列表"""
        customers = self.system.get_all_customers()
        self.fields['客户']['values'] = [f"{c[0]}-{c[1]} ({c[5]})" for c in customers]
    
    def clear_form(self):
        """清空表单"""
        for key, field in self.fields.items():
            if isinstance(field, ttk.Entry):
                field.delete(0, 'end')
            elif isinstance(field, tk.Text):
                field.delete('1.0', 'end')
            elif isinstance(field, ttk.Combobox):
                if key != '维修类型':
                    field.set('')
        
        self.fields['维修类型'].set('hardware')
    
    def create_repair_order(self):
        """创建维修订单"""
        customer_str = self.fields['客户'].get()
        if not customer_str:
            messagebox.showwarning("警告", "请选择客户")
            return
        
        try:
            customer_id = int(customer_str.split('-')[0])
            repair_cost = float(self.fields['维修费'].get() or 0)
            parts_cost = float(self.fields['配件费'].get() or 0)
            deposit = float(self.fields['定金'].get() or 0)
            
            problem_desc = self.fields['问题描述'].get('1.0', 'end-1c')
            notes = self.fields['备注'].get('1.0', 'end-1c')
            
            order_no = self.system.create_repair_order(
                customer_id=customer_id,
                device_brand=self.fields['设备品牌'].get(),
                device_model=self.fields['设备型号'].get(),
                problem_desc=problem_desc,
                repair_type=self.fields['维修类型'].get(),
                repair_cost=repair_cost,
                parts_cost=parts_cost,
                deposit=deposit
            )
            
            # 如果有备注，更新备注
            if notes:
                self.system.cursor.execute('UPDATE repair_orders SET notes = ? WHERE order_no = ?', 
                                           (notes, order_no))
                self.system.conn.commit()
            
            messagebox.showinfo("成功", f"维修订单创建成功！\n订单号：{order_no}")
            self.clear_form()
            self.refresh_orders()
            
        except Exception as e:
            messagebox.showerror("错误", f"创建失败：{e}")
    
    def refresh_orders(self):
        """刷新订单列表"""
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        orders = self.system.get_all_repair_orders()
        status_map = {
            'pending': '待维修',
            'repairing': '维修中',
            'completed': '已完成',
            'delivered': '已交付'
        }
        
        filter_status = self.status_filter.get()
        
        for order in orders:
            status_text = status_map.get(order[11], order[11])
            
            # 状态筛选
            if filter_status != '全部' and order[11] != filter_status:
                continue
            
            self.orders_tree.insert('', 'end', values=(
                order[1],  # 订单号
                order[16] if len(order) > 16 else '',  # 客户名
                f"{order[3]} {order[4]}",  # 品牌型号
                order[5][:20] + '...' if len(order[5] or '') > 20 else order[5],  # 问题描述
                f"¥{order[9]:.2f}",  # 总费用
                f"¥{order[10]:.2f}",  # 定金
                status_text,  # 状态
                order[12][:10] if order[12] else ''  # 接修日期
            ))
    
    def complete_repair(self):
        """完成维修"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一个维修订单")
            return
        
        values = self.orders_tree.item(selected[0], 'values')
        order_no = values[0]
        
        # 获取订单ID
        self.system.cursor.execute('SELECT id, total_cost, deposit FROM repair_orders WHERE order_no = ?', 
                                   (order_no,))
        order = self.system.cursor.fetchone()
        
        if order:
            remaining = order[1] - order[2]
            
            if remaining > 0:
                result = messagebox.askyesno("收款", f"订单还需收款 ¥{remaining:.2f}\n是否现在收款？")
                if result:
                    # 这里可以打开收款对话框
                    from tkinter import simpledialog
                    amount = simpledialog.askfloat("收款", f"请输入收款金额（最多 ¥{remaining:.2f}）：", 
                                                   minvalue=0, maxvalue=remaining)
                    if amount and amount > 0:
                        self.system.add_transaction('income', 'repair', amount, 
                                                    'repair_order', order[0], '现金')
                        # 更新定金（这里简化处理）
                        self.system.cursor.execute('UPDATE repair_orders SET deposit = deposit + ? WHERE id = ?',
                                                   (amount, order[0]))
                        self.system.conn.commit()
            
            self.system.complete_repair(order[0])
            messagebox.showinfo("成功", f"订单 {order_no} 已完成维修！")
            self.refresh_orders()
    
    def deliver_phone(self):
        """交付手机"""
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一个维修订单")
            return
        
        values = self.orders_tree.item(selected[0], 'values')
        order_no = values[0]
        
        # 检查是否已完成维修
        self.system.cursor.execute('SELECT status FROM repair_orders WHERE order_no = ?', (order_no,))
        status = self.system.cursor.fetchone()[0]
        
        if status != 'completed':
            messagebox.showwarning("警告", "该订单尚未完成维修，不能交付！")
            return
        
        self.system.cursor.execute('''
            UPDATE repair_orders 
            SET status = 'delivered', delivery_date = ?
            WHERE order_no = ?
        ''', (tk.datetime.now() if hasattr(tk, 'datetime') else None, order_no))
        self.system.conn.commit()
        
        messagebox.showinfo("成功", f"手机已交付给客户！\n订单号：{order_no}")
        self.refresh_orders()
    
    def view_repair_detail(self, event):
        """查看维修详情"""
        selected = self.orders_tree.selection()
        if not selected:
            return
        
        values = self.orders_tree.item(selected[0], 'values')
        order_no = values[0]
        
        # 获取完整订单信息
        self.system.cursor.execute('''
            SELECT r.*, c.name, c.phone 
            FROM repair_orders r
            LEFT JOIN customers c ON r.customer_id = c.id
            WHERE r.order_no = ?
        ''', (order_no,))
        
        order = self.system.cursor.fetchone()
        
        if order:
            # 创建详情窗口
            detail_dialog = tk.Toplevel()
            detail_dialog.title(f"维修订单详情 - {order_no}")
            detail_dialog.geometry("500x500")
            detail_dialog.transient(self.frame.winfo_toplevel())
            
            # 显示信息
            info_text = f"""
订单号：{order[1]}
客户：{order[16]} ({order[17]})
设备：{order[3]} {order[4]}
IMEI：{order[5]}

问题描述：
{order[6]}

维修类型：{order[7]}
维修费：¥{order[8]:.2f}
配件费：¥{order[9]:.2f}
总费用：¥{order[10]:.2f}
定金：¥{order[11]:.2f}
剩余应付：¥{order[10] - order[11]:.2f}

状态：{order[12]}
接修日期：{order[13]}
完成日期：{order[15] if order[15] else '未完成'}
交付日期：{order[16] if len(order) > 16 and order[16] else '未交付'}

备注：{order[17] if len(order) > 17 and order[17] else '无'}
            """
            
            text_widget = tk.Text(detail_dialog, wrap='word', width=60, height=25)
            text_widget.insert('1.0', info_text)
            text_widget.configure(state='disabled')
            text_widget.pack(padx=10, pady=10, fill='both', expand=True)
            
            ttk.Button(detail_dialog, text="关闭", command=detail_dialog.destroy).pack(pady=10)