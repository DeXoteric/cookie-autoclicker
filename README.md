# (Work In Progress) Cookie Autoclicker

This project is a Python script that automates the clicking of the "Cookie Clicker" game. It uses the Selenium library to interact with the web page and the pynput library to manage keyboard inputs for pausing and saving the game.

## Features

- Automatically clicks the big cookie.
- Purchases buildings and upgrades.
- Detects and clicks golden cookies.
- Buff management: Automatically casts Force the Hand of God spell when buff (like Frenzy) is active and mana is full.
- Periodically saves the game.
- Keyboard shortcuts for pausing and saving the game.

## Requirements

To run this script, you need to have the following installed:

- Python 3.8 or later
- Firefox browser
- Geckodriver (compatible with your version of Firefox)

The required Python packages are listed in the `requirements.txt` file and can be installed using pip.

## Installation

1. **Clone the repository:**

   Using HTTPS:

   ```bash
   git clone https://github.com/DeXoteric/cookie-autoclicker.git
   cd cookie-autoclicker
   ```

   Using SSH:

   ```bash
   git clone git@github.com:DeXoteric/cookie-autoclicker.git
   cd cookie-autoclicker
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download and place the uBlock0 Firefox extension:**

   Download the uBlock0 Firefox extension from [here](https://github.com/gorhill/uBlock/releases) and place it in your desired directory. Update the `ADDBLOCK_URL` in the script to point to the correct path of the downloaded extension file.

## Usage

1. **Run the script:**

   ```bash
   python cookie_autoclicker.py
   ```

2. **Controls:**

   - **Pause/Resume the game:** Press `Windows Key + Pause`.
   - **Save the game manually:** Press `Windows Key + Scroll Lock`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

This script is intended for educational purposes only. It is not designed to be an efficient or optimal way to play Cookie Clicker. It serves as a basic example of web automation with Selenium. Use at your own risk.
