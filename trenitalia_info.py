from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime

import time

def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

def Train_canc():
    cancelled = train_status[-11:-1]
    if cancelled == "cancellato":
        return True
    else:
        return False

def Train_not_departed():
    if train_status == "non partito":
        return True
    else:
        return False

def Train_in_time():
    if train_status == "Arrivato in orario":
        return True
    else:
        return False
   
#get the current hour
now = datetime.now()
hour = now.hour

if hour < 8:
    train = "16754"
else:
    train = "17368" 
    
#train = "16660"

print("Getting infomations for the train n.", train)

# Set up Chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  # Optional: Disable GPU acceleration

# Initialize the WebDriver with the headless options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open webpage
    driver.get('http://www.viaggiatreno.it/infomobilitamobile/pages/cercaTreno/cercaTreno.jsp')

    # Wait for the page to load
    time.sleep(3)
    print("Retriving informations from the website")
    # Find the "cerca treno" button and click it, fill the train number and search
    button = driver.find_element(By.ID, 'dati-treno')  
    button.click()
    time.sleep(2)
    textbox = driver.find_element(By.XPATH, '//div[@id="cerca-treno-popup-popup"]//input[@data-type="search"]')
    textbox.send_keys(train)
    time.sleep(1)
    textbox.send_keys(Keys.RETURN)
    time.sleep(2)

    #Retriving the train status
    result_element = driver.find_element(By.XPATH, '//span[@class="statoTreno"]')
    result_text = result_element.text
    train_status = result_text

    # Print the extracted text
    print("The status of the train is:")
    print(train_status)

    #Check for the delay
    delay = train_status[-6:-5]

    if is_integer(delay) is True:
        delay = int(delay)
        if delay > 1:
           print("The train is late!")
    elif Train_canc() is True:
        print("The train has been cancelled!")
    elif Train_not_departed() is True:
        print("The train is not departed yet.")
    elif Train_in_time() is True:
        print("The train is on time.")         
    else:
        print("There is a problem with the train status. Please check manually!")

except WebDriverException as e:
    print(f"WebDriver error occurred: {e}")
    
finally:
    # Close the browser
    driver.quit()

