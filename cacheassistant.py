#Cache Clearing Assistant by Dave Nissly
#1/28/2025
#v1.1
import csv
import string
import time

def preprocess():
    #data holds the netuite resources
    data = []
    #data2 holds the cloudinary resources
    data2 = []
    #numRows is used to keep track of when to skip a line for cloudinary
    numRows = 0
    #line holds temporary row data
    line = []

    #open the file as csvfile
    with open("data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) #skip over the column labels
        #iterate through and generate netsuite resources for each product
        #count of resources is equal to the number of images for each product
        for row in reader:
            if row[0] == "Total":
                break 
            iterations = int(row[2]) #count of images to update 
            for i in range(iterations):
                s = "/assets/images/products/" + str(row[1]) + '-' + str(i+1) + ".jpg"
                line = []
                line.append(s)
                data.append(line)
            line = []
            for i in range(iterations):
                if i <= 1:
                    #first two images need both big and small cloudinary links
                    cloudinaryLink1 = "https://media.rallyhouse.com/products/" + row[1] + "-" + str(i+1) + ".jpg?tx=f_auto,w_216,h_308"
                    cloudinaryLink2 = "https://media.rallyhouse.com/homepage/" + row[1] + "-" + str(i+1) + ".jpg?tx=f_auto,c_fit,w_730,h_730"
                    line = []
                    line.append(cloudinaryLink1)
                    data2.append(line)
                    numRows +=1
                    if numRows == 20 :
                        blank = []
                        data2.append(blank)
                        numRows = 0
                    line = []
                    line.append(cloudinaryLink2)
                    data2.append(line)
                    numRows+= 1
                    if numRows == 20 :
                        blank = []
                        data2.append(blank)
                        numRows = 0
                    line = []
                else:
                    #third image and beyond only need the big cloudinary links
                    cloudinaryLink1 = "https://media.rallyhouse.com/homepage/" + row[1] + "-" + str(i+1) + ".jpg?tx=f_auto,c_fit,w_730,h_730"
                    line.append(cloudinaryLink1)
                    data2.append(line)
                    numRows += 1
                    line = []
                    if numRows == 20 :
                        blank = []
                        data2.append(blank)
                        numRows = 0
#write cache invalidation data to csv
    with open("output_ns.csv", "w", newline="") as csvfile:
        writer1 = csv.writer(csvfile)
        for idx, row in enumerate(data, 1):
            writer1.writerow(row)
            if idx % 49 == 0:
                writer1.writerow([])  # Write a blank line every 49 rows
#write the data into the used output file        
    with open("output_clean.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data2)
    return()

def clearcache():
    input("Enter the netsuite assets from output_ns into the netsuite cache invalidator, then press Enter to continue...")

    with open("login.txt", "r") as file:
        line = file.readline()
        user = [line.strip()]
        line = file.readline()
        pwd = [line]

    input("Ensure you have done the netsuite step first, pressing Enter again will automatically start the cloudinary cache clearing...")

    #start the cloudinary cache clearing part
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys

    # Load Selenium WebDriver
    driver = webdriver.Chrome()

    # Open the website and navigate to the correct page after logging in
    driver.get("https://console.cloudinary.com/media-optimizer/c-2832f4fd444e62e50b570381a0d48b/configuration/invalidate-cache")  # Replace with actual URL
    time.sleep(5)  # Wait for the page to load
    user_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"user_session_email\"]"))
                )

    pwd_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"user_session_password\"]"))
                )

    login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"sign-in\"]"))
                )

    user_field.send_keys("\n".join(user))
    pwd_field.send_keys("\n".join(pwd))
    login_button.click()

    optimizer_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"media_optimizer\"]/div/img[2]"))
                )

    optimizer_button.click()

    cache_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"standalone\"]/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/nav/ul/li[3]/div/div/a"))
                )

    cache_button.click()

    # Wait for user confirmation
    #input("Navigate to the correct page, then press Enter to continue...")

    # Load CSV data
    with open("output_clean.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        
        chunk = []  # Store 20-row chunks
        
        for row in reader:
            if any(row):  # Ignore blank lines
                print(f"Clearing: {row[0]}")
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
        if chunk:
            text_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "urls"))
            )
            submit_button = driver.find_element(By.XPATH, "//*[@id=\"standalone\"]/div/div/div[3]/div/div/div/div/div/div[3]/button")
            
            text_field.send_keys("\n".join(chunk))
            submit_button.click()

            confirm_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"standalone\"]/div/div/div[3]/div/div/div/div/div[2]/div"))
            )
            confirm_click = driver.find_element(By.XPATH, "//*[@id=\"standalone\"]/div/div/div[3]/div/div/div/div/div[2]/div/button")
            confirm_click.click()

    # Close the browser when done

    driver.quit()
    return()

def main():
    preprocess()
    clearcache()
    return()

if __name__ == "__main__":
    main()
    print("Cache clearing complete!")
#EOF