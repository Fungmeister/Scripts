# Title: Telstra port in (prepaid starter pack life)
# Description: script to open up firefox and automatically fill in forms to port into telstra. manual final submit to confirm details before port in. 
# Author: Brian Fung
# Start Date: 06/08/2016
# Edit Date: 08/08/2015
# Last tested with firefox 35.0. selenium-2.53.6
#
#

import time
from sys import argv 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


## ----------------------- Edit your details -----------------------------

script = argv[0]
sim = argv[1]
service_provider = argv[2] # Amaysim, Optus, Vodafone

mobile = '##########'
title = 'Mr' #  Mr/Miss/Ms
name = 'John'
surname = 'Smith'
D = '1'  #1-31
MMM = 'Jan' # Jan/Feb/Mar etc
YYYY = '1975' #2006 cutoff
email = 'email@gmail.com'
license = '123456789'
license_state = 'VIC'
address = '00 PORT STREET, TELCO LAND' #enter enough of your address for dynamic drop down to single out your address

#can uncomment line 103 to automatically confirm port 

## ------------------------------------------------------------------------

 
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
def get_site(driver):
    driver.get("http://my.telstra.com.au/activate")
    driver.find_element_by_id("porting").click()
    driver.find_element_by_id("submit_activationDetails").click()

def fill_personal_details(driver):
    driver.find_element_by_id("portingsimserial").send_keys(sim)
    driver.find_element_by_id("check_sim_number_btn").click()

    time.sleep(7) # bad but works 
    
    driver.find_element_by_id("currentMsisdn").send_keys(mobile)
    driver.find_element_by_id("msisdnConfirm").send_keys(mobile)
    driver.find_element_by_id("portServiceProvider").send_keys(service_provider)
    driver.find_element_by_id("submit_pkgDetails").click()

    driver.find_element_by_id("agreeWithPortingTerms").click()
    driver.find_element_by_id("acknowledgePortingTerms").click()
    driver.find_element_by_id("submit_portingTerms").click()

    select = Select(driver.find_element_by_id("title"))
    select.select_by_visible_text("Mr")
    
    driver.find_element_by_id("firstName").send_keys(name)
    driver.find_element_by_id("lastName").send_keys(surname)

    select_day = Select(driver.find_element_by_id('dobDay'))
    select_day.select_by_value(D)

    select_month = Select(driver.find_element_by_id('dobMonth'))
    select_month.select_by_visible_text(MMM)

    select_year = Select(driver.find_element_by_id('dobYear'))
    select_year.select_by_value(YYYY)

    driver.find_element_by_id("emailAddress").send_keys(email)
    driver.find_element_by_id("emailAddressConfirm").send_keys(email)
    driver.find_element_by_id("licenseNumber").send_keys(license)

    state = Select(driver.find_element_by_id("stateOfIssue"))
    state.select_by_visible_text(license_state)

    #dyanmic address drop down menu 
    driver.find_element_by_id("address").send_keys(address)
    time.sleep(4)
    element_to_hover_over = driver.find_element_by_css_selector("ul.ui-autocomplete")
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    time.sleep(2)
    driver.find_element_by_id("ui-active-menuitem").click()
   
    driver.find_element_by_id("address-search-button").click()  
    driver.find_element_by_id("submit_yourdetails").click()

def confirm_id(driver):
    driver.find_element_by_id("licenseNumber").send_keys(license)
    driver.find_element_by_id("termsAndConditions").click()
    driver.find_element_by_id("submit_identification").click()
    driver.find_element_by_id("submit_yourdetails").click()

def final_submit(driver):
    driver.find_element_by_id("agreeWithTerm").click() 
    #driver.find_element_by_id("buttonActivate").click() 

    print('Done')

 
if __name__ == "__main__":
    driver = init_driver()
    get_site(driver)
    fill_personal_details(driver)
    confirm_id(driver)
    final_submit(driver)
    time.sleep(10)
    #driver.quit()
