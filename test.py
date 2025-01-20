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

from main import init_driver

# 启动浏览器并打开页面
driver = init_driver("chrome")
driver.get("https://www.baidu.com")

# 等待页面加载
time.sleep(2)

# 最大化窗口并确保获得焦点
driver.maximize_window()
driver.switch_to.window(driver.current_window_handle)
driver.execute_script("window.focus();")

# 等待一小段时间
time.sleep(1)

# 使用 PyAutoGUI 发送 Alt + Shift + P 组合键
pyautogui.keyDown("alt")
pyautogui.keyDown("shift")
pyautogui.press("p")
pyautogui.keyUp("shift")
pyautogui.keyUp("alt")

# 等待观察效果
time.sleep(2)

# 关闭浏览器
# driver.quit()
