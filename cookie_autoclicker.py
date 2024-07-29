import time
from pathlib import Path

from selenium import webdriver
from selenium.common import (ElementClickInterceptedException,
                             ElementNotInteractableException,
                             NoSuchElementException,
                             StaleElementReferenceException)
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
        self.options_btn: WebElement
        self.big_cookie: WebElement
        self.periodic_check_time: float
        self.next_purchase_time: float
        self.purchase_interval_increment: float

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

        self.options_btn = self.driver.find_element(By.CSS_SELECTOR, ".subButton")

        self.driver.find_element(By.CSS_SELECTOR, ".cc_btn").click()

        if Path("./save.txt").exists():
            self.auto_load()

        self.volume_off()

        self.periodic_check_time = time.time() + 5

        if Path("./delay.txt").exists():
            with open("./delay.txt", "r", encoding="utf-8") as file:
                self.purchase_interval_increment = float(file.read())
        else:
            self.purchase_interval_increment = 0.1

        self.next_purchase_time = time.time() + self.purchase_interval_increment

    def cookie_autoclicker(self) -> None:
        while True:
            self.click_lucky_cookie()

            if time.time() > self.periodic_check_time:
                self.click_lucky_cookie()
                self.buy_upgrades()
                self.close_notes()
                self.periodic_check_time = time.time() + 5

            if time.time() > self.next_purchase_time:
                self.buy_products()
                if self.purchase_interval_increment < 60:
                    self.purchase_interval_increment += 0.1

                self.next_purchase_time = time.time() + self.purchase_interval_increment

            self.auto_save()

    def click_big_cookie(self):
        try:
            self.big_cookie.click()
        except ElementClickInterceptedException:
            pass
        finally:
            time.sleep(0.125)

    def click_lucky_cookie(self):
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "shimmer").click()
            except ElementNotInteractableException:
                continue
            except ElementClickInterceptedException:
                continue
            except NoSuchElementException:
                pass
            break

    def buy_upgrades(self):
        while True:
            try:
                upgrades = self.driver.find_elements(
                    By.CSS_SELECTOR, ".crate.upgrade.enabled"
                )
                for upgrade in upgrades:
                    upgrade.click()
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                pass
            break

    def buy_products(self):
        while True:
            try:
                products = self.driver.find_elements(
                    By.CSS_SELECTOR, ".product.unlocked.enabled"
                )
                products.reverse()
                for product in products:
                    product.click()
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                pass
            break

    def close_notes(self):
        while True:
            try:
                notes = self.driver.find_elements(
                    By.CSS_SELECTOR, ".framed.note.haspic.hasdesc"
                )
                for note in notes:
                    close_button = note.find_element(By.CSS_SELECTOR, ".close")
                    close_button.click()
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                pass
            break

    def auto_save(self):
        try:
            self.driver.find_element(By.XPATH, "//*/h3[contains(text(), 'Game saved')]")
        except NoSuchElementException:
            pass
        else:
            self.save_to_file()
            self.save_purchase_interval_to_file()

    def auto_load(self):
        self.options_btn.click()

        import_save_btn = self.driver.find_element(
            By.XPATH, "//*/a[contains(text(), 'Import save')]"
        )
        import_save_btn.click()

        string_to_load = ""
        with open("./save.txt", "r", encoding="utf-8") as file:
            string_to_load = file.read()

        text_area = self.driver.find_element(By.CSS_SELECTOR, "#textareaPrompt")
        text_area.send_keys(string_to_load)

        load_btn = self.driver.find_element(By.CSS_SELECTOR, "#promptOption0")
        load_btn.click()

        self.options_btn.click()

    def save_to_file(self):
        self.driver.find_element(
            By.CSS_SELECTOR, ".framed.note.nopic.nodesc"
        ).find_element(By.CSS_SELECTOR, ".close").click()

        self.options_btn.click()

        export_save_btn = self.driver.find_element(
            By.XPATH, "//*/a[contains(text(), 'Export save')]"
        )
        export_save_btn.click()

        string_to_save = self.driver.find_element(
            By.CSS_SELECTOR, "#textareaPrompt"
        ).get_attribute("value")
        with open("./save.txt", "w", encoding="utf-8") as file:
            file.write(str(string_to_save))

        done_btn = self.driver.find_element(By.CSS_SELECTOR, "#promptOption0")
        done_btn.click()

        self.options_btn.click()

    def save_purchase_interval_to_file(self):
        with open("./delay.txt", "w", encoding="utf-8") as file:
            file.write(str(self.purchase_interval_increment))

    def volume_off(self):
        self.options_btn.click()
        volume_slider = self.driver.find_element(By.CSS_SELECTOR, "#volumeSlider")
        volume_slider.click()
        volume_slider.send_keys(webdriver.Keys.HOME)
        self.options_btn.click()

    def run(self):
        self.setup()
        self.cookie_autoclicker()


if __name__ == "__main__":
    app = CookieAutoclicker()
    app.run()
