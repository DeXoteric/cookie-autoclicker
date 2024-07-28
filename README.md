# (Work In Progress) CookieAutoclicker

CookieAutoclicker is a simple automation script for the game Cookie Clicker, created using Python and Selenium.

## Features

- Automatically clicks the big cookie.
- Automatically clicks lucky cookies when they appear.
- Automatically purchases available upgrades and products.
- Automatically loads and saves state of the game.

## Requirements

- Python 3.x
- Firefox Web Browser
- Geckodriver (for Firefox)
- uBlock Origin (optional)

## Installation

1. Clone this repository using HTTPS:
   ```sh
   git clone https://github.com/DeXoteric/CookieAutoclicker.git
   ```

   or using SSH:
   ```sh
   git clone git@github.com:DeXoteric/CookieAutoclicker.git
   ```

2. Install the required Python packages, including WebDriver:
   ```sh
   pip install -r requirements.txt
   ```

3. Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) for your system and ensure it is in your PATH. If Geckodriver is not in your PATH, specify the path directly when initializing the WebDriver:

   ```python
   from selenium import webdriver

   # Specify the path to the Geckodriver if it's not in PATH
   geckodriver_path = '/path/to/geckodriver'
   self.driver = webdriver.Firefox(executable_path=geckodriver_path)
   ```

4. (Optional) Install uBlock Origin or other browser extensions as needed.

## Setup

1. Update the `setup` method in the `CookieAutoclicker` class with any necessary configuration for your WebDriver and browser.

## Usage

1. Run the script:
   ```sh
   python cookie_autoclicker.py
   ```

## Notes

- If you do not wish to install uBlock Origin, you can skip this step by commenting out the following lines in the `setup` method:
  ```python
  # self.ublock_path: str = ("/path/to/addon")
  # self.driver.install_addon(self.ublock_path)
  ```

## Disclaimer

This script is intended for educational purposes only. It is not designed to be an efficient or optimal way to play Cookie Clicker. It serves as a basic example of web automation with Selenium. Use at your own risk.

