# gui/repair_view_ctk.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog

class RepairView:
    def __init__(self, parent, system, main_window=None):
        self.system = system
        self.parent = parent
        self.main_window = main_window  # 保存主窗口引用
        
        self.setup_ui()
        self.load_customers()
        self.load_technicians()
        self.load_repairs()
    
    def setup_ui(self):
        """设置维修管理界面"""
        
        # 创建主滚动区域
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建维修单表单卡片
        self.create_repair_card()
        
        # 创建维修单列表卡片
        self.create_repair_list_card()
    
    def create_repair_card(self):
        """创建维修单表单卡片"""
        repair_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        repair_card.pack(fill="x", padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            repair_card,
            text="🔧 创建维修单",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=15)
        
        # 表单区域 - 使用两列布局
        form_frame = ctk.CTkFrame(repair_card, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="x")
        
        # 左侧列
        left_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # 右侧列
        right_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        # 左侧字段
        self.fields = {}
        left_fields = [
            ('客户', 'combo'), ('设备品牌', 'entry'), ('设备型号', 'entry'),
            ('维修类型', 'combo'), ('维修费', 'entry')
        ]
        
        for i, (label, field_type) in enumerate(left_fields):
            ctk.CTkLabel(left_frame, text=f"{label}:", font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, padx=10, pady=8, sticky="e"
            )
            
            if field_type == 'combo':
                if label == '客户':
                    widget = ctk.CTkComboBox(left_frame, width=200, font=ctk.CTkFont(size=14))
                    self.fields[label] = widget
                else:  # 维修类型
                    widget = ctk.CTkComboBox(
                        left_frame,
                        values=['屏幕维修', '电池更换', '进水维修', '系统故障', '其他'],
                        width=200,
                        font=ctk.CTkFont(size=14)
                    )
                    widget.set('屏幕维修')
                    self.fields[label] = widget
            else:
                widget = ctk.CTkEntry(left_frame, width=200, font=ctk.CTkFont(size=14))
                self.fields[label] = widget
            
            widget.grid(row=i, column=1, padx=10, pady=8)
        
        # 右侧字段
        right_fields = [
            ('配件费', 'entry'), ('定金', 'entry'), ('维修技师', 'combo'), ('备注', 'text')
        ]
        
        for i, (label, field_type) in enumerate(right_fields):
            ctk.CTkLabel(right_frame, text=f"{label}:", font=ctk.CTkFont(size=14)).grid(
                row=i, column=0, padx=10, pady=8, sticky="e"
            )
            
            if field_type == 'combo':
                self.technician_combo = ctk.CTkComboBox(right_frame, width=200, font=ctk.CTkFont(size=14))
                self.technician_combo.grid(row=i, column=1, padx=10, pady=8)
                self.fields[label] = self.technician_combo
            elif field_type == 'text':
                widget = ctk.CTkTextbox(right_frame, width=200, height=80, font=ctk.CTkFont(size=14))
                widget.grid(row=i, column=1, padx=10, pady=8)
                self.fields[label] = widget
            else:
                widget = ctk.CTkEntry(right_frame, width=200, font=ctk.CTkFont(size=14))
                widget.insert(0, "0")
                widget.grid(row=i, column=1, padx=10, pady=8)
                self.fields[label] = widget
        
        # 按钮区域
        button_frame = ctk.CTkFrame(repair_card, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="创建维修单",
            command=self.create_repair,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="清空表单",
            command=self.clear_form,
            width=150,
            height=40,
            fg_color="gray"
        ).pack(side="left", padx=10)
        
        # 新客户按钮
        ctk.CTkButton(
            button_frame,
            text="新客户",
            command=self.add_customer,
            width=100,
            height=40,
            fg_color="#2196F3"
        ).pack(side="left", padx=10)
    
    def create_repair_list_card(self):
        """创建维修单列表卡片"""
        list_card = ctk.CTkFrame(self.main_frame, corner_radius=15)
        list_card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题
        title = ctk.CTkLabel(
            list_card,
            text="📋 维修单列表",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # 工具栏
        toolbar = ctk.CTkFrame(list_card, fg_color="transparent")
        toolbar.pack(fill="x", padx=20, pady=10)
        
        # 搜索框
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var, width=200, placeholder_text="搜索订单号/客户...")
        self.search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar,
            text="搜索",
            command=self.search_repairs,
            width=80
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            toolbar,
            text="刷新",
            command=self.load_repairs,
            width=80,
            fg_color="#2196F3"
        ).pack(side="left", padx=5)
        
        # 状态筛选
        ctk.CTkLabel(toolbar, text="状态:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.status_filter = ctk.CTkComboBox(
            toolbar,
            values=['全部', '待维修', '维修中', '已完成', '已取机'],
            width=100,
            font=ctk.CTkFont(size=14)
        )
        self.status_filter.set('全部')
        self.status_filter.pack(side="left", padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_repairs())
        
        # 定义列名
        self.columns = ("维修单号", "客户", "设备品牌", "故障描述", "状态", "创建日期")
        
        # 表格
        self.table_frame = ctk.CTkScrollableFrame(list_card, height=400)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题行
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#f0f0f0")
        header_frame.pack(fill="x", pady=1)
        
        for i, col in enumerate(self.columns):
            label = ctk.CTkLabel(
                header_frame,
                text=col,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150
            )
            label.grid(row=0, column=i, padx=5, pady=8)
        
        # 数据行容器
        self.data_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.data_container.pack(fill="x")
        
        self.data_rows = []
    
    def load_customers(self):
        """加载客户列表"""
        customers = self.system.get_all_customers()
        self.fields['客户']['values'] = [f"{c.get('id')}-{c.get('name')} ({c.get('phone')})" for c in customers]
    
    def load_technicians(self):
        """加载技师列表"""
        technicians = self.system.get_all_technicians()
        self.technician_combo['values'] = [f"{t.get('id')}-{t.get('name')}" for t in technicians]
    
    def add_customer(self):
        """添加客户对话框"""
        dialog = ctk.CTkToplevel()
        dialog.title("添加客户")
        dialog.geometry("400x450")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        fields = {}
        labels = ['姓名', '电话', '微信', '地址']
        
        for i, label in enumerate(labels):
            ctk.CTkLabel(dialog, text=f"{label}:").grid(row=i, column=0, padx=10, pady=8, sticky="e")
            if label == '地址':
                entry = ctk.CTkTextbox(dialog, width=200, height=60)
            else:
                entry = ctk.CTkEntry(dialog, width=200)
            entry.grid(row=i, column=1, padx=10, pady=8)
            fields[label] = entry
        
        def save():
            try:
                address = fields['地址'].get("1.0", "end-1c") if isinstance(fields['地址'], ctk.CTkTextbox) else fields['地址'].get()
                self.system.add_customer(
                    name=fields['姓名'].get(),
                    phone=fields['电话'].get(),
                    wechat=fields['微信'].get(),
                    address=address,
                    customer_type='retail'
                )
                messagebox.showinfo("成功", "客户添加成功！")
                dialog.destroy()
                self.load_customers()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{e}")
        
        ctk.CTkButton(dialog, text="保存", command=save).grid(row=len(labels), column=1, pady=20)
    
    def create_repair(self):
        """创建维修单"""
        customer_str = self.fields['客户'].get()
        if not customer_str:
            messagebox.showwarning("警告", "请选择客户")
            return
        
        customer_id = int(customer_str.split('-')[0])
        
        # 获取故障描述
        fault_desc = self.fields['备注'].get("1.0", "end-1c") if isinstance(self.fields['备注'], ctk.CTkTextbox) else self.fields['备注'].get()
        
        # 获取技师ID
        technician_str = self.technician_combo.get()
        technician_id = None
        if technician_str:
            technician_id = int(technician_str.split('-')[0])
        
        # 获取费用
        try:
            repair_cost = float(self.fields['维修费'].get() or 0)
            parts_cost = float(self.fields['配件费'].get() or 0)
            deposit = float(self.fields['定金'].get() or 0)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
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
                notes=fault_desc
            )
            
            messagebox.showinfo("成功", f"维修单创建成功！\n维修单号：{repair_no}")
            self.clear_form()
            self.load_repairs()
            
        except Exception as e:
            messagebox.showerror("错误", f"创建维修单失败：{e}")
    
    def load_repairs(self):
        """加载维修单列表"""
        # 清除现有行
        for row_widgets in self.data_rows:
            for widget in row_widgets:
                widget.destroy()
        self.data_rows.clear()
        
        repairs = self.system.get_all_repair_orders()
        
        status_map = {
            'pending': '待维修',
            'repairing': '维修中',
            'completed': '已完成',
            'picked': '已取机'
        }
        
        status_filter_cn = self.status_filter.get()
        
        # 状态颜色映射
        status_colors = {
            '待维修': '#FF9800',
            '维修中': '#2196F3',
            '已完成': '#4CAF50',
            '已取机': '#9E9E9E'
        }
        
        for repair in repairs:
            repair_no = repair.get('order_no', '')
            customer_name = repair.get('customer_name', '')
            device_brand = repair.get('device_brand', '')
            problem_desc = repair.get('problem_desc', '')[:30]
            status = repair.get('status', 'pending')
            receive_date = repair.get('receive_date', '')
            
            status_text = status_map.get(status, status)
            
            # 状态筛选
            if status_filter_cn != '全部' and status_text != status_filter_cn:
                continue
            
            # 格式化日期
            if receive_date and hasattr(receive_date, 'strftime'):
                date_str = receive_date.strftime('%Y-%m-%d')
            else:
                date_str = str(receive_date)[:10] if receive_date else ''
            
            row_frame = ctk.CTkFrame(self.data_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=1)
            
            widgets = []
            values = [repair_no, customer_name, device_brand, problem_desc, status_text, date_str]
            
            for i, value in enumerate(values):
                # 状态列特殊处理颜色
                if i == 4:
                    text_color = status_colors.get(status_text, '#333333')
                    font = ctk.CTkFont(size=12, weight="bold")
                else:
                    text_color = "#333333"
                    font = ctk.CTkFont(size=12)
                
                label = ctk.CTkLabel(
                    row_frame,
                    text=str(value),
                    width=150,
                    text_color=text_color,
                    font=font
                )
                label.grid(row=0, column=i, padx=5, pady=6)
                widgets.append(label)
            
            # 添加查看详情按钮
            view_btn = ctk.CTkButton(
                row_frame,
                text="查看详情",
                width=80,
                height=28,
                fg_color="#2196F3",
                command=lambda r=repair: self.view_repair_detail(r)
            )
            view_btn.grid(row=0, column=len(self.columns), padx=5, pady=6)
            widgets.append(view_btn)
            
            self.data_rows.append(widgets)
    
    def search_repairs(self):
        """搜索维修单"""
        keyword = self.search_var.get()
        if not keyword:
            self.load_repairs()
            return
        
        # 清除现有行
        for row_widgets in self.data_rows:
            for widget in row_widgets:
                widget.destroy()
        self.data_rows.clear()
        
        repairs = self.system.get_all_repair_orders()
        
        status_map = {
            'pending': '待维修',
            'repairing': '维修中',
            'completed': '已完成',
            'picked': '已取机'
        }
        
        status_colors = {
            '待维修': '#FF9800',
            '维修中': '#2196F3',
            '已完成': '#4CAF50',
            '已取机': '#9E9E9E'
        }
        
        for repair in repairs:
            repair_no = repair.get('order_no', '')
            customer_name = repair.get('customer_name', '')
            problem_desc = repair.get('problem_desc', '')
            device_brand = repair.get('device_brand', '')
            
            if keyword in repair_no or keyword in customer_name or keyword in problem_desc or keyword in device_brand:
                status = repair.get('status', 'pending')
                receive_date = repair.get('receive_date', '')
                status_text = status_map.get(status, status)
                
                if receive_date and hasattr(receive_date, 'strftime'):
                    date_str = receive_date.strftime('%Y-%m-%d')
                else:
                    date_str = str(receive_date)[:10] if receive_date else ''
                
                row_frame = ctk.CTkFrame(self.data_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=1)
                
                widgets = []
                values = [repair_no, customer_name, device_brand, problem_desc[:30], status_text, date_str]
                
                for i, value in enumerate(values):
                    if i == 4:
                        text_color = status_colors.get(status_text, '#333333')
                        font = ctk.CTkFont(size=12, weight="bold")
                    else:
                        text_color = "#333333"
                        font = ctk.CTkFont(size=12)
                    
                    label = ctk.CTkLabel(
                        row_frame,
                        text=str(value),
                        width=150,
                        text_color=text_color,
                        font=font
                    )
                    label.grid(row=0, column=i, padx=5, pady=6)
                    widgets.append(label)
                
                view_btn = ctk.CTkButton(
                    row_frame,
                    text="查看详情",
                    width=80,
                    height=28,
                    fg_color="#2196F3",
                    command=lambda r=repair: self.view_repair_detail(r)
                )
                view_btn.grid(row=0, column=6, padx=5, pady=6)
                widgets.append(view_btn)
                
                self.data_rows.append(widgets)
    
    def view_repair_detail(self, repair):
        """查看维修单详情"""
        dialog = ctk.CTkToplevel()
        dialog.title(f"维修单详情 - {repair.get('order_no', '')}")
        dialog.geometry("550x600")
        dialog.transient(self.parent.winfo_toplevel())
        dialog.grab_set()
        
        # 使窗口居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 550) // 2
        y = (dialog.winfo_screenheight() - 600) // 2
        dialog.geometry(f"550x600+{x}+{y}")
        
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
        
        # 创建详情显示区域
        scroll_frame = ctk.CTkScrollableFrame(dialog, height=500)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        info_text = f"""
        【基本信息】
        维修单号：{repair.get('order_no', '')}
        客户：{repair.get('customer_name', '')}
        状态：{status_map.get(repair.get('status', ''), repair.get('status', ''))}
        
        【设备信息】
        设备品牌：{repair.get('device_brand', '')}
        设备型号：{repair.get('device_model', '')}
        维修类型：{repair.get('repair_type', '')}
        
        【故障描述】
        {repair.get('problem_desc', '')}
        
        【费用明细】
        维修费：¥{repair.get('repair_cost', 0):.2f}
        配件费：¥{repair.get('parts_cost', 0):.2f}
        总费用：¥{total_cost:.2f}
        定金：¥{deposit:.2f}
        待付款：¥{remaining:.2f}
        
        【时间信息】
        接收日期：{receive_date_str}
        完成日期：{finish_date_str}
        
        【备注】
        {repair.get('notes', '')}
        """
        
        text_widget = ctk.CTkTextbox(scroll_frame, width=500, height=400, font=ctk.CTkFont(size=12))
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")
        text_widget.pack(pady=10)
        
        # 按钮区域
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        if repair.get('status') == 'pending':
            ctk.CTkButton(
                button_frame,
                text="开始维修",
                command=lambda: self.update_repair_status(repair.get('id'), 'repairing', dialog),
                width=120
            ).pack(side="left", padx=5)
        elif repair.get('status') == 'repairing':
            ctk.CTkButton(
                button_frame,
                text="完成维修",
                command=lambda: self.complete_repair(repair.get('id'), dialog),
                width=120,
                fg_color="#4CAF50"
            ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="关闭",
            command=dialog.destroy,
            width=120,
            fg_color="gray"
        ).pack(side="left", padx=5)
    
    def update_repair_status(self, repair_id, status, dialog=None):
        """更新维修单状态"""
        try:
            if hasattr(self.system, 'update_repair_status'):
                self.system.update_repair_status(repair_id, status)
            else:
                cursor = self.system.conn.cursor()
                cursor.execute(
                    "UPDATE repair_orders SET status = %s WHERE id = %s",
                    (status, repair_id)
                )
                self.system.conn.commit()
            
            messagebox.showinfo("成功", "维修单状态已更新")
            if dialog:
                dialog.destroy()
            self.load_repairs()
        except Exception as e:
            messagebox.showerror("错误", f"更新失败：{e}")
            self.system.conn.rollback()
    
    def complete_repair(self, repair_id, dialog=None):
        """完成维修"""
        try:
            remaining = self.system.complete_repair(repair_id)
            if remaining is not None:
                if remaining > 0:
                    messagebox.showinfo("成功", f"维修已完成\n待收款：¥{remaining:.2f}")
                else:
                    messagebox.showinfo("成功", "维修已完成")
                if dialog:
                    dialog.destroy()
                self.load_repairs()
            else:
                messagebox.showerror("错误", "完成维修失败")
        except Exception as e:
            messagebox.showerror("错误", f"完成维修失败：{e}")
    
    def clear_form(self):
        """清空表单"""
        for field_name, field in self.fields.items():
            if field_name == '备注':
                if isinstance(field, ctk.CTkTextbox):
                    field.delete("1.0", "end")
            elif field_name in ['客户', '维修技师', '维修类型']:
                if hasattr(field, 'set'):
                    field.set('')
            else:
                if hasattr(field, 'delete'):
                    field.delete(0, "end")
        
        # 清空技师选择
        self.technician_combo.set('')
        
        # 重置数字字段为0
        for field in ['维修费', '配件费', '定金']:
            if field in self.fields:
                self.fields[field].delete(0, "end")
                self.fields[field].insert(0, "0")