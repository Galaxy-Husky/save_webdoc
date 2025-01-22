# import pyautogui
# import time

# print("将鼠标移动到插件图标的位置，3秒后获取坐标...")
# time.sleep(3)
# cor_x, cor_y = pyautogui.position()
# print(f"当前鼠标位置: ({cor_x}, {cor_y})")
# print("2秒后点击...")
# time.sleep(2)
# pyautogui.click(x=cor_x, y=cor_y)

# # addonlocation = pyautogui.locateOnScreen("gofullpage.png", confidence=0.3)
# # print(addonlocation)

import time

import pyautogui
from selenium.webdriver.common.by import By

from main import DOWNLOAD_DIR, init_driver


def check_permissions(directory):
    import os

    if not os.access(directory, os.W_OK):
        print(f"权限丢失: {directory} 不可写")
    else:
        print(f"权限正常: {directory} 可写")


# 启动浏览器并打开页面
driver = init_driver("edge")
target_url = "https://www.baidu.com"
driver.get(target_url)
window_handles = driver.window_handles
print(driver.current_window_handle)
for handle in window_handles:
    driver.switch_to.window(handle)
    url = driver.current_url
    print(url)
driver.switch_to.window(window_handles[0])

# 等待页面加载
time.sleep(2)

driver.find_element(By.TAG_NAME, "body").click()

# 等待一小段时间
time.sleep(1)

# 使用 PyAutoGUI 发送 Alt + Shift + P 组合键
pyautogui.keyDown("alt")
pyautogui.keyDown("shift")
pyautogui.press("p")
pyautogui.keyUp("shift")
pyautogui.keyUp("alt")
print("按下 alt + shift + p")

time.sleep(1)
window_handles = driver.window_handles
for handle in window_handles:
    driver.switch_to.window(handle)
    url = driver.current_url
    print(url)
    if "capture" in url:
        driver.switch_to.window(handle)
        print("切换到capture窗口")
        break

check_permissions(DOWNLOAD_DIR)
# driver.switch_to.window(window_handles[1])
# print(driver.current_window_handle)
time.sleep(1)


def save_file():
    """
    使用快捷键保存文件的函数
    执行 Ctrl+S 然后按 Enter 确认保存
    """
    # 按下 Ctrl+S 打开保存对话框
    pyautogui.keyDown("ctrl")
    pyautogui.press("s")
    pyautogui.keyUp("ctrl")
    print("按下 ctrl + s")

    # 等待保存对话框出现
    time.sleep(2)

    # 直接按回车键确认保存
    pyautogui.press("enter")
    print("按下 enter 确认保存")

    # 等待保存完成
    time.sleep(2)


save_file()

# driver.switch_to.window(window_handles[0])

# 关闭浏览器
# driver.quit()
