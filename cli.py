# cli.py - 命令行版本
from database_mysql import PhoneBusinessSystem
import sys

def main():
    """命令行版本入口"""
    system = PhoneBusinessSystem()
    
    while True:
        print("\n" + "="*50)
        print("手机维修与二手机买卖管理系统 - 命令行版")
        print("="*50)
        print("1. 库存管理")
        print("2. 客户管理")
        print("3. 销售管理")
        print("4. 维修管理")
        print("5. 报表统计")
        print("6. 供应商管理")
        print("0. 退出")
        print("="*50)
        
        choice = input("请选择操作：").strip()
        
        if choice == '1':
            inventory_menu(system)
        elif choice == '2':
            customer_menu(system)
        elif choice == '3':
            sales_menu(system)
        elif choice == '4':
            repair_menu(system)
        elif choice == '5':
            report_menu(system)
        elif choice == '6':
            supplier_menu(system)
        elif choice == '0':
            system.close()
            print("谢谢使用，再见！")
            break
        else:
            print("无效选择，请重新输入！")

def inventory_menu(system):
    """库存管理菜单"""
    while True:
        print("\n--- 库存管理 ---")
        print("1. 查看所有商品")
        print("2. 添加商品")
        print("3. 搜索商品")
        print("4. 修改库存")
        print("0. 返回上级菜单")
        
        choice = input("请选择：").strip()
        
        if choice == '1':
            products = system.get_all_inventory()
            print("\n商品列表：")
            print("-"*80)
            for p in products:
                print(f"ID:{p[0]} | {p[2]} | 库存:{p[8]} | 售价:¥{p[10]} | 成本:¥{p[9]}")
            print("-"*80)
        
        elif choice == '2':
            print("\n添加新商品：")
            product_code = input("商品编码：")
            product_name = input("商品名称：")
            category = input("类别：")
            brand = input("品牌：")
            model = input("型号：")
            cost_price = float(input("成本价："))
            sell_price = float(input("售价："))
            wholesale_price = float(input("批发价："))
            quantity = int(input("初始库存："))
            
            system.add_inventory(
                product_code, product_name, category, brand, model,
                cost_price, sell_price, wholesale_price, quantity
            )
            print("✓ 商品添加成功！")
        
        elif choice == '3':
            keyword = input("请输入搜索关键词：")
            products = system.search_inventory(keyword)
            for p in products:
                print(f"{p[2]} - 库存:{p[8]} - 售价:¥{p[10]}")
        
        elif choice == '4':
            product_id = int(input("商品ID："))
            new_quantity = int(input("新库存数量："))
            # 获取当前库存
            system.cursor.execute('SELECT quantity FROM inventory WHERE id = ?', (product_id,))
            current = system.cursor.fetchone()[0]
            system.update_stock(product_id, new_quantity - current)
            print("✓ 库存已更新！")
        
        elif choice == '0':
            break

def customer_menu(system):
    """客户管理菜单"""
    while True:
        print("\n--- 客户管理 ---")
        print("1. 查看所有客户")
        print("2. 添加客户")
        print("3. 搜索客户")
        print("0. 返回上级菜单")
        
        choice = input("请选择：").strip()
        
        if choice == '1':
            customers = system.get_all_customers()
            print("\n客户列表：")
            print("-"*60)
            for c in customers:
                print(f"ID:{c[0]} | {c[1]} | {c[2]} | 类型:{c[5]}")
            print("-"*60)
        
        elif choice == '2':
            name = input("姓名：")
            phone = input("电话：")
            wechat = input("微信：")
            customer_type = input("客户类型(retail/wholesale/online)：")
            system.add_customer(name, phone, wechat, None, customer_type)
            print("✓ 客户添加成功！")
        
        elif choice == '3':
            keyword = input("请输入搜索关键词：")
            customers = system.search_customers(keyword)
            for c in customers:
                print(f"{c[1]} - {c[2]} - {c[3]}")
        
        elif choice == '0':
            break

