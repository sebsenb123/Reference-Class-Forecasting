from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import copy

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

#Enter Aramco deal
driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_ListCtrl1_LB1_FDTBL"]/tbody/tr[2]/td[9]/a').click()



#Section 2: Define the functions

#while on a deal page, this function changes the index page to the next one

def change_index_page3(page_index_we):
    while True:
        time.sleep(2)
        page_index_v = page_index_we.get_attribute("value")
        page_index_copy = int(copy.copy(page_index_v))
        page_index_copy_b = int(page_index_copy) + 1
        driver.find_element_by_xpath('//*[@id="SeqNrlbl"]').clear()
        driver.find_element_by_xpath('//*[@id="SeqNrlbl"]').send_keys(page_index_copy_b)
        driver.find_element_by_xpath('//*[@id="SeqNrlbl"]').send_keys(Keys.ENTER)
        return starter1()

#checks if the deal status equals "Completed". If yes: run the scraper. If not: run the change_index_page
def navigator_bot2(page_index):
    deal_status = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[3]')
    if deal_status.text != "Completed":
        change_index_page3(page_index_we)
    else:
        scraper()

def starter1():
    while current_page_index < 2054977:
        navigator_bot2(page_index)


# page_scraper(sub_list, master_list)
##Takes a sub list and a master list. The sublist is cleared and then filled with variables which then is appended to the master list, containing all the deals.
def scraper(master_list):
    sub_list = []

    deal_type = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[3]')
    deal_status = driver.find_element_by_xpathdriver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[3]')
    deal_value = driver.find_element_by_xpath.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td[3]')
    completed_date = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_STRUCTURESDATES_MainStructuresDates"]/tbody/tr/td[2]/table/tbody/tr[4]/td[3]')

    acquiror_name = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[3]/a')
    acquiror_country = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[4]')
    # acquired_stake = driver.find_element_by_xpath

    target_name = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[4]/a')
    target_country = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[5]')
    # target_enterprise_value = driver.find_element_by_xpath

    # SCROLL

    pd_target_operating_revenue = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_PREDEALFINANCIALS_SSCtr"]/tbody/tr[8]/td[2]/span')
    pd_target_EBITDA = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_PREDEALFINANCIALS_SSCtr"]/tbody/tr[9]/td[2]/span')
    # target_business_desc = driver.find_element_by_xpath
    # target_trade_desc = driver.find_element_by_xpath

    target_activity = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[6]/table/tbody/tr[1]')
    target_bvd_sector_desc = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[7]')
    # target_primary_business_desc = driver.find_element_by_xpath

    sub_list.append(deal_type.text)
    sub_list.append(deal_status.text)
    sub_list.append(deal_value.text)

    sub_list.append(completed_date.text)
    sub_list.append(acquiror_name.text)
    sub_list.append(acquiror_country.text)

    sub_list.append(target_name.text)
    sub_list.append(target_country.text)
    sub_list.append(pd_target_operating_revenue.text)
    sub_list.append(pd_target_EBITDA.text)
    sub_list.append(target_activity.text)
    sub_list.append(target_bvd_sector_desc.text)


current_page_index_we = driver.find_element_by_xpath('//*[@id="SeqNrlbl"]')
current_page_index = current_page_index_we.get_attribute("value")
master_list = []

#testing below here:

current_page_index_we = driver.find_element_by_xpath('//*[@id="SeqNrlbl"]')
current_page_index = current_page_index_we.get_attribute("value")

time.sleep(2)
page_index_copy = int(copy.copy(current_page_index))
page_index_copy_b = page_index_copy + 3
driver.find_element_by_xpath('//*[@id="SeqNrlbl"]').clear()
driver.find_element_by_xpath('//*[@id="SeqNrlbl"]').send_keys(page_index_copy_b)
driver.find_element_by_xpath('//*[@id="SeqNrlbl"]').send_keys(Keys.ENTER)

time.sleep(2)

sub_list = []

deal_type = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[3]')
deal_status = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[3]')
deal_value = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td[3]')
completed_date = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_STRUCTURESDATES_MainStructuresDates"]/tbody/tr/td[2]/table/tbody/tr[4]/td[3]')

acquiror_name = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_PREDEALFINANCIALS_SSCtr"]/tbody/tr[2]/td')
acquiror_country = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[4]')
    # acquired_stake = driver.find_element_by_xpath

#target_name = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[3]/a')
target_country = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[4]')
    # target_enterprise_value = driver.find_element_by_xpath

driver.execute_script("document.body.style.zoom='33%'")

pd_target_operating_revenue = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_PREDEALFINANCIALS_SSCtr"]/tbody/tr[5]/td[2]')

pd_target_EBITDA = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_PREDEALFINANCIALS_SSCtr"]/tbody/tr[6]/td[2]')
    # target_business_desc = driver.find_element_by_xpath
    # target_trade_desc = driver.find_element_by_xpath

target_activity = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[6]/table/tbody/tr[1]')
target_bvd_sector_desc = driver.find_element_by_xpath('//*[@id="ContentContainer1_ctl00_Content_Section_OVERVIEW_MainOverview"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td[7]')
    # target_primary_business_desc = driver.find_element_by_xpath

time.sleep(2)

sub_list.append(deal_type.text)
sub_list.append(deal_status.text)
sub_list.append(deal_value.text)

sub_list.append(completed_date.text)
sub_list.append(acquiror_name.text)
sub_list.append(acquiror_country.text)

#sub_list.append(target_name.text)
sub_list.append(target_country.text)
sub_list.append(pd_target_operating_revenue.text)
sub_list.append(pd_target_EBITDA.text)
sub_list.append(target_activity.text)
sub_list.append(target_bvd_sector_desc.text)

print(sub_list)

master_list.append(sub_list)
print(master_list)



time.sleep(10)
driver.close()
print("Done")