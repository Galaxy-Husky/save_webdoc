import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_TYPE = "edge"
USER_DATA_DIR_MAPPING = {
    "chrome": r"C:/Users/dxt75/AppData/Local/Google/Chrome/User Data",
    "edge": r"C:/Users/dxt75/AppData/Local/Microsoft/Edge/User Data",
}
DOWNLOAD_DIR = r"D:/ChromeDownload"
URL = "https://oed41vnioo.feishu.cn/wiki/Nw0bwlTCCiLeL2ksGVmcCSdanBg"
PASSWORD = "4p4@6814"
CSS_CLOSE = "#pp_popupContainer > div.ud__portal > div > div:nth-child(4) > div > div > div > div > div.lite-login-dialog__close"
CSS_PWD_INPUT = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > div.layout-row.password-required-container > div > input"
CSS_LOGIN_BTN = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > button"
CSS_SIDEBAR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-czvXZf.eCdaTP.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-eEvRUm.iAHRHS > div > div > div.wiki-tree-wrap > div"
SEC_BASE_SELECTOR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-bQFtmx.YfgBr.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-hgkBRQ.GFLjf > div > div > div.wiki-tree-wrap > div > div > ul > li:nth-child"


def verify_browser_options(driver_type):
    USER_DATA_DIR = USER_DATA_DIR_MAPPING[driver_type]
    if driver_type == "chrome":
        options = webdriver.ChromeOptions()
        print("使用 Chrome 浏览器")
        if not os.access(DOWNLOAD_DIR, os.W_OK):
            raise Exception(f"没有写权限: {DOWNLOAD_DIR}")
        prefs = {
            "download.default_directory": DOWNLOAD_DIR,  # 设置默认下载路径
        }
        options.add_experimental_option("prefs", prefs)
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--enable-logging")  # 启用日志
        # options.add_argument("--v=1")  # 设置日志级别
    elif driver_type == "firefox":
        options = webdriver.FirefoxOptions()
        print("使用 Firefox 浏览器")
    elif driver_type == "edge":
        options = webdriver.EdgeOptions()
        print("使用 edge 浏览器")
    else:
        raise ValueError("不支持的浏览器类型")
    if driver_type in ("chrome", "edge"):
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
        options.add_experimental_option("detach", True)
    return options


def init_driver(driver_type):
    options = verify_browser_options(driver_type)
    if driver_type == "chrome":
        driver = webdriver.Chrome(options=options)
    elif driver_type == "firefox":
        driver = webdriver.Firefox(options=options)
    elif driver_type == "edge":
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError("不支持的浏览器类型")
    driver.maximize_window()
    return driver


def close_popup(driver, wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_CLOSE)))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_CLOSE)))
    btn_close = driver.find_element(By.CSS_SELECTOR, CSS_CLOSE)
    btn_close.click()
    print("关闭弹窗")
    time.sleep(1)


def input_password(driver, wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_PWD_INPUT)))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_PWD_INPUT)))
    input_pwd = driver.find_element(By.CSS_SELECTOR, CSS_PWD_INPUT)
    input_pwd.send_keys(PASSWORD)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_LOGIN_BTN)))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_LOGIN_BTN)))
    btn_login = driver.find_element(By.CSS_SELECTOR, CSS_LOGIN_BTN)
    btn_login.click()


def handle_login(driver):
    short_wait = WebDriverWait(driver, 3)
    try:
        # 检查是否需要登录
        short_wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_PWD_INPUT))
        )
        print("需要登录")

        # 关闭弹窗
        close_popup(driver, short_wait)

        # 输入密码并登录
        input_password(driver, short_wait)
    except Exception:
        print("已经登录，跳过登录步骤")
    
    try:
        close_popup(driver, short_wait)
    except Exception:
        print("没有新的弹窗")


def adjust_firefox_zoom(driver):
    short_wait = WebDriverWait(driver, 2)
    max_attempts = 7
    attempt = 0
    while attempt < max_attempts:
        try:
            sidebar_element = short_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SIDEBAR))
            )
            if sidebar_element.is_displayed():
                print("侧边栏元素已出现")
                break
        except Exception:
            driver.set_context("chrome")
            win = driver.find_element(By.TAG_NAME, "html")
            win.send_keys(Keys.CONTROL + Keys.SUBTRACT)
            print(f"缩小页面，尝试次数: {attempt + 1}")
            attempt += 1
    driver.set_context("content")
    
    
def switch_page(driver, keyword):
    window_handles = driver.window_handles
    # print(f"共有页面：{len(window_handles)}")
    for handle in window_handles:
        driver.switch_to.window(handle)
        url = driver.current_url
        # print(url)
        if keyword in url:
            driver.switch_to.window(handle)
            print("切换窗口")
            break
        

def get_handles_info(driver):
    original_handles = driver.window_handles
    num_handles = len(original_handles)
    return num_handles
    
    
def save_page(driver):
    # 等待新窗口出现
    num_handles = get_handles_info(driver)
    print(num_handles)
    
    long_wait = WebDriverWait(driver, 10)
    # 按下 Alt + Shift + P 调用GoFullPage
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.press("p")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("alt")
    print("按下 alt + shift + p")
    time.sleep(1)
    
    max_attempts = 30  # 最大尝试次数
    attempt = 0
    while attempt < max_attempts:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "capture" in driver.current_url:
                time.sleep(1)
                print("已切换到截图窗口")
                # 继续执行保存操作
                # 按下 Ctrl+S 打开保存对话框
                pyautogui.keyDown("ctrl")
                pyautogui.press("s")
                pyautogui.keyUp("ctrl")
                print("按下 ctrl + s")
                # 等待保存对话框出现
                time.sleep(1)
                # 直接按回车键确认保存
                pyautogui.press("enter")
                print("按下 enter 确认保存")
                time.sleep(1)
                driver.close()
                print("关闭保存页面")
                switch_page(driver, "feishu")
                return
        attempt += 1
        time.sleep(1)  # 短暂等待后重试
        if attempt == max_attempts:
            raise TimeoutError("未能找到截图窗口")

def operate_sections(driver):
    wait = WebDriverWait(driver, 5)
    drag = driver.find_element(By.CLASS_NAME, "wiki-flexible-line-v2")
    actions = ActionChains(driver)
    
    i = 0
    last_num = 0
    while True:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, 'span.wiki-tree-node-expand-arrow[data-selector="wiki-tree-node-switcher"]')
            cur_num = len(elements)
            print(cur_num)
            if cur_num > 20:
                break
            if cur_num == last_num:
                print("没有未展开列表")
                break
            last_num = cur_num
            for element in elements:
                class_name = element.get_attribute('class')
                if 'close' in class_name:
                    element.click()
                    i += 1
                    time.sleep(1)
                    break
        except Exception:
            print("error")
            break
        
    elements = driver.find_elements(By.CSS_SELECTOR, ".tree-title-content-title.ellipsis")
    print(len(elements))
    for element in elements:
        print(element.text)
        element.click()
        time.sleep(2)
        try:
            save_page(driver)
        except Exception as e:
            print(f"保存页面时发生错误: {str(e)}")
            continue
        
    # actions.drag_and_drop_by_offset(drag, 0, 15).perform()


def main():
    driver = init_driver(DRIVER_TYPE)
    driver.get(URL)
    print("打开网页")

    handle_login(driver)

    if DRIVER_TYPE == "firefox":
        adjust_firefox_zoom(driver)

    # save_page(driver)
    operate_sections(driver)
    # driver.quit()


if __name__ == "__main__":
    main()
