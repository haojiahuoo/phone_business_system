# gui/repair_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class RepairView:
    def __init__(self, parent, system):
        self.system = system
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="维修管理")
        
        self.setup_ui()
        self.load_customers()
        self.load_technicians()
        self.load_repairs()
    
    def setup_ui(self):
        """设置界面"""
        # 创建表单框架
        form_frame = ttk.LabelFrame(self.frame, text="创建维修单", padding=10)
        form_frame.pack(pady=10, padx=20, fill='x')
        
        # 定义表单字段
        self.fields = {}
        labels = ['客户', '设备品牌', '设备型号', '故障描述', '维修类型', '维修费', '配件费', '定金', '备注']
        
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=f"{label}:").grid(row=i, column=0, sticky='e', padx=5, pady=5)
            
            if label == '故障描述':
                entry = tk.Text(form_frame, width=40, height=3)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                self.fields[label] = entry
            elif label == '客户':
                combo = ttk.Combobox(form_frame, width=37)
                combo.grid(row=i, column=1, padx=5, pady=5)
                self.fields[label] = combo
                ttk.Button(form_frame, text="新客户", command=self.add_customer).grid(row=i, column=2, padx=5)
            elif label == '维修技师':
                combo = ttk.Combobox(form_frame, width=37)
                combo.grid(row=i, column=1, padx=5, pady=5)
                self.fields[label] = combo
            elif label == '维修类型':
                combo = ttk.Combobox(form_frame, values=['屏幕维修', '电池更换', '进水维修', '系统故障', '其他'], width=37)
                combo.grid(row=i, column=1, padx=5, pady=5)
                self.fields[label] = combo
            else:
                entry = ttk.Entry(form_frame, width=40)
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.fields[label] = entry
        
        # 维修技师选择
        ttk.Label(form_frame, text="维修技师:").grid(row=len(labels), column=0, sticky='e', padx=5, pady=5)
        self.technician_combo = ttk.Combobox(form_frame, width=37)
        self.technician_combo.grid(row=len(labels), column=1, padx=5, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels)+1, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="创建维修单", command=self.create_repair, width=15).pack(side='left', padx=10)
        ttk.Button(button_frame, text="清空表单", command=self.clear_form, width=15).pack(side='left', padx=10)
        
        # 维修单列表
        self.create_repair_list_frame()
    
    def create_repair_list_frame(self):
        """创建维修单列表"""
        list_frame = ttk.LabelFrame(self.frame, text="维修单列表", padding=10)
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # 搜索框
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill='x', pady=5)
        
        ttk.Label(search_frame, text="搜索:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=20).pack(side='left', padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_repairs).pack(side='left', padx=5)
        ttk.Button(search_frame, text="刷新", command=self.load_repairs).pack(side='left', padx=5)
        
        # 状态筛选
        ttk.Label(search_frame, text="状态:").pack(side='left', padx=5)
        self.status_filter = ttk.Combobox(search_frame, values=['全部', '待维修', '维修中', '已完成', '已取机'], width=10)
        self.status_filter.set('全部')
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_repairs())
        self.status_filter.pack(side='left', padx=5)
        
        # 维修单列表
        columns = ('维修单号', '客户', '设备品牌', '故障描述', '状态', '创建日期')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        col_widths = {'维修单号': 120, '客户': 100, '设备品牌': 100, '故障描述': 200, '状态': 80, '创建日期': 100}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100))
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 绑定事件
        self.tree.bind('<Double-Button-1>', self.view_repair_detail)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # 右键菜单
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="更新状态", command=self.update_status)
        self.context_menu.add_command(label="删除", command=self.delete_repair)
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def load_customers(self):
        """加载客户列表"""
        customers = self.system.get_all_customers()
        self.fields['客户']['values'] = [f"{c.get('id')}-{c.get('name')} ({c.get('phone')})" for c in customers]
    
    def load_technicians(self):
        """加载技师列表"""
        technicians = self.system.get_all_technicians()
        self.technician_combo['values'] = [f"{t.get('id')}-{t.get('name')}" for t in technicians]
    
    def add_customer(self):
        """添加新客户"""
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
    
    def create_repair(self):
        """创建维修单"""
        customer_str = self.fields['客户'].get()
        if not customer_str:
            messagebox.showwarning("警告", "请选择客户")
            return
        
        customer_id = int(customer_str.split('-')[0])
        
        # 获取故障描述
        fault_desc = self.fields['故障描述'].get('1.0', 'end-1c') if isinstance(self.fields['故障描述'], tk.Text) else self.fields['故障描述'].get()
        
        # 获取技师ID
        technician_str = self.technician_combo.get()
        technician_id = None
        if technician_str:
            technician_id = int(technician_str.split('-')[0])
        
        # 获取费用
        try:
            repair_cost = float(self.fields['维修费'].get() or 0)
        except ValueError:
            repair_cost = 0
        
        try:
            parts_cost = float(self.fields['配件费'].get() or 0)
        except ValueError:
            parts_cost = 0
        
        try:
            deposit = float(self.fields['定金'].get() or 0)
        except ValueError:
            deposit = 0
        
        try:
            repair_no = self.system.create_repair_order(
                customer_id=customer_id,
                device_brand=self.fields['设备品牌'].get(),
                device_model=self.fields['设备型号'].get(),
                problem_desc=fault_desc,
                repair_type=self.fields['维修类型'].get(),
                repair_cost=repair_cost,
                parts_cost=parts_cost,
                deposit=deposit,
                notes=self.fields['备注'].get()
            )
            
            messagebox.showinfo("成功", f"维修单创建成功！\n维修单号：{repair_no}")
            self.clear_form()
            self.load_repairs()
            
        except Exception as e:
            messagebox.showerror("错误", f"创建维修单失败：{e}")
    
    def load_repairs(self):
        """加载维修单列表"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取所有维修单
        repairs = self.system.get_all_repair_orders()
        
        # 状态映射（英文转中文）
        status_map = {
            'pending': '待维修',
            'repairing': '维修中',
            'completed': '已完成',
            'picked': '已取机'
        }
        
        # 获取状态筛选条件（中文）
        status_filter_cn = self.status_filter.get()
        
        for repair in repairs:
            # 使用字典键名访问（匹配 database_mysql.py 中的字段名）
            repair_no = repair.get('order_no', '')
            customer_name = repair.get('customer_name', '')
            device_brand = repair.get('device_brand', '')
            problem_desc = repair.get('problem_desc', '')[:30] + '...' if len(repair.get('problem_desc', '')) > 30 else repair.get('problem_desc', '')
            status = repair.get('status', 'pending')
            receive_date = repair.get('receive_date', '')
            
            # 状态中文
            status_text = status_map.get(status, status)
            
            # 状态筛选
            if status_filter_cn != '全部' and status_text != status_filter_cn:
                continue
            
            # 格式化日期
            if receive_date:
                if hasattr(receive_date, 'strftime'):
                    date_str = receive_date.strftime('%Y-%m-%d')
                else:
                    date_str = str(receive_date)[:10] if receive_date else ''
            else:
                date_str = ''
            
            self.tree.insert('', 'end', values=(
                repair_no,
                customer_name,
                device_brand,
                problem_desc,
                status_text,
                date_str
            ))
    
    def search_repairs(self):
        """搜索维修单"""
        keyword = self.search_var.get()
        if not keyword:
            self.load_repairs()
            return
        
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取所有维修单
        repairs = self.system.get_all_repair_orders()
        
        # 状态映射
        status_map = {
            'pending': '待维修',
            'repairing': '维修中',
            'completed': '已完成',
            'picked': '已取机'
        }
        
        for repair in repairs:
            repair_no = repair.get('order_no', '')
            customer_name = repair.get('customer_name', '')
            problem_desc = repair.get('problem_desc', '')
            device_brand = repair.get('device_brand', '')
            
            # 搜索匹配
            if keyword in repair_no or keyword in customer_name or keyword in problem_desc or keyword in device_brand:
                status = repair.get('status', 'pending')
                receive_date = repair.get('receive_date', '')
                status_text = status_map.get(status, status)
                
                if receive_date:
                    if hasattr(receive_date, 'strftime'):
                        date_str = receive_date.strftime('%Y-%m-%d')
                    else:
                        date_str = str(receive_date)[:10] if receive_date else ''
                else:
                    date_str = ''
                
                self.tree.insert('', 'end', values=(
                    repair_no,
                    customer_name,
                    device_brand,
                    problem_desc[:30] + '...' if len(problem_desc) > 30 else problem_desc,
                    status_text,
                    date_str
                ))
    
    def view_repair_detail(self, event):
        """查看维修单详情"""
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected[0], 'values')
        repair_no = values[0]
        
        # 获取所有维修单，找到对应的
        repairs = self.system.get_all_repair_orders()
        repair = None
        for r in repairs:
            if r.get('order_no') == repair_no:
                repair = r
                break
        
        if not repair:
            messagebox.showerror("错误", "未找到维修单信息")
            return
        
        # 创建详情窗口
        detail_dialog = tk.Toplevel()
        detail_dialog.title(f"维修单详情 - {repair_no}")
        detail_dialog.geometry("500x550")
        detail_dialog.transient(self.frame.winfo_toplevel())
        
        # 显示详细信息
        info_frame = ttk.Frame(detail_dialog, padding=10)
        info_frame.pack(fill='both', expand=True)
        
        # 状态映射
        status_map = {
            'pending': '待维修',
            'repairing': '维修中',
            'completed': '已完成',
            'picked': '已取机'
        }
        
        # 格式化日期
        receive_date = repair.get('receive_date', '')
        if receive_date and hasattr(receive_date, 'strftime'):
            receive_date_str = receive_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            receive_date_str = str(receive_date) if receive_date else ''
        
        finish_date = repair.get('finish_date', '')
        if finish_date and hasattr(finish_date, 'strftime'):
            finish_date_str = finish_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            finish_date_str = '未完成'
        
        total_cost = repair.get('total_cost', 0)
        deposit = repair.get('deposit', 0)
        remaining = total_cost - deposit
        
        info_text = f"""
