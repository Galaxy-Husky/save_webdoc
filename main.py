import os
import time

import pyautogui
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DOTENV_PATH = ".env"
assert load_dotenv(DOTENV_PATH)

DRIVER_TYPE = "edge"
USER_DATA_DIR_MAPPING = {
    "chrome": os.getenv("chrome_user_data_dir"),
    "edge": os.getenv("edge_user_data_dir"),
}
USER_DATA_DIR = USER_DATA_DIR_MAPPING[DRIVER_TYPE]
DOWNLOAD_DIR = os.getenv("download_dir")
URL = os.getenv("url")
PASSWORD = os.getenv("password")
CSS_SIDEBAR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-czvXZf.eCdaTP.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-eEvRUm.iAHRHS > div > div > div.wiki-tree-wrap > div"
SEC_BASE_SELECTOR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-bQFtmx.YfgBr.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-hgkBRQ.GFLjf > div > div > div.wiki-tree-wrap > div > div > ul > li:nth-child"


def verify_browser_options(driver_type):
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


def perform_with_retries_decorator(max_attempts=30, wait_time=1, raise_error=False):
    def perform_with_retries(func):
        def wrapper(*args):
            attempt = 0
            while attempt < max_attempts:
                try:
                    func(*args)
                    return
                except Exception as e:
                    print(f"尝试 {attempt + 1}/{max_attempts} 失败: {str(e)}")
                    attempt += 1
                    time.sleep(wait_time)
            msg = f"在 {max_attempts} 次尝试后操作仍未成功"
            if raise_error:
                raise TimeoutError(msg)
            else:
                print(msg)

        return wrapper

    return perform_with_retries


@perform_with_retries_decorator(max_attempts=2)
def wait_login(wait, pwd_element):
    wait.until(EC.presence_of_element_located(pwd_element))
    print("等待登录元素出现")


@perform_with_retries_decorator(max_attempts=2)
def close_popup(driver, wait, close_element):
    wait.until(EC.element_to_be_clickable(close_element))
    btn_close = driver.find_element(*close_element)
    btn_close.click()
    print("关闭弹窗")
    time.sleep(0.1)


@perform_with_retries_decorator(max_attempts=3)
def input_password(driver, wait, pwd_element, login_element):
    wait.until(EC.element_to_be_clickable(pwd_element))
    input_pwd = driver.find_element(*pwd_element)
    input_pwd.send_keys(PASSWORD)
    print("输入密码")
    time.sleep(0.1)

    wait.until(EC.element_to_be_clickable(login_element))
    btn_login = driver.find_element(*login_element)
    btn_login.click()
    print("点击登录")
    time.sleep(0.1)


def handle_login(driver):
    short_wait = WebDriverWait(driver, 3)
    pwd_element = (By.CLASS_NAME, "password-input")
    close_element = (By.CLASS_NAME, "lite-login-dialog__close")
    login_element = (By.CLASS_NAME, "password-required-button")
    wait_login(short_wait, pwd_element)
    close_popup(driver, short_wait, close_element)
    input_password(driver, short_wait, pwd_element, login_element)
    close_popup(driver, short_wait, close_element)


def click_expand_arrow(element):
    class_name = element.get_attribute("class")
    if "close" in class_name:
        element.click()
        time.sleep(0.5)


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
    # 按下 Alt + Shift + P 调用GoFullPage
    pyautogui.keyDown("alt")
    pyautogui.keyDown("shift")
    pyautogui.press("p")
    pyautogui.keyUp("shift")
    pyautogui.keyUp("alt")
    print("按下 alt + shift + p")
    time.sleep(1)

    def switch_to_capture_window():
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

    # perform_with_retries(switch_to_capture_window)


def operate_sections(driver):
    # wait = WebDriverWait(driver, 5)
    # drag = driver.find_element(By.CLASS_NAME, "wiki-flexible-line-v2")
    # actions = ActionChains(driver)

    last_num = 0
    while True:
        try:
            elements = driver.find_elements(
                By.CSS_SELECTOR,
                'span.wiki-tree-node-expand-arrow[data-selector="wiki-tree-node-switcher"]',
            )
            cur_num = len(elements)
            print(cur_num)
            if cur_num > 20:
                break
            if cur_num == last_num:
                print("没有未展开列表")
                break
            last_num = cur_num
            for element in elements:
                click_expand_arrow(element)
                break
        except Exception:
            print("error")
            break

    elements = driver.find_elements(
        By.CSS_SELECTOR, ".tree-title-content-title.ellipsis"
    )
    print(f"共有标题：{len(elements)}")
    # for element in elements:
    #     print(element.text)
    #     element.click()
    #     time.sleep(1)
    #     try:
    #         save_page(driver)
    #     except Exception as e:
    #         print(f"保存页面时发生错误: {str(e)}")
    #         continue

    # actions.drag_and_drop_by_offset(drag, 0, 15).perform()


def main():
    driver = init_driver(DRIVER_TYPE)
    driver.get(URL)
    print("打开网页")

    handle_login(driver)

    # save_page(driver)
    operate_sections(driver)
    # driver.quit()


if __name__ == "__main__":
    main()
