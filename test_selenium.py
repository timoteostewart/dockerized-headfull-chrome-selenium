import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def main():
    print("Starting Selenium test...")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        print("Initializing webdriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("Navigating to example.com...")
        driver.get("https://www.example.com")
        print("Page title:", driver.title)

        print("Waiting for h1 element...")
        wait = WebDriverWait(driver, 10)
        h1 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        print("H1 text:", h1.text)

        print("Taking screenshot...")
        driver.save_screenshot("screenshot.png")
        print("Screenshot saved as screenshot.png")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
    finally:
        if "driver" in locals():
            driver.quit()
        print("Test completed.")


if __name__ == "__main__":
    main()
