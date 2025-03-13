import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger()

def test_Naukri_update():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    try:
        logger.info("Opening Naukri website...")
        driver.get('https://www.naukri.com/nlogin/login')
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usernameField')))
        
        logger.info("Entering username...")
        username = os.getenv("NAUKRI_USERNAME")
        username_field.send_keys(username)

        logger.info("Entering password...")
        password_field = driver.find_element(By.ID, 'passwordField')
        password = os.getenv("NAUKRI_PASSWORD")
        password_field.send_keys(password)

        logger.info("Clicking on the Login button...")
        login_button = driver.find_element(By.XPATH, '//button[text()="Login"]')
        login_button.click()

        logger.info("Opening User's profile page...")
        WebDriverWait(driver, 10).until(EC.url_contains('https://www.naukri.com/mnjuser/homepage'))
        driver.get('https://www.naukri.com/mnjuser/profile?id=&orgn=homepage')
        file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        # Get script directory and construct resume path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        resume_path = os.path.join(script_dir, "utils", "Narotam's_Resume_Mar25.pdf")
        file_input.send_keys(resume_path)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Resume uploaded successfully')]")))
        logger.info("Resume updated successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logger.info(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
if __name__ == "__main__":
    test_Naukri_update()
