from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time
import pygetwindow as gw


tenant = "https://xph62488.live.dynatrace.com/"
username = 'lkc-it-automation@ntu.edu.sg'
password = 'TVmonitor123'
backuri = "#dashboard;gtf=l_2_HOURS;gf=all;id=e5e5f314-c733-4b14-8dd2-d087028c9291"
wait_time = 30

chrome_title_1 = 'Window 2'

def run_script(chrome_title):
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--kiosk")

    # Set the path to your chromedriver executable
    chromedriver_path = "C:/Users/OEM/Desktop/autologin folder/chromedriver-win64/chromedriver.exe"  # Update with your actual chromedriver path
    service = Service(chromedriver_path)

    # Initialize the WebDriver with the Service object and options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script(f"document.title = '{chrome_title}';")

    time.sleep(2)

    windows = gw.getWindowsWithTitle(chrome_title)
    if windows:
        chrome_window = windows[0]
        monitor_1 = (0, 0)
        monitor_2 = (21, -1080)
        monitor_3 = (-1920, 0)
        monitor_4 = (-1899, -1080)

        chrome_window.moveTo(*monitor_2)

    # Open the login page
    driver.get(tenant)

    # Print debug message
    print("Opening login page")

    # Wait for the email input field to be present and enter the email
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.NAME, "email")))
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(username)

    # Print debug message
    print("Submitted email")

    # Click the submit button to proceed to password entry
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-id="email_submit"]')))
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[data-id="email_submit"]')
    submit_button.click()

    # Wait for the password field to be present and enter the password
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]')))
    password_field = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
    password_field.send_keys(password)

    # Print debug message
    print("Submitted password")

    # Click the login button
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-id="sign_in"]')))
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[data-id="sign_in"]')
    login_button.click()

    # Wait for the dashboard to appear
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, "mobileapp-user-menu")))

    # Navigate to the dashboard
    driver.get(tenant + backuri)

    # Print debug message
    print("Navigated to dashboard")

    # Keep the browser open for debugging
    input("Press Enter to close the browser...")

    driver.quit()

if __name__ == '__main__':
    run_script(chrome_title_1)