维修单号：{repair.get('order_no', '')}
客户：{repair.get('customer_name', '')}
设备品牌：{repair.get('device_brand', '')}
设备型号：{repair.get('device_model', '')}
故障描述：{repair.get('problem_desc', '')}
维修类型：{repair.get('repair_type', '')}
维修费：¥{repair.get('repair_cost', 0):.2f}
配件费：¥{repair.get('parts_cost', 0):.2f}
总费用：¥{total_cost:.2f}
定金：¥{deposit:.2f}
待付款：¥{remaining:.2f}
状态：{status_map.get(repair.get('status', ''), repair.get('status', ''))}
接收日期：{receive_date_str}
完成日期：{finish_date_str}
备注：{repair.get('notes', '')}
        """
        
        text_widget = tk.Text(info_frame, width=60, height=20)
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)
        
        # 按钮区域
        button_frame = ttk.Frame(detail_dialog)
        button_frame.pack(pady=10)
        
        if repair.get('status') == 'pending':
            ttk.Button(button_frame, text="开始维修", 
                      command=lambda: self.update_repair_status(repair.get('id'), 'repairing')).pack(side='left', padx=5)
        elif repair.get('status') == 'repairing':
            ttk.Button(button_frame, text="完成维修", 
                      command=lambda: self.complete_repair(repair.get('id'))).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="关闭", command=detail_dialog.destroy).pack(side='left', padx=5)
    
    def update_repair_status(self, repair_id, status):
        """更新维修单状态"""
        try:
            # 使用数据库类中的 update_repair_status 方法
            # 如果没有这个方法，需要先在 database_mysql.py 中添加
            if hasattr(self.system, 'update_repair_status'):
                self.system.update_repair_status(repair_id, status)
            else:
                # 直接执行 SQL
                cursor = self.system.conn.cursor()
                cursor.execute(
                    "UPDATE repair_orders SET status = %s WHERE id = %s",
                    (status, repair_id)
                )
                self.system.conn.commit()
            messagebox.showinfo("成功", "维修单状态已更新")
            self.load_repairs()
        except Exception as e:
            messagebox.showerror("错误", f"更新失败：{e}")
            self.system.conn.rollback()
    
    def complete_repair(self, repair_id):
        """完成维修"""
        try:
            # 调用已有的 complete_repair 方法
            remaining = self.system.complete_repair(repair_id)
            if remaining is not None:
                if remaining > 0:
                    messagebox.showinfo("成功", f"维修已完成\n待收款：¥{remaining:.2f}")
                else:
                    messagebox.showinfo("成功", "维修已完成")
                self.load_repairs()
            else:
                messagebox.showerror("错误", "完成维修失败")
        except Exception as e:
            messagebox.showerror("错误", f"完成维修失败：{e}")
    
    def add_repair_cost(self, repair_id):
        """添加维修费用"""
        cost = simpledialog.askfloat("添加费用", "请输入额外费用：", minvalue=0)
        if cost is not None and cost > 0:
            try:
                # 更新维修费用
                cursor = self.system.conn.cursor()
                cursor.execute(
                    "UPDATE repair_orders SET parts_cost = parts_cost + %s, total_cost = total_cost + %s WHERE id = %s",
                    (cost, cost, repair_id)
                )
                self.system.conn.commit()
                messagebox.showinfo("成功", f"已添加费用 ¥{cost:.2f}")
                self.load_repairs()
            except Exception as e:
                messagebox.showerror("错误", f"添加费用失败：{e}")
                self.system.conn.rollback()
    
    def update_status(self):
        """右键菜单：更新状态"""
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected[0], 'values')
        repair_no = values[0]
        
        # 获取当前状态
        repairs = self.system.get_all_repair_orders()
        repair = None
        for r in repairs:
            if r.get('order_no') == repair_no:
                repair = r
                break
        
        if not repair:
            return
        
        current_status = repair.get('status')
        
        # 状态选项
        status_options = {
            'pending': '待维修',
            'repairing': '维修中',
            'completed': '已完成',
            'picked': '已取机'
        }
        
        # 根据当前状态决定可选项
        if current_status == 'pending':
            options = ['repairing']
        elif current_status == 'repairing':
            options = ['completed']
        elif current_status == 'completed':
            options = ['picked']
        else:
            options = []
        
        if not options:
            messagebox.showinfo("提示", "该维修单无法更改状态")
            return
        
        # 选择新状态
        new_status = simpledialog.askstring("更新状态", 
                                            f"当前状态：{status_options.get(current_status)}\n选择新状态：",
                                            initialvalue=options[0])
        
        if new_status and new_status in options:
            self.update_repair_status(repair.get('id'), new_status)
    
    def delete_repair(self):
        """右键菜单：删除维修单"""
        selected = self.tree.selection()
        if not selected:
            return
        
        values = self.tree.item(selected[0], 'values')
        repair_no = values[0]
        
        if messagebox.askyesno("确认", f"确定要删除维修单 {repair_no} 吗？"):
            try:
                # 获取维修单ID
                repairs = self.system.get_all_repair_orders()
                for r in repairs:
                    if r.get('order_no') == repair_no:
                        cursor = self.system.conn.cursor()
                        cursor.execute("DELETE FROM repair_orders WHERE id = %s", (r.get('id'),))
                        self.system.conn.commit()
                        break
                messagebox.showinfo("成功", "维修单已删除")
                self.load_repairs()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败：{e}")
                self.system.conn.rollback()
    
    def clear_form(self):
        """清空表单"""
        for field_name, field in self.fields.items():
            if field_name == '故障描述':
                field.delete('1.0', 'end')
            elif field_name in ['客户', '维修技师', '维修类型']:
                if hasattr(field, 'set'):
                    field.set('')
            else:
                if hasattr(field, 'delete'):
                    field.delete(0, 'end')
        
        # 清空技师选择
        self.technician_combo.set('')