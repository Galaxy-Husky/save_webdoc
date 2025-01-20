import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_TYPE = "chrome"
USER_DATA_DIR = r"C:/Users/Ping/AppData/Local/Google/Chrome/User Data"
URL = "https://oed41vnioo.feishu.cn/wiki/Nw0bwlTCCiLeL2ksGVmcCSdanBg"
PASSWORD = "4p4@6814"
CSS_CLOSE = "#pp_popupContainer > div.ud__portal > div > div:nth-child(4) > div > div > div > div > div.lite-login-dialog__close"
CSS_PWD_INPUT = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > div.layout-row.password-required-container > div > input"
CSS_LOGIN_BTN = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.app-main.main__content.layout-column > div.suite-body.flex.layout-column > div > div.sc-domHXz.TEzci > div > button"
CSS_SIDEBAR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-czvXZf.eCdaTP.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-eEvRUm.iAHRHS > div > div > div.wiki-tree-wrap > div"
SEC_BASE_SELECTOR = "#mainContainer > div.app-main-container.flex.layout-row.explorer-v3.is-suite > div.sc-bQFtmx.YfgBr.wiki-sidebar-wrap.wiki-sidebar-responsive-wrap.disabled-contextmenu > div:nth-child(1) > div > div.sc-hgkBRQ.GFLjf > div > div > div.wiki-tree-wrap > div > div > ul > li:nth-child"


def verify_browser_options(driver_type):
    if driver_type == "chrome":
        options = webdriver.ChromeOptions()
        print("使用 Chrome 浏览器")
        options.add_experimental_option("detach", True)
        options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    elif driver_type == "firefox":
        options = webdriver.FirefoxOptions()
        print("使用 Firefox 浏览器")
    else:
        raise ValueError("不支持的浏览器类型")
    return options


def init_driver(driver_type):
    options = verify_browser_options(driver_type)
    driver = (
        webdriver.Chrome(options=options)
        if driver_type == "chrome"
        else webdriver.Firefox(options=options)
    )
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

    # get_section_titles(driver, wait)
    body = driver.find_element(By.TAG_NAME, "body")
    body.click()
    actions = ActionChains(driver)
    actions.key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys("p").key_up(
        Keys.SHIFT
    ).key_up(Keys.ALT)
    actions.perform()
    print("按下 alt + shift + p")

    time.sleep(3)
    actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)
    actions.perform()
    print("按下 ctrl + a")

    driver.quit()


if __name__ == "__main__":
    main()
