from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from barnum import gen_data

import names
import random
import string


def make_code():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    letters = string.ascii_lowercase
    random_mail = ''.join(random.choice(letters) for _ in range(6)) + '@mailsac.com'

    free_trial_link = 'https://www.maplesoft.com/products/maple/free-trial/'
    getlink = 'https://mailsac.com/inbox/'
    print("Download...")
    driver.get(free_trial_link)
    driver.find_element("xpath", "//input[@id='EmailAddress']").send_keys(random_mail)
    button = driver.find_element(By.XPATH, "//div[contains(text(),'Get your Free Trial')]")
    button.click()

    driver.find_element("xpath", "//input[@id='FirstName']").send_keys(names.get_first_name())
    driver.find_element("xpath", "//input[@id='LastName']").send_keys(names.get_last_name())
    driver.find_element("xpath", "//input[@id='Company']").send_keys(gen_data.create_company_name())
    driver.find_element("xpath", "//input[@id='JobTitle']").send_keys(gen_data.create_job_title())

    country_drop_list = Select(driver.find_element("xpath", "//*[@id='CountryDropDownList']"))
    country_drop_list.select_by_visible_text("United States")
    driver.implicitly_wait(5)
    ddl_segment = Select(driver.find_element("xpath", "//*[@id='ddlSegment']"))
    ddl_segment.select_by_visible_text("Commercial")
    driver.find_element("xpath", "//option[@value='CA  ']").click()
    driver.find_element("xpath", "//*[@id='chkAgreeToGDPR']").click()
    driver.find_element("xpath", "//*[@id='SubmitButton']").click()
    driver.implicitly_wait(10)

    driver.get(getlink + random_mail)
    driver.find_element("xpath", "/html/body/div[1]/div[3]/div[1]/div/div[2]/div/table/tbody/tr[2]/td[3]").click()

    div_element = driver.find_element(By.XPATH, "//div[@ng-bind-html='trustAsHtml(msg.body)']")

    div_content = div_element.text

    start_index = div_content.find("https://")

    end_index = div_content.find("\n", start_index)

    link = div_content[start_index:end_index]

    driver.get(link)

    expiration_date = driver.find_element("xpath", "//*[@id='evaluationExpiry']").text
    activation_code = driver.find_element("xpath", "//span[@id='evaluationPurchaseCode']").text
    print('\n')
    print('Activation code : ' + activation_code)
    print('Your evaluation will expire in ' + str(expiration_date))
    print('\n')

    print("Do you need a download link?\nEnter 1 or 2")
    print("1. Yes, thanks\n2. No, i already have Maple 2024")

    choose = int(input())
    if choose == 1:
        download_link = driver.find_element("xpath", "//span[@id='evaluationDownloadLink']").text
        print("Download link: " + download_link + "\n")
        print("Thanks for using the program")
    else:
        print("Thanks for using the program")


make_code()
