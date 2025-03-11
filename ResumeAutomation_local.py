from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from webdriver_manager.chrome import ChromeDriverManager

# Function to log in to Naukri and update the resume
def update_resume_on_naukri(username, password):
    try:

        # Launch Chrome browser
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()

        # Open Naukri website
        driver.get("https://www.naukri.com/")
        time.sleep(5)  # Wait for the page to load

        # Click on the Login button
        login_button = driver.find_element(By.XPATH, "//a[@title='Jobseeker Login' and text()='Login']")
        login_button.click()
        time.sleep(3)

        # Enter username and password
        username_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")
        username_field.send_keys(username)
        time.sleep(1)

        password_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter your password']")
        password_field.send_keys(password)
        time.sleep(1)

        # Click on the Login button
        login_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_submit_button.click()
        time.sleep(5)  # Wait for login to complete

        # click on profile icon
        profile_icon = driver.find_element(By.XPATH, "//div[@class='nI-gNb-drawer__bars']/div[@class='nI-gNb-bar2']")
        profile_icon.click()
        time.sleep(3)

        # Navigate to the Profile section
        profile_link = driver.find_element(By.XPATH, "//a[text()='View & Update Profile']")
        profile_link.click()
        time.sleep(5)

        # Click on the "Update Resume" button
        update_resume_button = driver.find_element(By.XPATH, "//input[@value='Update resume']")
        update_resume_button.click()
        time.sleep(3)

        # Upload the new resume file
        resume_file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        resume_file_input.send_keys("C:/Users/Narotam/Desktop/Narotam's_Resume_Mar25.pdf")  # Update this path
        time.sleep(5)  # Wait for the file to upload

        print("Resume updated successfully on Naukri at:", datetime.datetime.now())

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        # Close the browser
        driver.quit()

# Main function to run the script
def main():
    # Naukri credentials (replace with your actual credentials)
    # username = os.getenv("NAUKRI_USERNAME")
    # password = os.getenv("NAUKRI_PASSWORD")

    username = ""
    password = ""

    # Call the function to update the resume
    update_resume_on_naukri(username, password)

if __name__ == "__main__":
    main()