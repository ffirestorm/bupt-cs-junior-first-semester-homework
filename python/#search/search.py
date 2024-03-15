import os

def search_files(root_dir, search_strings):
    matched_files = []

    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if all(search_str in filename for search_str in search_strings):
                matched_files.append(os.path.join(foldername, filename))

    return matched_files

if __name__ == "__main__":
    # 设置要查找的根目录和文件名包含的字符串列表
    root_directory = "/path/to/your/directory"  # 替换为你要查找的根目录的路径
    search_strings = ["string1", "string2", "string3"]  # 替换为你要查找的字符串列表

    # 查找文件并打印结果
    matched_files = search_files(root_directory, search_strings)

    if matched_files:
        print("匹配的文件:")
        for file_path in matched_files:
            print(file_path)
    else:
        print("未找到匹配的文件。")