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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def update_resume_on_naukri(username, password):
    driver = None
    try:
        print("Setting up Chrome options...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        
        print("Initializing WebDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.set_page_load_timeout(60)
        
        print("Opening Naukri website...")
        driver.get("https://www.naukri.com/")
        time.sleep(random.uniform(5, 8))
        
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
            print("Trying alternative login button...")
            driver.save_screenshot("before_alt_login.png")
            try:
                login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'login') or contains(text(), 'Login')]"))
                )
                login_button.click()
                time.sleep(random.uniform(3, 5))
            except TimeoutException:
                try:
                    # Third attempt - try to find any login-related element
                    print("Trying third login option...")
                    elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'login') or contains(text(), 'Login')]")
                    if elements:
                        elements[0].click()
                        time.sleep(random.uniform(3, 5))
                    else:
                        print("No login element found, trying direct URL...")
                        driver.get("https://www.naukri.com/nlogin/login")
                        time.sleep(random.uniform(5, 7))
                except:
                    print("Login button not found. Trying direct login URL...")
                    driver.get("https://www.naukri.com/nlogin/login")
                    time.sleep(random.uniform(5, 7))
        
        driver.save_screenshot("after_login_click.png")
        
        print("Entering username...")
        try:
            username_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"))
            )
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(1, 2))
        except TimeoutException:
            try:
                # Try alternative username field
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Email') or contains(@id, 'email') or contains(@name, 'email')]"))
                )
                username_field.clear()
                for char in username:
                    username_field.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                time.sleep(random.uniform(1, 2))
            except:
                driver.save_screenshot("username_field_not_found.png")
                print("Username field not found.")
                print(f"Page source: {driver.page_source[:1000]}...")
                return False

        print("Entering password...")
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your password']"))
            )
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(random.uniform(1, 2))
        except TimeoutException:
            try:
                # Try alternative password field
                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
                )
                password_field.clear()
                for char in password:
                    password_field.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                time.sleep(random.uniform(1, 2))
            except:
                driver.save_screenshot("password_field_not_found.png")
                print("Password field not found.")
                return False

        print("Clicking on the Login button...")
        try:
            login_submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_submit_button.click()
            time.sleep(random.uniform(7, 10))
        except TimeoutException:
            try:
                # Try any button that might be the login button
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    if "login" in button.text.lower() or "sign in" in button.text.lower():
                        button.click()
                        time.sleep(random.uniform(7, 10))
                        break
            except:
                driver.save_screenshot("login_submit_button_not_found.png")
                print("Login submit button not found.")
                return False
            
        driver.save_screenshot("after_login.png")
        
        print("Checking if login was successful...")
        if "Invalid" in driver.page_source or "incorrect" in driver.page_source.lower():
            driver.save_screenshot("login_failed.png")
            print("Login failed. Invalid credentials or CAPTCHA required.")
            return False
            
        # Direct navigation to profile update page - most reliable method
        print("Navigating directly to resume update page...")
        driver.get("https://www.naukri.com/mnjuser/profile?id=&altresid")
        time.sleep(5)
        driver.save_screenshot("profile_page_direct.png")
        
        # Print the current URLs we've visited to debug
        print(f"Current URL after direct navigation: {driver.current_url}")
        
        # Check if we need to go to a different page for resume upload
        if "attachCV" not in driver.current_url:
            print("Navigating to specific CV upload page...")
            try:
                driver.get("https://www.naukri.com/mnjuser/attachCV")
                time.sleep(5)
            except:
                print("Failed to navigate to attachCV page. Trying alternative.")
                try:
                    driver.get("https://www.naukri.com/mnjuser/profile?id=&altresid&file=attach")
                    time.sleep(5)
                except:
                    pass
        
        driver.save_screenshot("before_upload_attempt.png")
        print(f"Current URL before upload attempt: {driver.current_url}")
        
        # Extensive approach to find file input element
        print("Looking for file input element...")
        file_input_found = False
        
        # Try multiple strategies to find and interact with file input
        try:
            # Strategy 1: Direct XPath
            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
            print(f"Found {len(file_inputs)} file input elements")
            
            if file_inputs:
                file_input_found = True
                for idx, file_input in enumerate(file_inputs):
                    try:
                        print(f"Trying file input #{idx+1}")
                        driver.execute_script("arguments[0].style.display = 'block';", file_input)
                        time.sleep(1)
                        
                        resume_path = os.path.abspath("./utils/Narotam's_Resume_Mar25.pdf")
                        print(f"Resume path: {resume_path}")
                        
                        if not os.path.exists(resume_path):
                            print(f"Resume file not found at: {resume_path}")
                            utils_dir = os.path.dirname(resume_path)
                            print(f"Files in {utils_dir}: {os.listdir(utils_dir) if os.path.exists(utils_dir) else 'directory not found'}")
                            return False
                            
                        file_input.send_keys(resume_path)
                        time.sleep(10)  # Wait longer for upload
                        driver.save_screenshot(f"after_upload_attempt_{idx}.png")
                        
                        # Check for success indicators
                        if "success" in driver.page_source.lower() or "uploaded" in driver.page_source.lower():
                            print("Resume upload successful!")
                            driver.save_screenshot("upload_success_confirmed.png")
                            return True
                    except Exception as e:
                        print(f"Error with file input #{idx+1}: {str(e)}")
                        continue
            
            # Strategy 2: Look for any update/upload button and click it first
            if not file_input_found:
                print("Looking for update/upload buttons...")
                update_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Update') or contains(text(), 'Upload')]")
                
                for idx, button in enumerate(update_buttons):
                    try:
                        print(f"Clicking update/upload button #{idx+1}")
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(1)
                        button.click()
                        time.sleep(3)
                        driver.save_screenshot(f"after_update_button_click_{idx}.png")
                        
                        # Now look for file input again
                        file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
                        if file_inputs:
                            for file_idx, file_input in enumerate(file_inputs):
                                try:
                                    driver.execute_script("arguments[0].style.display = 'block';", file_input)
                                    time.sleep(1)
                                    
                                    resume_path = os.path.abspath("./utils/Narotam's_Resume_Mar25.pdf")
                                    file_input.send_keys(resume_path)
                                    time.sleep(10)
                                    driver.save_screenshot(f"after_upload_attempt_btn_{idx}_file_{file_idx}.png")
                                    
                                    if "success" in driver.page_source.lower() or "uploaded" in driver.page_source.lower():
                                        print("Resume upload successful via button click approach!")
                                        return True
                                except Exception as e:
                                    print(f"Error with file input after button #{idx+1}: {str(e)}")
                                    continue
                    except Exception as e:
                        print(f"Error clicking button #{idx+1}: {str(e)}")
                        continue
            
            # Strategy 3: Try to use JavaScript to trigger file upload dialog
            print("Trying JavaScript approach to file upload...")
            try:
                resume_path = os.path.abspath("./utils/Narotam's_Resume_Mar25.pdf")
                
                # Create a temporary file input element
                driver.execute_script("""
                    var input = document.createElement('input');
                    input.type = 'file';
                    input.id = 'temp-file-input';
                    input.style.display = 'block';
                    input.style.position = 'fixed';
                    input.style.top = '0';
                    input.style.left = '0';
                    document.body.appendChild(input);
                """)
                time.sleep(1)
                
                # Try to use the temporary input
                temp_input = driver.find_element(By.ID, "temp-file-input")
                temp_input.send_keys(resume_path)
                time.sleep(3)
                driver.save_screenshot("after_js_file_upload.png")
                
                # Try to submit the form if any exists
                forms = driver.find_elements(By.TAG_NAME, "form")
                if forms:
                    for form in forms:
                        try:
                            driver.execute_script("arguments[0].submit();", form)
                            time.sleep(5)
                            driver.save_screenshot("after_form_submit.png")
                        except:
                            pass
            except Exception as e:
                print(f"JavaScript approach failed: {str(e)}")
            
            # At this point, we've tried multiple strategies
            print("All file upload strategies attempted, checking page content for success indicators...")
            driver.save_screenshot("final_state.png")
            
            # Final check for success indicators in the page
            page_text = driver.page_source.lower()
            if "success" in page_text or "uploaded" in page_text or "updated" in page_text:
                print("Page indicates successful upload!")
                return True
            else:
                print("No success indicators found in page.")
                print("HTML snippet around potential indicators:")
                # Print a snippet of HTML that might contain status information
                try:
                    status_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'status') or contains(@class, 'message') or contains(@class, 'notification')]")
                    for idx, elem in enumerate(status_elements):
                        print(f"Status element #{idx+1}: {elem.text}")
                        print(f"HTML: {elem.get_attribute('outerHTML')}")
                except:
                    pass
                return False
            
        except Exception as e:
            driver.save_screenshot("file_upload_error.png")
            print(f"Error during file upload attempts: {str(e)}")
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