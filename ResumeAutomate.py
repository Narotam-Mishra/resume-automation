from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
import os
import sys

def update_resume_on_naukri(username, password):
    driver = None  # Initialize driver variable
    try:
        print("Setting up Chrome options...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")  # Unique user data directory

        print("Initializing WebDriver...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        print("Opening Naukri website...")
        driver.get("https://www.naukri.com/")
        time.sleep(random.uniform(2, 5))  # Random delay

        print("Checking for CAPTCHA or blocking...")
        if "CAPTCHA" in driver.page_source or "Access Denied" in driver.page_source:
            print("CAPTCHA or blocking detected. Please solve it manually.")
            time.sleep(60)  # Wait for manual intervention

        print("Waiting for the Login button...")
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Jobseeker Login' and text()='Login']"))
        )
        login_button.click()
        time.sleep(random.uniform(1, 3))

        print("Entering username...")
        username_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"))
        )
        username_field.send_keys(username)
        time.sleep(random.uniform(1, 3))

        print("Entering password...")
        password_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter your password']")
        password_field.send_keys(password)
        time.sleep(random.uniform(1, 3))

        print("Clicking on the Login button...")
        login_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_submit_button.click()
        time.sleep(random.uniform(5, 7))

        print("Clicking on profile icon...")
        profile_icon = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='nI-gNb-bar2']"))
        )
        profile_icon.click()
        time.sleep(random.uniform(2, 4))

        print("Navigating to the Profile section...")
        profile_link = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='View & Update Profile']"))
        )
        profile_link.click()
        time.sleep(random.uniform(3, 5))

        print("Clicking on the 'Update Resume' button...")
        update_resume_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Update resume']"))
        )
        update_resume_button.click()
        time.sleep(random.uniform(2, 4))

        print("Uploading the new resume file...")
        resume_path = os.path.abspath("./utils/Narotam's_Resume_Mar25.pdf")  # Convert to absolute path
        if not os.path.exists(resume_path):  # Check if file exists
            print(f"Resume file not found at: {resume_path}")
            sys.exit(1)  # Exit with a non-zero status code
        resume_file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        resume_file_input.send_keys(resume_path)  # Use absolute path
        time.sleep(random.uniform(5, 7))

        print("Resume updated successfully on Naukri at:", datetime.datetime.now())

    except Exception as e:
        print("An error occurred:", str(e))
        if driver:  # Check if driver was initialized
            driver.save_screenshot("error_screenshot.png")
        sys.exit(1)  # Exit with a non-zero status code to indicate failure

    finally:
        print("Closing the browser...")
        if driver:  # Check if driver was initialized
            driver.quit()

def main():
    # Replace with your actual credentials
    username = os.getenv("NAUKRI_USERNAME")
    password = os.getenv("NAUKRI_PASSWORD")

    print("Starting the resume update process...")
    update_resume_on_naukri(username, password)
    print("Resume update process completed.")

if __name__ == "__main__":
    main()