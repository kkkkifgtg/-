import os
import sys
import time
import platform
import shutil


def force_delete(file_path, retries=3, delay=2):
    """
    强制删除文件或文件夹（跨平台）
    :param file_path: 文件/文件夹路径
    :param retries: 重试次数
    :param delay: 重试间隔时间（秒）
    """
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return

    # 根据操作系统选择删除方式
    system = platform.system()

    for _ in range(retries):
        try:
            if system == "Windows":
                # 使用 cmd 删除（绕过部分权限限制）
                os.system(f'cmd /c "del /f /q {file_path}"')
                # 处理顽固文件
                if os.path.exists(file_path):
                    os.system(f'cmd /c "rmdir /s /q {file_path}"')
            else:
                # macOS/Linux 使用 rm -rf
                os.system(f'rm -rf "{file_path}"')

            print(f"成功删除 {file_path}")
            return

        except Exception as e:
            print(f"删除失败: {e}")
            time.sleep(delay)

    print(f"经过 {retries} 次尝试仍无法删除 {file_path}")


def main():
    if len(sys.argv) < 2:
        print("用法: python force_delete.py [文件/文件夹路径]")
        return

    target = sys.argv[1]

    # 检查是否为文件夹
    if os.path.isdir(target):
        print(f"正在强制删除文件夹: {target}")
        force_delete(target)
    else:
        print(f"正在强制删除文件: {target}")
        force_delete(target)


if __name__ == "__main__":
    main()