import os

def scan_directory(directory, prefix=""):
    """
    递归扫描目录并打印文件结构，忽略指定目录
    :param directory: 要扫描的根目录
    :param prefix: 当前目录的前缀，用于格式化输出
    """
    # 获取目录下的所有文件和子目录，并按名称排序
    entries = sorted(os.listdir(directory))
    entries_count = len(entries)
    
    for i, entry in enumerate(entries):
        # 构造完整路径
        path = os.path.join(directory, entry)

        # 跳过 .git 文件夹
        if entry == ".git":
            continue
        
        # 确定是否是最后一个条目，调整前缀符号
        connector = "└── " if i == entries_count - 1 else "├── "
        
        # 打印当前文件或目录
        print(prefix + connector + entry)
        
        # 如果是目录，递归调用自己
        if os.path.isdir(path):
            # 如果是最后一个目录，缩进加 "    "，否则加 "│   "
            extension = "    " if i == entries_count - 1 else "│   "
            scan_directory(path, prefix + extension)

# 设置要扫描的根目录
root_directory = r"C:\Users\A-Znk\Credit-Insight"  # 或指定任意目录 
print(root_directory + "/")
scan_directory(root_directory)
