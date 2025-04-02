from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

# Set up Selenium WebDriver
driver = webdriver.Chrome()

# Open the target website
driver.get("https://console.cloudinary.com/media-optimizer/c-2832f4fd444e62e50b570381a0d48b/configuration/invalidate-cache")  # Replace with the actual website URL

input("Log in manually, then press Enter...")

pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
print("Cookies saved!")
 
driver.quit()


# Load cookies and print them
cookies = pickle.load(open("cookies.pkl", "rb"))
print(cookies)  # Should show a list of cookies
