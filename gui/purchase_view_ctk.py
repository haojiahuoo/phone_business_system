# gui/purchase_view_ctk.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime

class PurchaseView:
    def __init__(self, parent, system):
        self.system = system
        self.parent = parent
        self.purchase_items = []
        
        self.setup_ui()
        self.load_suppliers()
        self.load_products()
        self.refresh_purchases()
    
    def setup_ui(self):
        """设置采购管理界面"""
        self.main_frame = ctk.CTkScrollableFrame(self.parent, fg_color="#1e1e2e")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建采购订单卡片
        self.create_purchase_card()
        
        # 创建采购记录卡片
        self.create_purchase_list_card()
    
    def create_purchase_card(self):
        """创建采购订单卡片"""
        card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2d2d2d")
        card.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="🛒 创建采购订单",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title.pack(pady=15)
        
        # 表单区域
        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="x")
        
        # 供应商选择
        ctk.CTkLabel(form_frame, text="供应商:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        self.supplier_combo = ctk.CTkComboBox(form_frame, width=300, font=ctk.CTkFont(size=14))
        self.supplier_combo.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkButton(
            form_frame,
            text="新供应商",
            command=self.add_supplier,
            width=100
        ).grid(row=0, column=2, padx=10, pady=10)
        
        # 商品选择
        ctk.CTkLabel(form_frame, text="商品:", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.product_combo = ctk.CTkComboBox(form_frame, width=300, font=ctk.CTkFont(size=14))
        self.product_combo.grid(row=1, column=1, padx=10, pady=10)
        
        ctk.CTkButton(
            form_frame,
            text="添加商品",
            command=self.add_purchase_item,
            width=100,
            fg_color="#4CAF50"
        ).grid(row=1, column=2, padx=10, pady=10)
        
        # 采购明细表格
        self.create_items_table(card)
        
        # 总金额
        total_frame = ctk.CTkFrame(card, fg_color="transparent")
        total_frame.pack(pady=10)
        
        ctk.CTkLabel(total_frame, text="总金额:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)
        self.total_label = ctk.CTkLabel(
            total_frame,
            text="¥0.00",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4CAF50"
        )
        self.total_label.pack(side="left", padx=5)
        
        # 按钮
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="创建采购订单",
            command=self.create_purchase,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="清空",
            command=self.clear_items,
            width=100,
            height=40,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def create_items_table(self, parent):
        """创建采购明细表格"""
        self.items_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.items_container.pack(fill="x", padx=20, pady=10)
        
        # 标题行
        header = ctk.CTkFrame(self.items_container, fg_color="#3c3c3c")
        header.pack(fill="x", pady=1)
        
        columns = ["商品名称", "数量", "单价", "小计", "操作"]
        widths = [200, 100, 100, 150, 80]
        
        for i, (col, w) in enumerate(zip(columns, widths)):
            label = ctk.CTkLabel(header, text=col, width=w, font=ctk.CTkFont(size=12, weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5)
        
        self.items_data = ctk.CTkFrame(self.items_container, fg_color="transparent")
        self.items_data.pack(fill="x")
        
        self.item_rows = []
    
    def update_items_display(self):
        """更新采购明细显示"""
        for row_widgets in self.item_rows:
            for w in row_widgets:
                w.destroy()
        self.item_rows.clear()
        
        total = 0
        for i, item in enumerate(self.purchase_items):
            row_frame = ctk.CTkFrame(self.items_data, fg_color="#2d2d2d" if i % 2 == 0 else "#3a3a3a")
            row_frame.pack(fill="x", pady=1)
            
            name_label = ctk.CTkLabel(row_frame, text=item['product_name'], width=200)
            name_label.grid(row=0, column=0, padx=5, pady=5)
            
            qty_label = ctk.CTkLabel(row_frame, text=str(item['quantity']), width=100)
            qty_label.grid(row=0, column=1, padx=5, pady=5)
            
            price_label = ctk.CTkLabel(row_frame, text=f"¥{item['unit_price']:.2f}", width=100)
            price_label.grid(row=0, column=2, padx=5, pady=5)
            
            subtotal = item['quantity'] * item['unit_price']
            total += subtotal
            subtotal_label = ctk.CTkLabel(row_frame, text=f"¥{subtotal:.2f}", width=150)
            subtotal_label.grid(row=0, column=3, padx=5, pady=5)
            
            delete_btn = ctk.CTkButton(
                row_frame,
                text="删除",
                width=60,
                height=25,
                fg_color="#e74c3c",
                command=lambda idx=i: self.delete_item(idx)
            )
            delete_btn.grid(row=0, column=4, padx=5, pady=5)
            
            self.item_rows.append([name_label, qty_label, price_label, subtotal_label, delete_btn])
        
        self.total_label.configure(text=f"¥{total:.2f}")
    
    def create_purchase_list_card(self):
        """创建采购记录卡片"""
        card = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2d2d2d")
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="📋 采购记录",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        title.pack(pady=10)
        
        # 采购记录表格
        columns = ("采购单号", "供应商", "总金额", "状态", "创建日期")
        self.purchase_tree = ctk.CTkScrollableFrame(card, height=300)
        self.purchase_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题行
        header = ctk.CTkFrame(self.purchase_tree, fg_color="#3c3c3c")
        header.pack(fill="x", pady=1)
        
        for i, col in enumerate(columns):
            label = ctk.CTkLabel(header, text=col, width=150, font=ctk.CTkFont(size=12, weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5)
        
        self.purchase_container = ctk.CTkFrame(self.purchase_tree, fg_color="transparent")
        self.purchase_container.pack(fill="x")
        
        self.purchase_rows = []
    
    # ... 其他方法（load_suppliers, load_products, add_supplier, add_purchase_item, 
    # create_purchase, refresh_purchases, delete_item, clear_items等）