def sales_menu(system):
    """销售管理菜单"""
    # 先查看所有客户
    customers = system.get_all_customers()
    if not customers:
        print("请先添加客户！")
        return
    
    print("\n客户列表：")
    for c in customers:
        print(f"{c[0]}. {c[1]} - {c[2]}")
    
    customer_id = int(input("请选择客户ID："))
    order_type = input("订单类型(retail/wholesale/online)：")
    
    items = []
    while True:
        # 显示商品列表
        products = system.get_all_inventory()
        print("\n商品列表：")
        for p in products:
            if p[8] > 0:
                print(f"{p[0]}. {p[2]} - 库存:{p[8]} - 售价:¥{p[10]}")
        
        product_id = input("选择商品ID（输入0结束）：")
        if product_id == '0':
            break
        
        quantity = int(input("数量："))
        items.append({'inventory_id': int(product_id), 'quantity': quantity})
    
    if items:
        discount = float(input("折扣金额（0为无折扣）："))
        order_no, amount = system.create_sales_order(customer_id, order_type, items, discount)
        print(f"\n✓ 订单创建成功！")
        print(f"订单号：{order_no}")
        print(f"订单金额：¥{amount}")
        
        pay_now = input("是否现在收款？(y/n)：")
        if pay_now.lower() == 'y':
            paid = float(input("收款金额："))
            # 获取订单ID
            system.cursor.execute('SELECT id FROM sales_orders WHERE order_no = ?', (order_no,))
            order_id = system.cursor.fetchone()[0]
            system.receive_payment(order_id, paid)
            print("✓ 收款成功！")

def repair_menu(system):
    """维修管理菜单"""
    customers = system.get_all_customers()
    if not customers:
        print("请先添加客户！")
        return
    
    print("\n客户列表：")
    for c in customers:
        print(f"{c[0]}. {c[1]} - {c[2]}")
    
    customer_id = int(input("请选择客户ID："))
    device_brand = input("设备品牌：")
    device_model = input("设备型号：")
    problem_desc = input("问题描述：")
    repair_type = input("维修类型(hardware/software/water_damage)：")
    repair_cost = float(input("维修费："))
    parts_cost = float(input("配件费："))
    deposit = float(input("定金："))
    
    order_no = system.create_repair_order(
        customer_id, device_brand, device_model, problem_desc,
        repair_type, repair_cost, parts_cost, deposit
    )
    
    print(f"\n✓ 维修订单创建成功！")
    print(f"订单号：{order_no}")
    
    complete_now = input("维修是否已完成？(y/n)：")
    if complete_now.lower() == 'y':
        system.cursor.execute('SELECT id FROM repair_orders WHERE order_no = ?', (order_no,))
        order_id = system.cursor.fetchone()[0]
        remaining = system.complete_repair(order_id)
        if remaining > 0:
            print(f"还需收款：¥{remaining}")

def report_menu(system):
    """报表统计菜单"""
    profit = system.get_profit_loss()
    print("\n=== 利润统计 ===")
    print(f"总收入：¥{profit['total_income']:.2f}")
    print(f"总支出：¥{profit['total_expense']:.2f}")
    print(f"利润：¥{profit['profit']:.2f}")
    
    sales_report = system.get_sales_report()
    print("\n=== 销售报表 ===")
    for row in sales_report:
        print(f"{row[0]}: 订单数:{row[1]}, 销售额:¥{row[2]:.2f}, 已收款:¥{row[3]:.2f}")
    
    inv_value = system.get_inventory_value()
    print(f"\n库存总价值：¥{inv_value:.2f}")

def supplier_menu(system):
    """供应商管理菜单"""
    while True:
        print("\n--- 供应商管理 ---")
        print("1. 查看所有供应商")
        print("2. 添加供应商")
        print("3. 创建采购订单")
        print("0. 返回上级菜单")
        
        choice = input("请选择：").strip()
        
        if choice == '1':
            suppliers = system.get_all_suppliers()
            for s in suppliers:
                print(f"{s[0]}. {s[1]} - {s[2]} - 联系人:{s[4]}")
        
        elif choice == '2':
            name = input("供应商名称：")
            phone = input("电话：")
            contact = input("联系人：")
            system.add_supplier(name, phone, None, contact)
            print("✓ 供应商添加成功！")
        
        elif choice == '3':
            # 创建采购订单
            suppliers = system.get_all_suppliers()
            print("供应商列表：")
            for s in suppliers:
                print(f"{s[0]}. {s[1]}")
            
            supplier_id = int(input("选择供应商ID："))
            
            items = []
            while True:
                product_id = input("商品ID（输入0结束）：")
                if product_id == '0':
                    break
                quantity = int(input("数量："))
                unit_price = float(input("单价："))
                items.append({
                    'inventory_id': int(product_id),
                    'quantity': quantity,
                    'unit_price': unit_price
                })
            
            if items:
                order_no = system.create_purchase_order(supplier_id, items)
                print(f"✓ 采购订单创建成功！订单号：{order_no}")
                
                receive = input("是否收货入库？(y/n)：")
                if receive.lower() == 'y':
                    system.cursor.execute('SELECT id FROM purchase_orders WHERE order_no = ?', (order_no,))
                    purchase_id = system.cursor.fetchone()[0]
                    system.receive_purchase(purchase_id)
                    print("✓ 收货入库成功！")

if __name__ == '__main__':
    main()