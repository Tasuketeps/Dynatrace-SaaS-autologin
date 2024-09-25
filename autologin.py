from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import urllib.request
import time
import pygetwindow as gw


tenant = "https://xph62488.live.dynatrace.com/"
username = 'lkc-it-automation@ntu.edu.sg'
password = 'TVmonitor123'
backuri = "#dashboard;id=86d7ee1d-50eb-4945-8d7c-f5b238830c29;gf=all;gtf=-2h"
wait_time = 30

chrome_title_1 = 'Window 1'

#initialise chrome driver
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--no-sandbox")   # Run without sandbox

# Set the path to your chromedriver executable
chromedriver_path = "C:/Users/CS-EDISON.TAY/Desktop/scripts/chromedriver/chromedriver.exe"  # Update with your actual chromedriver path
service = Service(chromedriver_path)

# Initialize the WebDriver with the Service object and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Test for internet connection first before starting
def wait_for_internet(timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen('https://google.com', timeout=5)
            print("Internet connection available.")
            return True
        except:
            time.sleep(5)
    raise Exception("Internet connection failed to initialize.")
    return False

def run_script(chrome_title):
    # Open the login page
    driver.get(tenant)

    # Print debug message
    print("Opening login page")

    # Wait for the email input field to be present and enter the email
    try:
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.NAME, "email")))
        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys(username)
    except TimeoutException:
        print('Timed out waiting for email field to load')
        driver.quit()
        run_script(chrome_title_1)
        print('Restarting the script again...')

    # Print debug message
    print("Submitted email")

    # Click the submit button to proceed to password entry
    try:
        WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-id="email_submit"]')))
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[data-id="email_submit"]')
        submit_button.click()
    except TimeoutException:
        print('Email submit button not loaded')
        driver.quit()
        run_script(chrome_title_1)
        print('Restarting the script again...')

    # Wait for the password field to be present and enter the password
    try:
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]')))
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
        password_field.send_keys(password)
    except TimeoutException:
        print('Password field failed to load')
        driver.quit()
        run_script(chrome_title_1)
        print('Restarting the script again...')


    # Print debug message
    print("Submitted password")

    # Click the login button
    try:
        WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-id="sign_in"]')))
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[data-id="sign_in"]')
        login_button.click()
    except TimeoutException:
        print('Login button failed to load')
        driver.quit()
        run_script(chrome_title_1)
        print('Restarting the script again...')

    try:
        # Wait for the dashboard to appear
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, "mobileapp-user-menu")))

        # Navigate to the dashboard
        driver.get(tenant + backuri)

        # Print debug message
        print("Successfully logged in to dashboard")
        driver.execute_script(f"document.title = '{chrome_title}';")
        time.sleep(5)
        print(gw.getAllTitles())

        windows = gw.getWindowsWithTitle(f'{chrome_title} - Google Chrome')
        if not windows:
            raise Exception(f"No windows found with title '{chrome_title}'")
        
        if windows:
            print('title change success')
            chrome_window = windows[0]
            monitor_1 = (0, 0)
            monitor_2 = (21, -1080)
            monitor_3 = (-1920, 0)
            monitor_4 = (-1899, -1080)

            chrome_window.moveTo(*monitor_4)

    except TimeoutException:
        print('Dashboard timed out')
        driver.quit()
        run_script(chrome_title_1)
        print('Restarting the script again...')

#run the functions
internet = False
tries = 0
max_retries = 5

while not internet and tries < max_retries:
    try:
        print('Checking for internet connection...')
        internet = wait_for_internet()  # Try to check if internet is available
        if not internet:
            raise Exception("No internet connection")
    except Exception as e:
        print('Not connected to the internet, trying again...')
        tries += 1
        print(f"{tries}/{max_retries} retries so far...")
        time.sleep(5)  # Wait 5 seconds before trying again
    else:
        print("Connected to the internet")
        run_script(chrome_title_1)  # Call your script here

input('Press enter to close the display')
driver.quit()