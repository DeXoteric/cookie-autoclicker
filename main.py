from selenium import webdriver


def main():
    driver = webdriver.Firefox()

    driver.install_addon("/home/dexoteric/Downloads/uBlock0_1.58.0.firefox.signed.xpi")
    driver.get("https://orteil.dashnet.org/cookieclicker/")


if __name__ == "__main__":
    main()
