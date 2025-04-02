import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Load Selenium WebDriver
driver = webdriver.Chrome()

# Open the website
driver.get("https://console.cloudinary.com/media-optimizer/c-2832f4fd444e62e50b570381a0d48b/configuration/invalidate-cache")  # Replace with actual URL

# Wait for user confirmation
input("Navigate to the correct page, then press Enter to continue...")

# Load CSV data
with open("output_clean.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    
    chunk = []  # Store 20-row chunks
    
    for row in reader:
        if any(row):  # Ignore blank lines
            chunk.append(row[0])  # Assuming data is in the first column
        
        # Process the chunk when it reaches 20 rows
        if len(chunk) == 20:
            # Locate text field and submit button
            text_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "urls"))
            )
            submit_button = driver.find_element(By.XPATH, "//*[@id=\"standalone\"]/div/div/div[3]/div/div/div/div/div/div[3]/button")
            
            # Paste data into the text field
            text_field.send_keys("\n".join(chunk))  # Join chunk into a single string
            
            # Submit the form
            submit_button.click()
            
            # Wait for the next page to load before continuing (new method below)
            #time.sleep(10)

            # we wait until we see the confirmation box appear then click the x to make it go away and insert the next data
            confirm_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"standalone\"]/div/div/div[3]/div/div/div/div/div[2]/div"))
            )
            confirm_click = driver.find_element(By.XPATH, "//*[@id=\"standalone\"]/div/div/div[3]/div/div/div/div/div[2]/div/button")
            confirm_click.click()

            text_field.send_keys(Keys.CONTROL + "a")  # Select all text
            text_field.send_keys(Keys.DELETE)
            
            # Reset chunk for the next batch
            chunk = []

# Close the browser when done

driver.quit()