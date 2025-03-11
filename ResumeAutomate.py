from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import sys
import random
from selenium.common.exceptions import TimeoutException, WebDriverException

def update_resume_on_naukri(username, password):
    driver = None
    try:
        print("Setting up Chrome options...")
        # Setup Chrome options specifically for GitHub Actions
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Don't use webdriver_manager in GitHub Actions
        print("Initializing WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Increase page load timeout
        driver.set_page_load_timeout(60)
        
        print("Opening Naukri website...")
        driver.get("https://www.naukri.com/")
        time.sleep(random.uniform(5, 8))  # Increased wait time
        
        # Take a screenshot to debug
        driver.save_screenshot("naukri_homepage.png")
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        
        print("Checking for CAPTCHA or blocking...")
        if "CAPTCHA" in driver.page_source or "Access Denied" in driver.page_source:
            driver.save_screenshot("blocked_page.png")
            print("CAPTCHA or blocking detected. Exiting as this requires manual intervention.")
            return False
            
        try:
            print("Waiting for the Login button...")
            login_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@title='Jobseeker Login' and text()='Login']"))
            )
            login_button.click()
            time.sleep(random.uniform(3, 5))
        except TimeoutException:
            # Try alternative login button if the first one isn't found
            print("Trying alternative login button...")
            driver.save_screenshot("before_alt_login.png")
            try:
                # Alternative login button selectors
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'login') and contains(text(), 'Login')]"))
                )
                login_button.click()
                time.sleep(random.uniform(3, 5))
            except TimeoutException:
                print("Login button not found. Taking screenshot for debugging...")
                driver.save_screenshot("login_button_not_found.png")
                print(f"Page source: {driver.page_source[:1000]}...")  # Print first 1000 chars of page source
                return False
        
        driver.save_screenshot("after_login_click.png")
        
        print("Entering username...")
        try:
            username_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"))
            )
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))  # Type like a human
            time.sleep(random.uniform(1, 2))
        except TimeoutException:
            driver.save_screenshot("username_field_not_found.png")
            print("Username field not found.")
            return False

        print("Entering password...")
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your password']"))
            )
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))  # Type like a human
            time.sleep(random.uniform(1, 2))
        except TimeoutException:
            driver.save_screenshot("password_field_not_found.png")
            print("Password field not found.")
            return False

        print("Clicking on the Login button...")
        try:
            login_submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_submit_button.click()
            time.sleep(random.uniform(7, 10))  # Increased wait time after login
        except TimeoutException:
            driver.save_screenshot("login_submit_button_not_found.png")
            print("Login submit button not found.")
            return False
            
        driver.save_screenshot("after_login.png")
        
        print("Checking if login was successful...")
        if "Invalid" in driver.page_source or "incorrect" in driver.page_source.lower():
            driver.save_screenshot("login_failed.png")
            print("Login failed. Invalid credentials or CAPTCHA required.")
            return False
        
        print("Clicking on profile icon...")
        try:
            # Try multiple selectors for the profile icon
            selectors = [
                "//div[@class='nI-gNb-bar2']",
                "//div[contains(@class, 'user-profile')]",
                "//a[contains(@href, 'profile')]"
            ]
            
            profile_icon = None
            for selector in selectors:
                try:
                    profile_icon = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
                    
            if profile_icon:
                profile_icon.click()
                time.sleep(random.uniform(3, 5))
            else:
                driver.save_screenshot("profile_icon_not_found.png")
                print("Profile icon not found with any selector.")
                
                # Try direct navigation to profile page
                print("Trying direct navigation to profile page...")
                driver.get("https://www.naukri.com/mnjuser/profile")
                time.sleep(random.uniform(5, 7))
        except Exception as e:
            driver.save_screenshot("profile_icon_error.png")
            print(f"Error clicking profile icon: {str(e)}")
            
            # Try direct navigation as backup
            print("Trying direct navigation to profile page...")
            driver.get("https://www.naukri.com/mnjuser/profile")
            time.sleep(random.uniform(5, 7))
        
        driver.save_screenshot("profile_page.png")
        
        # Try direct navigation to resume upload page as a backup
        try:
            print("Navigating directly to resume upload page...")
            driver.get("https://www.naukri.com/mnjuser/profile?id=&altresid")
            time.sleep(random.uniform(5, 7))
        except:
            pass
            
        print("Clicking on the 'Update Resume' button...")
        try:
            # Try multiple possible selectors for the update resume button
            selectors = [
                "//input[@value='Update resume']",
                "//button[contains(text(), 'Update')]",
                "//a[contains(text(), 'Update Resume')]",
                "//div[contains(@class, 'updateResume')]//button"
            ]
            
            update_button = None
            for selector in selectors:
                try:
                    update_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
                    
            if update_button:
                update_button.click()
                time.sleep(random.uniform(3, 5))
            else:
                driver.save_screenshot("update_button_not_found.png")
                print("Update resume button not found with any selector.")
                return False
        except Exception as e:
            driver.save_screenshot("update_button_error.png")
            print(f"Error clicking update button: {str(e)}")
            return False
            
        driver.save_screenshot("before_upload.png")
        
        print("Uploading the new resume file...")
        try:
            # Get absolute path and verify file exists
            resume_path = os.path.abspath("./utils/Narotam's_Resume_Mar25.pdf")
            print(f"Resume path: {resume_path}")
            
            if not os.path.exists(resume_path):
                print(f"Resume file not found at: {resume_path}")
                # List files in directory to debug
                utils_dir = os.path.dirname(resume_path)
                print(f"Files in {utils_dir}: {os.listdir(utils_dir) if os.path.exists(utils_dir) else 'directory not found'}")
                return False
                
            # Find file input element
            try:
                # Wait for the file input to be present in the DOM
                resume_file_input = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                # Make sure it's interactable
                driver.execute_script("arguments[0].style.display = 'block';", resume_file_input)
                time.sleep(1)
                resume_file_input.send_keys(resume_path)
                time.sleep(random.uniform(7, 10))  # Wait longer for upload
            except TimeoutException:
                driver.save_screenshot("file_input_not_found.png")
                print("File input element not found.")
                return False
        except Exception as e:
            driver.save_screenshot("upload_error.png")
            print(f"Error during file upload: {str(e)}")
            return False
            
        driver.save_screenshot("after_upload.png")
        
        # Wait for the upload confirmation
        try:
            success_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'successfully') or contains(text(), 'Success')]"))
            )
            print("Resume updated successfully on Naukri at:", datetime.datetime.now())
            driver.save_screenshot("upload_success.png")
            return True
        except TimeoutException:
            driver.save_screenshot("upload_confirmation_timeout.png")
            print("Upload confirmation not found. Update may have failed.")
            return False

    except Exception as e:
        print("An error occurred:", str(e))
        if driver:
            driver.save_screenshot("error_screenshot.png")
        return False

    finally:
        print("Closing the browser...")
        if driver:
            driver.quit()
            
def main():
    # Get credentials from environment variables
    username = os.getenv("NAUKRI_USERNAME")
    password = os.getenv("NAUKRI_PASSWORD")
    
    if not username or not password:
        print("Error: NAUKRI_USERNAME or NAUKRI_PASSWORD environment variables not set.")
        sys.exit(1)
        
    print("Starting the resume update process...")
    success = update_resume_on_naukri(username, password)
    
    if success:
        print("Resume update process completed successfully.")
        sys.exit(0)  # Exit with success code
    else:
        print("Resume update process failed.")
        sys.exit(1)  # Exit with failure code

if __name__ == "__main__":
    main()