# main.py - CustomTkinter 版本
import sys
import os
import traceback
from datetime import datetime
from database_mysql import PhoneBusinessSystem
import customtkinter as ctk

# 设置 CustomTkinter 外观
ctk.set_appearance_mode("dark")  # 可选: "dark", "light", "system"
ctk.set_default_color_theme("green")  # 可选: "blue", "green", "dark-blue"

# 重要：将程序所在目录设置为工作目录
def set_working_directory():
    """设置工作目录为程序所在目录"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe 运行
        application_path = os.path.dirname(sys.executable)
    else:
        # 如果是 Python 脚本运行
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # 切换到程序所在目录
    os.chdir(application_path)
    
    # 添加程序目录到系统路径
    if application_path not in sys.path:
        sys.path.insert(0, application_path)
    
    return application_path

# 设置工作目录
app_path = set_working_directory()
print(f"程序运行目录: {app_path}")

# 创建错误日志函数
def setup_error_log():
    """设置错误日志"""
    log_dir = os.path.join(app_path, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f'error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    return log_file

def log_error(log_file, error_msg):
    """记录错误到文件"""
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"="*60 + "\n")
            f.write(f"错误时间: {datetime.now()}\n")
            f.write(f"错误信息: {error_msg}\n")
            f.write(f"详细堆栈:\n{traceback.format_exc()}\n")
            f.write(f"="*60 + "\n\n")
        print(f"错误已记录到: {log_file}")
    except Exception as e:
        print(f"无法写入日志: {e}")

def show_error_dialog(error_msg):
    """显示错误对话框"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("启动错误", f"程序启动失败！\n\n{error_msg}\n\n请查看 logs 文件夹中的错误日志")
        root.destroy()
    except:
        print(f"错误信息: {error_msg}")

def main():
    """主函数"""
    log_file = setup_error_log()
    
    try:
        print("1. 开始导入模块...")
        print(f"当前工作目录: {os.getcwd()}")
        
        # 导入必要的模块
        import tkinter as tk
        print("✓ tkinter 导入成功")
        
        from tkinter import messagebox, simpledialog
        print("✓ tkinter 子模块导入成功")
        
        import sqlite3
        print("✓ sqlite3 导入成功")
        
        # 导入项目模块
        print("2. 导入项目模块...")
        
        # 检查必要文件是否存在
        required_files = ['database_mysql.py', 'config.py', 'gui']
        for file in required_files:
            if os.path.exists(file):
                print(f"✓ {file} 存在")
            else:
                print(f"✗ {file} 不存在")
                print(f"当前目录内容: {os.listdir('.')}")
                raise FileNotFoundError(f"找不到文件: {file}")
        
        # 导入 database 模块
        from database_mysql import PhoneBusinessSystem
        print("✓ database 模块导入成功")
        
        # 导入 CustomTkinter gui 模块
        from gui.main_window_ctk import MainWindow
        print("✓ gui 模块导入成功")
        
        print("3. 初始化数据库...")
        
        # 确保 data 目录存在
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"✓ 创建数据目录: {data_dir}")
        
        # 初始化系统
        db_path = os.path.join(data_dir, 'phone_business.db')
        system = PhoneBusinessSystem(db_path)
        print(f"✓ 数据库初始化成功: {db_path}")
        
        print("4. 创建主窗口...")
        
        # 创建 CustomTkinter 主窗口
        root = ctk.CTk()
        root.title("手机维修与二手机买卖管理系统")
        root.geometry("1400x800")
        
        # 设置窗口最小大小
        root.minsize(1200, 700)
        
        # 设置窗口居中
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 1400) // 2
        y = (screen_height - 800) // 2
        root.geometry(f"1400x800+{x}+{y}")
        
        # 设置窗口图标（如果有）
        try:
            icon_path = os.path.join(app_path, 'icon.ico')
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except:
            pass
        
        app = MainWindow(root, system)
        
        def on_closing():
            try:
                system.close()
            except:
                pass
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("5. 启动主循环...")
        print("程序启动成功！")
        
        root.mainloop()
        
    except Exception as e:
        error_msg = f"{str(e)}\n\n{traceback.format_exc()}"
        log_error(log_file, error_msg)
        print(f"启动失败: {e}")
        print(f"详细错误请查看: {log_file}")
        
        try:
            show_error_dialog(str(e))
        except:
            pass
        
        input("\n按回车键退出...")
        sys.exit(1)

if __name__ == '__main__':
    main()