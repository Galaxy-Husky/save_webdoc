import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PASSWORD = "4p4@6814"
CSS_CLOSE = "#pp_popupContainer > div.ud__portal > div > div:nth-child(4) > div > div > div > div > div.lite-login-dialog__close"
CSS_PWD_INPUT = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > div.layout-row.password-required-container > div > input"
CSS_LOGIN_BTN = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > button"
CSS_SIDEBAR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-czvXZf.eCdaTP.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-eEvRUm.iAHRHS > div > div > div.wiki-tree-wrap > div"

options = webdriver.FirefoxOptions()
# options.add_experimental_option("detach", True)  # for Chrome driver
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 20)
driver.maximize_window()
driver.get("https://oed41vnioo.feishu.cn/wiki/Nw0bwlTCCiLeL2ksGVmcCSdanBg")

# 第一次关闭弹窗
# 先等待元素出现在DOM中
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_CLOSE)))
# 然后等待元素可点击
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_CLOSE)))
# 最后再查找和点击元素
btn_close = driver.find_element(By.CSS_SELECTOR, CSS_CLOSE)
btn_close.click()
time.sleep(1)

# 输入密码
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_PWD_INPUT)))
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_PWD_INPUT)))
input_pwd = driver.find_element(By.CSS_SELECTOR, CSS_PWD_INPUT)
input_pwd.send_keys(PASSWORD)

# 点击登录按钮
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_LOGIN_BTN)))
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_LOGIN_BTN)))
btn_login = driver.find_element(By.CSS_SELECTOR, CSS_LOGIN_BTN)
btn_login.click()

# 第二次关闭弹窗
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_CLOSE)))
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_CLOSE)))
btn_close = driver.find_element(By.CSS_SELECTOR, CSS_CLOSE)
btn_close.click()
time.sleep(1)


max_attempts = 7
attempt = 0
while attempt < max_attempts:
    try:
        # 尝试查找侧边栏元素
        sidebar_element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SIDEBAR))
        )
        if sidebar_element.is_displayed():
            print("侧边栏元素已出现")
            break
    except Exception:
        # 如果未找到元素，缩小页面字体（Ctrl + -）
        driver.set_context("chrome")
        win = driver.find_element(By.TAG_NAME, "html")
        win.send_keys(Keys.CONTROL + Keys.SUBTRACT)
        print(f"缩小页面，尝试次数: {attempt + 1}")
        attempt += 1
driver.set_context("content")

SEC_BASE_SELECTOR = "li.list-item-wrapper:nth-child"
SEC_UNFOLD_SELECTOR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-czvXZf.eCdaTP.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-eEvRUm.iAHRHS > div > div > div.wiki-tree-wrap > div > div > ul > li:nth-child(4) > div > div > span"
for i in range(4, 18):
    print(i)
    try:
        sec_title = f"{SEC_BASE_SELECTOR}({i}) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2) > a:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)"
        title = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, sec_title))
        ).text
        print(f"{title}")

    except Exception:
        print(f"{i} 不存在或无法访问")
        continue
