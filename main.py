import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_TYPE = "chrome"
USER_DATA_DIR_MAPPING = {
    "chrome": r"C:/Users/Ping/AppData/Local/Google/Chrome/User Data",
    "edge": r"C:/Users/Ping/AppData/Local/Microsoft/Edge/User Data",
}
URL = "https://oed41vnioo.feishu.cn/wiki/Nw0bwlTCCiLeL2ksGVmcCSdanBg"
PASSWORD = "4p4@6814"
CSS_CLOSE = "#pp_popupContainer > div.ud__portal > div > div:nth-child(4) > div > div > div > div > div.lite-login-dialog__close"
CSS_PWD_INPUT = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > div.layout-row.password-required-container > div > input"
CSS_LOGIN_BTN = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > button"
CSS_SIDEBAR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-czvXZf.eCdaTP.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-eEvRUm.iAHRHS > div > div > div.wiki-tree-wrap > div"
SEC_BASE_SELECTOR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-bQFtmx.YfgBr.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-hgkBRQ.GFLjf > div > div > div.wiki-tree-wrap > div > div > ul > li:nth-child"
DOWNLOAD_DIR = r"E:/ChromeDownload"


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


def handle_login(driver, wait):
    """处理登录流程"""
    try:
        # 检查是否需要登录
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_PWD_INPUT))
        )
        print("需要登录")

        # 关闭首次弹窗
        close_popup(driver, wait)

        # 输入密码并登录
        input_password(driver, wait)

        # 关闭登录后弹窗
        close_popup(driver, wait)

    except Exception:
        print("已经登录，跳过登录步骤")


def adjust_firefox_zoom(driver):
    max_attempts = 7
    attempt = 0
    while attempt < max_attempts:
        try:
            sidebar_element = WebDriverWait(driver, 2).until(
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


def get_section_titles(driver, wait):
    for i in range(4, 18):
        try:
            sec_title = f"{SEC_BASE_SELECTOR}({i}) > div > div > div > div > span > span.tree-item-content-title-wrapper > a > div > span > span"
            title = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, sec_title))
            ).text
            print(f"{title}")
        except Exception:
            print(f"{i} 不存在或无法访问")
            continue


def main():
    driver = init_driver(DRIVER_TYPE)
    wait = WebDriverWait(driver, 20)

    driver.get(URL)
    print("打开网页")

    handle_login(driver, wait)

    if DRIVER_TYPE == "firefox":
        adjust_firefox_zoom(driver)

    get_section_titles(driver, wait)
    driver.quit()


if __name__ == "__main__":
    main()
