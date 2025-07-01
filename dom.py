import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import difflib

URL = "https://abcxyz.com"
DOM_NAME = "domoriginaldomoriginal.html"
NEW_DOM_NAME = "dom_new.html"


if platform.system() == "Windows":
    save_dir = r"C:\Users\abcxyz...."
else:
    save_dir = "/home/linhn/abcxyz"

os.makedirs(save_dir, exist_ok=True)
dom_path_old = os.path.join(save_dir, DOM_NAME)
dom_path_new = os.path.join(save_dir, NEW_DOM_NAME)


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,800')

driver = webdriver.Chrome(options=options)


print("Lấy DOM của website...")
driver.get(URL)
time.sleep(5)
page_source = driver.page_source
driver.quit()

with open(dom_path_new, "w", encoding="utf-8") as f:
    f.write(page_source)


def clean_dom(lines):
    skip_keywords = [
        "nonce", "timestamp", "tracking", "fb:app_id", "csrf", "data-testid",
        "data-client-token", "data-sigil", "async", "__CONF__", "random", "trace", "sentry"
    ]
    return [line for line in lines if not any(k in line for k in skip_keywords)]


def compare_dom(f1, f2):
    with open(f1, encoding="utf-8") as d1, open(f2, encoding="utf-8") as d2:
        lines1 = clean_dom(d1.readlines())
        lines2 = clean_dom(d2.readlines())
    return list(difflib.unified_diff(lines1, lines2, fromfile="DOM cũ", tofile="DOM mới"))


if not os.path.exists(dom_path_old):
    os.rename(dom_path_new, dom_path_old)
    print("Đã lưu DOM hiện tại làm baseline.")
else:
    diff = compare_dom(dom_path_old, dom_path_new)
    if diff:
        print("Cảnh báo: DOM đã thay đổi so với baseline!")
        for line in diff[:20]:  # In tối đa 20 dòng khác biệt
            print(line.strip())
    else:
        print("DOM không thay đổi.")
    os.remove(dom_path_new)
