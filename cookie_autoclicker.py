import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class CookieAutoclicker:
    def __init__(self) -> None:
        self.driver: webdriver.Firefox
        self.ublock_path: str = (
            "/home/dexoteric/Downloads/uBlock0_1.58.0.firefox.signed.xpi"
        )
        self.page_url: str = "https://orteil.dashnet.org/cookieclicker/"
        self.big_cookie: WebElement

    def setup(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.install_addon(self.ublock_path)

        self.driver.get(self.page_url)

        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.ID, "langSelect-EN"))
        ).click()

        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.ID, "bigCookie"))
        )
        self.big_cookie = self.driver.find_element(By.ID, "bigCookie")

        time.sleep(1)

        self.driver.find_element(By.CSS_SELECTOR, ".cc_btn").click()

    def cookie_autoclicker(self) -> None:
        while True:
            self.big_cookie.click()

            self.click_lucky_cookie()
            self.buy_upgrades()
            self.buy_products()

    def click_lucky_cookie(self):
        try:
            lucky_cookie = self.driver.find_element(By.CLASS_NAME, "shimmer")
        except NoSuchElementException:
            pass
        else:
            lucky_cookie.click()

    def buy_upgrades(self):
        upgrades = self.driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
        for upgrade in upgrades:
            upgrade.click()

    def buy_products(self):
        products = self.driver.find_elements(
            By.CSS_SELECTOR, ".product.unlocked.enabled"
        )
        for product in products:
            product.click()

    def run(self):
        self.setup()
        self.cookie_autoclicker()


if __name__ == "__main__":
    app = CookieAutoclicker()
    app.run()
