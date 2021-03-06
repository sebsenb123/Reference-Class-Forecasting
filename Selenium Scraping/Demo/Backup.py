from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import copy
import pandas as pd

#Section 1: Logging into Zephyr and navigating to the list of all deals

print('start')

username = input("Insert username: ")
password = input("Insert password: ")
url = "https://cas.cbs.dk/saml/module.php/core/loginuserpass.php?AuthState=_71e08cea1ce750476fbcf2b3deee8e1adb63e42ece%3Ahttps%3A%2F%2Fcas.cbs.dk%2Fsaml%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Fcas.cbs.dk%252Fsaml%252Fmodule.php%252Fsaml%252Fsp%252Fmetadata.php%252Fsaml2%26RelayState%3Dhttps%253A%252F%252Fcas.cbs.dk%252Fsaml%252Fmodule.php%252Fcasserver%252Fcas.php%252Flogin%253Fservice%253Dhttps%25253A%25252F%25252Flogin.esc-web.lib.cbs.dk%25253A8443%25252Flogin%25253Fqurl%25253Dezp.2aHR0cHM6Ly96ZXBoeXIuYnZkaW5mby5jb20vaG9tZS5zZXJ2P3Byb2R1Y3Q9emVwaHlybmVvJmxvZ2luZnJvbWNvbnRleHQ9aXBhZGRyZXNz%26cookieTime%3D1586890197"

#Open Chrome
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()

#Logg in using info in "username" and "password"
driver.find_element_by_name("username").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_name("wp-submit").send_keys(Keys.ENTER)

#Accepting the conditions
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="image"][@src="SiteCommon2006/en/Blue/accept_condition.gif"]'))).click()

#Waiting for the advanced button to fully generate and click it
time.sleep(2)
driver.find_element_by_id("ContentContainer1_ctl00_Content_VersionSelection1_GoZephyrAdvanced").click()

#Open the dropdown menu by hovering and click the "All deals"-button that appears, then get list
#Really struggled here
element_to_hover_over = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_QuickSearch1_ctl02_SearchSearchMenu_Menu2"]/li[13]')
hover = ActionChains(driver).move_to_element(element_to_hover_over)
hover.perform()
all_deals_button = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_QuickSearch1_ctl02_SearchSearchMenu_Menu2"]/li[13]/ul/li[1]').click()
driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_QuickSearch1_ctl05_GoToList"]').click()

number_of_deals_on_page = 0
table_element = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_FDTBL"]/tbody')
for tr in table_element.find_elements_by_tag_name("tr"):
    number_of_deals_on_page = number_of_deals_on_page + 1
print(number_of_deals_on_page)

number_of_pages = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_ListNavigation_PagesLabel"]').text[-5:]
print(number_of_pages)

page_index_we = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_ListNavigation_CurrentPage"]')
time.sleep(2)
driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_ListNavigation_NextPage"]').click()
time.sleep(10)

number_of_deals_on_page = 0
table_element = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_FDTBL"]/tbody')
for tr in table_element.find_elements_by_tag_name("tr"):
    number_of_deals_on_page = number_of_deals_on_page + 1
print(number_of_deals_on_page)

#Section 2: Define the functions

#the master list will be converted into a DataFrame at a later stage
master_list = []

#while on a deal page, this function changes the index page to the next one
#change this to work on the list page
def change_index_page3(page_index_we, new_page_index):
    page_index_we.clear()
    page_index_we.send_keys(new_page_index)
    page_index_we.send_keys(Keys.ENTER)
    return scraper()

