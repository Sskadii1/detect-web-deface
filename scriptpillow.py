import os
import platform
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageChops
import time


URL = "https://abc.com"  
IMG_NAME = "gốc.png"      
NEW_IMG_NAME = "screenshot_new.png"


if platform.system() == "Windows":
    save_dir = r"C:\Users\test"
else:
    save_dir = "/home/Pictures/test"

os.makedirs(save_dir, exist_ok=True)


baseline_path = os.path.join(save_dir, IMG_NAME)
new_path = os.path.join(save_dir, NEW_IMG_NAME)


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,800')

driver = webdriver.Chrome(options=options)


print(f"Đang truy cập {URL} và chụp ảnh...")
driver.get(URL)
time.sleep(5)  
driver.save_screenshot(new_path)
driver.quit()


def images_are_different(img1_path, img2_path):
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')

    diff = ImageChops.difference(img1, img2)
    if diff.getbbox():
        print("Ảnh khác nhau - có thể website đã bị thay đổi.")
        diff.show()  # Tùy chọn: hiển thị phần khác biệt
        return True
    else:
        print("Ảnh giống nhau - không phát hiện thay đổi.")
        return False


if not os.path.exists(baseline_path):
    print("Chưa có ảnh gốc, lưu ảnh này làm ảnh gốc.")
    os.rename(new_path, baseline_path)
else:
    if images_are_different(baseline_path, new_path):
        print("Cảnh báo: website có thể đã bị thay đổi giao diện.")
    else:
        print("Website không có thay đổi đáng kể.")
    os.remove(new_path)
