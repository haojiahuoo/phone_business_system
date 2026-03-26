# gui/inventory_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class InventoryView:
    def __init__(self, parent, system):
        self.system = system
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="库存管理")
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        # 工具栏
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(toolbar, text="搜索:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        ttk.Entry(toolbar, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        ttk.Button(toolbar, text="搜索", command=self.search).pack(side='left', padx=5)
        ttk.Button(toolbar, text="显示全部", command=self.refresh).pack(side='left', padx=5)
        ttk.Button(toolbar, text="添加商品", command=self.add_product).pack(side='left', padx=5)
        
        # 商品列表
        columns = ('ID', '商品编码', '商品名称', '品牌', '型号', '库存', '成本价', '售价', '位置')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        # 绑定双击事件
        self.tree.bind('<Double-Button-1>', self.edit_stock)
    
    def refresh(self):
        """刷新列表"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.system.get_all_inventory()
        for p in products:
            self.tree.insert('', 'end', values=(
                p[0], p[1], p[2], p[5], p[6], p[8], p[9], p[10], p[12]
            ))
    
    def search(self):
        """搜索商品"""
        keyword = self.search_var.get()
        if keyword:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            products = self.system.search_inventory(keyword)
            for p in products:
                self.tree.insert('', 'end', values=(
                    p[0], p[1], p[2], p[5], p[6], p[8], p[9], p[10], p[12]
                ))
    
    def add_product(self):
        """添加商品"""
        dialog = tk.Toplevel()
        dialog.title("添加商品")
        dialog.geometry("400x500")
        
        fields = {}
        labels = ['商品编码', '商品名称', '类别', '品牌', '型号', 
                  '成本价', '售价', '批发价', '初始库存', '位置', '最低库存']
        
        for i, label in enumerate(labels):
            ttk.Label(dialog, text=f"{label}:").grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(dialog, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            fields[label] = entry
        
        def save():
            try:
                self.system.add_inventory(
                    product_code=fields['商品编码'].get(),
                    product_name=fields['商品名称'].get(),
                    category=fields['类别'].get(),
                    brand=fields['品牌'].get(),
                    model=fields['型号'].get(),
                    cost_price=float(fields['成本价'].get()),
                    sell_price=float(fields['售价'].get()),
                    wholesale_price=float(fields['批发价'].get()),
                    quantity=int(fields['初始库存'].get()),
                    location=fields['位置'].get(),
                    min_stock=int(fields['最低库存'].get() or 0)
                )
                messagebox.showinfo("成功", "商品添加成功！")
                dialog.destroy()
                self.refresh()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败：{e}")
        
        ttk.Button(dialog, text="保存", command=save).grid(row=len(labels), column=1, pady=20)
    
    def edit_stock(self, event):
        """编辑库存数量"""
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        product_id = values[0]
        product_name = values[2]
        current_stock = values[5]
        
        new_quantity = simpledialog.askinteger(
            "修改库存", 
            f"商品：{product_name}\n当前库存：{current_stock}\n请输入新库存数量：",
            initialvalue=current_stock
        )
        
        if new_quantity is not None:
            change = new_quantity - current_stock
            self.system.update_stock(product_id, change)
            self.refresh()
            messagebox.showinfo("成功", f"库存已更新为：{new_quantity}")
            