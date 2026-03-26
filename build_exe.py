# build_exe.py - 打包配置文件
import os
import sys
import PyInstaller.__main__

def build():
    """打包程序"""
    
    # 程序图标（如果有的话）
    icon_path = 'icon.ico'  # 可以放一个图标文件
    
    # PyInstaller 参数
    args = [
        'main.py',  # 主程序文件
        '--name=手机维修管理系统',  # 程序名称
        '--onefile',  # 打包成单个exe文件
        '--windowed',  # 不显示命令行窗口（纯GUI程序）
        '--noconsole',  # 同--windowed
        '--add-data=config.py;.',  # 添加配置文件（Windows用;分隔）
        '--add-data=database.py;.',
        '--add-data=gui;gui',
        '--hidden-import=tkinter',
        '--hidden-import=sqlite3',
        '--hidden-import=datetime',
        '--hidden-import=uuid',
        '--clean',  # 清理临时文件
        '--log-level=INFO',
    ]
    
    # 如果存在图标文件，添加图标
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    
    # 执行打包
    PyInstaller.__main__.run(args)
    
    print("\n" + "="*50)
    print("打包完成！")
    print("可执行文件位置：dist/手机维修管理系统.exe")
    print("="*50)

if __name__ == '__main__':
    build()
    