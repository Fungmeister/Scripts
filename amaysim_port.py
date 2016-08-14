# Title: Amaysim port in (prepaid starter pack life)
# Description: script to open up firefox and automatically fill in forms to port into amaysim. manual final submit to confirm details before port in. 
# Author: Brian Fung
# Start Date: 08/08/2016
# Edit Date: 12/08/2016
# Last used stable with firefox 35.0. selenium-2.53.6
# 
#

# ----------------------- Edit your details -----------------------------

mobile = '1234567890'
title = 'Mr' #  Mr/Miss/Ms/Mrs/Miss/Dr
name = 'John'
surname = 'Smith'
DOB = '01/01/1988' #DD/MM/YYYY 
email = 'email@gmail'
daytime_phone = '12345678'  
password = 'password'
license = '12345678'
address = '10 AMAYSIM ST PORT IN' #enter enough of your address for dynamic drop down to single out your address

# ------------------------------------------------------------------------


import time
import argparse
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


script = argv[0] # Script name 
sim = argv[1] # Sim number 
service_provider = argv[2] # Telstra, 'Woolworths Mobile', Vodafone


def init_driver():
	driver = webdriver.Firefox()
	driver.wait = WebDriverWait(driver, 5)
	return driver

def get_site(driver):
	driver.get("https://www.amaysim.com.au/my-account/activate")
	driver.find_element_by_id("my_amaysim2_sim_iccid").send_keys(sim)
	driver.find_element_by_id("new_sim_submit").click()

def fill_mobile(driver):
	driver.find_element_by_id("step-plan").click()
	time.sleep(5)
	
	driver.find_element_by_id("previous_mobile_number_info_number").send_keys(mobile)
	select_provider = Select(driver.find_element_by_id("previous_mobile_number_info_provider"))
	select_provider.select_by_visible_text(service_provider)

	radio = driver.find_element_by_id(
		"previous_mobile_number_info_payment_type_prepaid") 
	driver.execute_script("arguments[0].click();", radio) #simulate click via javascript

	# need xpath for dob box
	driver.find_element_by_xpath(
		"/html/body/div[1]/section[2]/div[2]/div[1]/form/section[3]/div[5]/div[3]/div/input").click()
	driver.find_element_by_xpath(
		"/html/body/div[1]/section[2]/div[2]/div[1]/form/section[3]/div[5]/div[3]/div/input").send_keys(DOB)

	radio_2 = driver.find_element_by_id("previous_mobile_number_info_transfer_auth")
	driver.execute_script("arguments[0].click();", radio_2)
	driver.find_element_by_id("step-number").click()

def fill_personal_details(driver):
	select_title = Select(driver.find_element_by_id("order_transaction_title"))
	select_title.select_by_visible_text("Mr")

	driver.find_element_by_id("order_transaction_first_name").send_keys(name)
	driver.find_element_by_id("order_transaction_last_name").send_keys(surname)
	driver.find_element_by_id("order_transaction_daytime_phone").send_keys(daytime_phone)

	driver.find_element_by_id("order_transaction_email").send_keys(email)
	driver.find_element_by_id("order_transaction_password").send_keys(password)
	driver.find_element_by_id("order_transaction_password_confirmation").send_keys(password)

	driver.find_element_by_id("autocomplete-residential-address").send_keys(address)
	time.sleep(2)
	action = ActionChains(driver)
	action.key_down(Keys.DOWN)
	action.key_up(Keys.ENTER)
	action.perform()
	time.sleep(3)

	driver.find_element_by_id("step-address").click()

def confirm(driver):
	time.sleep(3)
	radio_4 = driver.find_element_by_id("order_transaction_payment_method_2")
	driver.execute_script("arguments[0].click();", radio_4)

	select_title = Select(driver.find_element_by_id("client_identity_dvs_data_source"))
	select_title.select_by_value("vicregodvs") #has problems with select by visible text
	time.sleep(3)

	driver.find_element_by_id("client_identity_number").send_keys(license)
	driver.find_element_by_id("identity_submit").click()
	time.sleep(3)

	radio_5 = driver.find_element_by_id("t_and_c_check")
	driver.execute_script("arguments[0].click();", radio_5)

	#driver.find_element_by_id("order_submit").click()
	print("Done")


if __name__ == "__main__":
	driver = init_driver()
	get_site(driver)
	time.sleep(5)
	fill_mobile(driver)
	time.sleep(5)
	fill_personal_details(driver)
	confirm(driver)
	#driver.quit()
