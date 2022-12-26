#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import telegram_send

import time
import chime
import os


driverService=Service('/usr/lib/chromium-browser/chromedriver')
waiting_time = 15


def chime_n(n):
    i = 0
    while i < n:
        chime.success()
        print("chime")
        time.sleep(1)
        i+=1


# options = Options()
# options.headless = True
# options.add_argument('--headless')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=driverService, options=options)

# Selenium Stealth settings
stealth(driver,
      languages=["en-US", "en"],
      vendor="Google Inc.",
      platform="Win32",
      webgl_vendor="Intel Inc.",
      renderer="Intel Iris OpenGL Engine",
      fix_hairline=True,
)


def load_page():
    try:
        print ("Page loading ...")

        # homepage
        url = "https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en"
        driver.get(url)

        # Disable all alerts in page:
        driver.execute_script("window.alert = function() {};")
        time.sleep(1)

        book_appointment = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Book Appointment')]")))
        book_appointment.click()
        time.sleep(1)

        
        agree = WebDriverWait(driver, waiting_time).until(
            EC.element_to_be_clickable((By.ID, "xi-cb-1")))
        agree.click()
        time.sleep(1)

        next = WebDriverWait(driver, waiting_time).until(
            EC.element_to_be_clickable((By.ID, "applicationForm:managedForm:proceed")))
        next.click()

        time.sleep(10)

    except Exception as e:
        print ("load_page failed")




def service_selection():
    # Just to confirm page load by checking the citizenship element
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "xi-sel-400")))

    print("Selecting Citizenship")
    citizenship = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.ID, "xi-sel-400")))
    citizenship_select = Select(citizenship)
    citizenship_select.select_by_value('461')
    time.sleep(2)

    print("Selecting Number of People")
    num_people = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.ID, "xi-sel-422")))
    num_people_select = Select(num_people)
    num_people_select.select_by_value('1')
    time.sleep(2)

    print("Selecting Berlin")
    in_berlin = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.ID, "xi-sel-427")))
    in_berlin_select = Select(in_berlin)
    in_berlin_select.select_by_value('1')
    time.sleep(2)


    print("Selecting Family Citizenship")
    family_citizenship = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.ID, "xi-sel-428")))
    family_citizenship_select = Select(family_citizenship)
    family_citizenship_select.select_by_value('461-0')
    time.sleep(2)


	# #  Apply for a residence permit
    # print("Selecting Residence Title")
    # residence_title = WebDriverWait(driver, waiting_time).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, "kachel-461-0-1")))
    # residence_title.click()
    # time.sleep(2)


    # Extend a residence title
    print("Selecting Extend a residence title")
    residence_title = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "kachel-461-0-2")))
        # EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ozg-kachel.kachel-461-0-2.level1")))
    residence_title.click()
    time.sleep(2)


    # Education Reasons
    print("Selecting Education Reasons")
    education_reasons = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "accordion-461-0-2-3")))
    education_reasons.click()
    time.sleep(2)


    # Family Reasons
    # print("Selecting Family Reasons")
    # family_reasons = WebDriverWait(driver, waiting_time).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, "accordion-461-0-1-4")))
    # family_reasons.click()
    # time.sleep(2)


    # Residence permit for the purpose of studying (sect. 16b)
    print("Selecting Residence permit for the purpose of studying (sect. 16b)")
    residence_permit = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.ID, "SERVICEWAHL_EN461-0-2-3-305244")))
    residence_permit.click()
    time.sleep(2)


    print("Selecting Next")
    service_selection_next = WebDriverWait(driver, waiting_time).until(
        EC.element_to_be_clickable((By.ID, "applicationForm:managedForm:proceed")))
    service_selection_next.click()
    time.sleep(5)


def find_available_date(html, acceptable_dates):
    soup = BeautifulSoup(html, 'html.parser')
    dates = []
    #   table = soup.find('table')
    #   rows = table.find_all('tr')
    rows = soup.find_all('tr')                
    for row in rows:
        cells = row.find_all('td')
        for cell in cells:
                if cell.find(href=True): 
                    if cell.string in acceptable_dates:
                        dates.append(cell.string)
                        # print ("Appointment found on: {}\n". format(cell.string))
                
    return dates


def find_available_month(acceptable_months, acceptable_dates):
    appointments = ""
    month = ""
    try:
        # ui-datepicker-month
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-datepicker-month")))
        month = element.get_attribute("innerHTML")
    except:
        print ("ui-datepicker-month failed\n")
        return ""


    if month not in acceptable_months:
        print ("Not in the months\n")
        return ""

    print('\033[1;32;40m --------------- Appointment found ------------------ \033[0;37;40m')
    print('\033[1;32;40m Latest appointments found in month: {0} \033[0;37;40m'.format(month))

    try:
        # ui-datepicker-calendar
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "ui-datepicker-calendar")))
        month_calender = element.get_attribute("innerHTML")

        dates = find_available_date(month_calender, acceptable_dates)
        print ("Available dates: {}". format(dates))
        if len(dates) != 0:
            appointments='Appointment found in {} - {}'.format(month, dates)
            return appointments

    except Exception as e:
        print ("ui-datepicker-calendar failed: {}\n".format(e))
        return ""

    return ""


load_page()

num_next_clicks = 0

while True:
    num_next_clicks+=1
    print("------------- [%d] RETRY -----------------"% num_next_clicks)

    try:
        if (num_next_clicks % 25) == 0:
            load_page()

        service_selection()

        try:
            print("Checking appointment(s)")
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "errorMessage")))
            errorMessage = element.get_attribute("innerHTML")

            print('\033[1;31;40mNo appointments found: {0}\033[0;37;40m'.format(errorMessage))

            # This will send a spurious messages, mean useless notifications every few seconds, do this only for testing...
            # Or send to different (filtered) channel on telegram is just to keep eye on the script that it is running 
            # telegram_send.send(messages=["No appointments found"])

        except:
            acceptable_dates = [
                '1', '4','5','6','7','8','9','10',
                 '11','12', '13','14','15','16','17','18','19','20'
                 '21','22','23','24','25','26','27','28','29','30',
                ]

            acceptable_months = ['July', 'August' ]

            msg=find_available_month(acceptable_months, acceptable_dates )
            if msg:
                # Open new TAB
                driver.execute_script("window.open(''),'_blank'")
                driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])

                # Console message
                print('\033[1;32;40m appointments found: {0} \033[0;37;40m'.format(msg))

                # Linux notification
                os.system('notify-send "LEA Appointment" "LEA Appointment"')

                # Send telegram message
                telegram_send.send(messages=[msg])

                chime_n(2)
            
                time.sleep(300)  # 5 mins
                load_page()

            else :
                print('\033[1;31;40mLatest appointments found in months \033[0;37;40m')

    except Exception as e:
        # print ("service_selection() failed: {0}".format(e))
        print ("service_selection() failed")
        load_page()
    
    try:
        print("Selecting Service")
        service = WebDriverWait(driver, waiting_time).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "antcl_first-step")))
        service.click()
    except Exception as e:
        # print ("service re-selection() failed: {0}".format(e))
        print ("service re-selection() failed")
        load_page()

    time.sleep(15)