# page_scraper(sub_list, master_list)
##Takes a sub list and a master list. The sublist is cleared and then filled with variables which then is appended to the master list, containing all the deals.
def scraper(master_list):

    list_row = 1

    deal_number_var = "2"
    deal_type_var = "2"
    deal_status_var = "2"
    deal_value_var = "2"
    completed_date_var = "2"
    acquiror_name_var = "2"
    acquiror_country_var = "2"
    target_name_var = "2"
    target_country_var = "2"
    pd_target_operating_revenue_var = "2"
    pd_target_EBITDA_var = "2"
    target_activity_var = "2"



    while list_row < 25:
        driver.execute_script("document.body.style.zoom='50%'")
        sub_list = []

        xpath_deal_number = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_FDTBL"]/tbody/tr[' + deal_number_var + ']/td[1]'
        deal_number = driver.find_element_by_xpath(xpath_deal_number)
        deal_number_var2 = int(deal_number_var) + 1
        deal_number_var = str(copy.copy(deal_number_var2))
        sub_list.append(deal_number.text)

        xpath_deal_type = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + deal_type_var + ']/td[9]'
        deal_type = driver.find_element_by_xpath(xpath_deal_type)
        deal_type_var2 = int(deal_type_var) + 1
        deal_type_var = str(copy.copy(deal_type_var2))
        sub_list.append(deal_type.text)

        xpath_deal_status = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + deal_status_var + ']/td[11]'
        deal_status = driver.find_element_by_xpath(xpath_deal_status)
        deal_status_var2 = int(deal_status_var) + 1
        deal_status_var = str(copy.copy(deal_status_var2))
        sub_list.append(deal_status.text)

        xpath_deal_value = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + deal_value_var + ']/td[13]'
        deal_value = driver.find_element_by_xpath(xpath_deal_value)
        deal_value_var2 = int(deal_value_var) + 1
        deal_value_var = str(copy.copy(deal_value_var2))
        sub_list.append(deal_value.text)

        xpath_completed_date = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr['+completed_date_var+']/td[23]'
        completed_date = driver.find_element_by_xpath(xpath_completed_date)
        completed_date_var2 = int(completed_date_var) + 1
        completed_date_var = str(copy.copy(completed_date_var2))
        sub_list.append(completed_date.text)

        xpath_acquiror_name = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + acquiror_name_var + ']/td[1]'
        acquiror_name = driver.find_element_by_xpath(xpath_acquiror_name)
        acquiror_name_var2 = int(acquiror_name_var) + 1
        acquiror_name_var = str(copy.copy(acquiror_name_var2))
        sub_list.append(acquiror_name.text)

        xpath_acquiror_country = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + acquiror_country_var + ']/td[3]'
        acquiror_country = driver.find_element_by_xpath(xpath_acquiror_country)
        acquiror_country_var2 = int(acquiror_country_var) + 1
        acquiror_country_var = str(copy.copy(acquiror_country_var2))
        sub_list.append(acquiror_country.text)

        xpath_target_name = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + target_name_var + ']/td[5]'
        target_name = driver.find_element_by_xpath(xpath_target_name)
        target_name_var2 = int(target_name_var) + 1
        target_name_var = str(copy.copy(target_name_var2))
        sub_list.append(target_name.text)

        xpath_target_country = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + target_country_var + ']/td[7]'
        target_country = driver.find_element_by_xpath(xpath_target_country)
        target_country_var2 = int(target_country_var) + 1
        target_country_var = str(copy.copy(target_country_var2))
        sub_list.append(target_country.text)

        xpath_pd_target_operating_revenue = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + pd_target_operating_revenue_var + ']/td[17]'
        pd_target_operating_revenue = driver.find_element_by_xpath(xpath_pd_target_operating_revenue)
        pd_target_operating_revenue_var2 = int(pd_target_operating_revenue_var) + 1
        pd_target_operating_revenue_var = str(copy.copy(pd_target_operating_revenue_var2))
        sub_list.append(pd_target_operating_revenue.text)

        xpath_pd_target_EBITDA = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + pd_target_EBITDA_var + ']/td[19]'
        pd_target_EBITDA = driver.find_element_by_xpath(xpath_pd_target_EBITDA)
        pd_target_EBITDA_var2 = int(pd_target_EBITDA_var) + 1
        pd_target_EBITDA_var = str(copy.copy(pd_target_EBITDA_var2))
        sub_list.append(pd_target_EBITDA.text)

        xpath_target_activity = '//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_VDTBL"]/tbody/tr[' + target_activity_var + ']/td[21]'
        target_activity = driver.find_element_by_xpath(xpath_target_activity)
        target_activity_var2 = int(target_activity_var) + 1
        target_activity_var = str(copy.copy(target_activity_var2))
        sub_list.append(target_activity.text)

        # acquired_stake = driver.find_element_by_xpath

        # target_enterprise_value = driver.find_element_by_xpath
        # target_business_desc = driver.find_element_by_xpath
        # target_trade_desc = driver.find_element_by_xpath
        # target_bvd_sector_desc = driver.find_element_by_xpath
        # target_primary_business_desc = driver.find_element_by_xpath

        master_list.append(sub_list)
        list_row = list_row + 1

    page_index_we = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_ListNavigation_CurrentPage"]')
    page_index_value = page_index_we.get_attribute("value")
    page_index_copy = int(copy.copy(page_index_value))
    new_page_index = int(page_index_copy) + 1
    # 82222
    if int(page_index_value) < 2:
        change_index_page3(new_page_index)
    else: finish(master_list)

def finish(master_list):
    print(master_list)
    df_master_list = pd.DataFrame(master_list)
    print(df_master_list)
    print("Done")



time.sleep(30)
