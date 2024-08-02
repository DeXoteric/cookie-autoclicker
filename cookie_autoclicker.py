import random
import time
from pathlib import Path

from pynput import keyboard
from selenium import webdriver
from selenium.common import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

PAGE_URL: str = "https://orteil.dashnet.org/cookieclicker/"
ADDBLOCK_URL: str = "/home/dexoteric/Downloads/uBlock0_1.58.0.firefox.signed.xpi"
MAX_INTERVAL: float = 600
INTERVAL_INCREMENT: float = 1.01
INITIAL_INTERVAL: float = 15
PAUSE_KEY_COMBINATION: set = {keyboard.Key.cmd, keyboard.Key.pause}
SAVE_KEY_COMBINATION: set = {keyboard.Key.cmd, keyboard.Key.scroll_lock}
CLICK_KEY_COMBINATION: set = {keyboard.Key.cmd, keyboard.Key.print_screen}
INTERVAL_CHANCE: float = 0.1
INTERVAL_MULTIPLAYER: float = 5


class CookieAutoclicker:
    def __init__(self) -> None:
        self.driver: webdriver.Firefox
        self.options_btn: WebElement
        self.big_cookie: WebElement
        self.periodic_check_time: float
        self.next_purchase_time: float
        self.purchase_interval_increment: float
        self.is_buff_active: float = False
        self.is_game_paused: float = False
        self.keys_pressed: set = set()
        self.memory_management_interval: float

    def setup(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.install_addon(ADDBLOCK_URL)

        self.driver.get(PAGE_URL)

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
            self.purchase_interval_increment = INITIAL_INTERVAL

        self.next_purchase_time = time.time() + self.purchase_interval_increment

        self.memory_management_interval = time.time() + 300

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

    def cookie_autoclicker(self) -> None:
        while True:
            if not self.is_game_paused:
                self.click_big_cookie()
                self.click_lucky_cookie()

                try:
                    self.is_buff_active = self.driver.find_element(
                        By.CSS_SELECTOR, ".crate.enabled.buff"
                    ).is_displayed()
                except StaleElementReferenceException:
                    continue
                except NoSuchElementException:
                    self.is_buff_active = False

                if time.time() > self.periodic_check_time:
                    self.close_notes()
                    self.periodic_check_time = time.time() + 5

                if not self.is_buff_active:
                    if time.time() > self.next_purchase_time:
                        self.buy_upgrades()
                        self.buy_products()
                        if self.purchase_interval_increment < MAX_INTERVAL:
                            self.purchase_interval_increment *= INTERVAL_INCREMENT
                            print(self.purchase_interval_increment)
                        if random.random() <= INTERVAL_CHANCE:
                            print(f"x{INTERVAL_MULTIPLAYER}")
                            self.next_purchase_time = time.time() + (
                                self.purchase_interval_increment * INTERVAL_MULTIPLAYER
                            )
                        else:
                            print(self.purchase_interval_increment)
                            self.next_purchase_time = (
                                time.time() + self.purchase_interval_increment
                            )
                    self.auto_save()

                self.spawn_golden_cookie()

                time.sleep(0.1)

            elif self.is_game_paused:
                time.sleep(0.1)

    def click_big_cookie(self):
        try:
            self.big_cookie.click()
        except ElementClickInterceptedException:
            pass

    def click_lucky_cookie(self):
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "shimmer").click()
            except ElementNotInteractableException:
                continue
            except ElementClickInterceptedException:
                continue
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                pass
            break

    def buy_upgrades(self):
        while True:
            try:
                upgrades = self.driver.find_element(
                    By.CSS_SELECTOR, "#upgrades"
                ).find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
                for upgrade in upgrades:
                    upgrade.click()
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                pass
            finally:
                time.sleep(0.1)
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
            finally:
                time.sleep(0.1)
            break

    def spawn_golden_cookie(self):
        while True:
            try:
                mana_text = self.driver.find_element(
                    By.CSS_SELECTOR, "#grimoireBarText"
                )

                current_mana = int(mana_text.text.split("/")[0].strip())
                max_mana = int(mana_text.text.split("/")[1].split(" ")[0].strip())
                is_mana_full = current_mana == max_mana

                mana_cost = int(
                    self.driver.find_element(
                        By.CSS_SELECTOR, "#grimoirePrice1"
                    ).text.strip()
                )

                if self.is_buff_active and is_mana_full and current_mana >= mana_cost:
                    self.driver.find_element(By.CSS_SELECTOR, "#grimoireSpell1").click()
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                pass
            except ValueError:
                continue
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
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, ".framed.note.nopic.nodesc"
            ).find_element(By.CSS_SELECTOR, ".close").click()
        except NoSuchElementException:
            pass

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

    def on_press(self, key):
        if key in PAUSE_KEY_COMBINATION:
            self.keys_pressed.add(key)
            if all(key in self.keys_pressed for key in PAUSE_KEY_COMBINATION):
                self.is_game_paused = not self.is_game_paused
        if key in SAVE_KEY_COMBINATION:
            self.keys_pressed.add(key)
            if all(key in self.keys_pressed for key in SAVE_KEY_COMBINATION):
                self.save_to_file()
        if key in CLICK_KEY_COMBINATION:
            self.keys_pressed.add(key)
            if all(key in self.keys_pressed for key in CLICK_KEY_COMBINATION):
                self.big_cookie.click()

    def on_release(self, key):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def run(self):
        self.setup()
        self.cookie_autoclicker()


if __name__ == "__main__":
    app = CookieAutoclicker()
    app.run()
