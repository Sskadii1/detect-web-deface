import os
import platform
from datetime import datetime


TARGET_FILES = [
    "/var/www/html/index.html",
    "/var/www/html/style.css"
]

def check_file_metadata(path):
    try:
        stat = os.stat(path)
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        info = f"File: {path}\nLần sửa đổi cuối: {mtime}"

        if platform.system() == "Linux":
            import pwd, grp
            user = pwd.getpwuid(stat.st_uid).pw_name
            group = grp.getgrgid(stat.st_gid).gr_name
            info += f"\nNgười sửa cuối: {user}, Nhóm: {group}"
        return info
    except FileNotFoundError:
        return f"Không tìm thấy file hehehe: {path}"


for path in TARGET_FILES:
    print("---")
    print(check_file_metadata(path))
