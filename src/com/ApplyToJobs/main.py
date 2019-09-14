from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException
from selenium.webdriver.support.ui import Select
import re
import os
import time

emailPattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
experanceLevelPattern = re.compile("^[JjMmSsLl]")
driver = webdriver.Firefox()
data = {}


def getUserData():
    if not os.path.isfile('metadata'):
        f = open("metadata", "w+")
        email = input('What is the email associated with your Stack Overflow account?')
        while not emailPattern.match(email):
            email = input('That is not a valid email address')
        f.write(email + '\n')

        password = input(
            'What is the password you use to log into Stack Overflow. Note this is stored in the metadata file and not put anywhere else. Feel free to valadate that.')
        f.write(password + '\n')
        # TODO allow for more than one
        desiredLevel = input(
            'What is the minimum desired level of experance expectation that a job ought to have for you to apply. '
            'Options are Studnet, Junior, Mid-Level, Senior, Lead, or Manager. ')
        while not experanceLevelPattern.match(desiredLevel):
            desiredLevel = input(
                'That is not a valid experance level. Chose one of the following. Student, Junior, Mid-Level, Senior, Lead, or Manager. Be sure to capatlize the first letter of the level you chose.')
        f.write(desiredLevel + '\n')

        desiredLevel = input(
            'What is the maximum desired level of experance expectation that a job ought to have for you to apply. '
            'Options are Studnet, Junior, Mid-Level, Senior, Lead, or Manager. ')
        while not experanceLevelPattern.match(desiredLevel):
            desiredLevel = input(
                'That is not a valid experance level. Chose one of the following. Student, Junior, Mid-Level, Senior, Lead, or Manager. Be sure to capatlize the first letter of the level you chose.')
        f.write(desiredLevel + '\n')

        tags = input(
            'What are some technologies you like? Separate them by spaces.')
        f.write(tags + '\n')

        langs = input(
            "What are some languages you don't like? Separate by spaces.")
        f.write(langs)

        salary = input(
            "What is your desired salary?.")
        f.write(salary)
        return open('metadata', 'r').readlines()
    else:
        return open('metadata', 'r').readlines()


def login():
    driver.get('https://stackoverflow.com/users/login')
    driver.find_element_by_id('email').clear()
    driver.find_element_by_id('email').send_keys(data[0][:-1])
    time.sleep(1)
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys(data[1][:-1])
    driver.find_element_by_id('submit-button').click()
    driver.get('https://stackoverflow.com/jobs')
    time.sleep(1)



# TODO close other links
def recursiveApply(linkNum = 0):
    print("Ran Recursive Apply\nLinkNumber = " + str(linkNum))
    time.sleep(15.12)
    # TODO get back to the jobs listing without going back to page 0
    driver.get('https://stackoverflow.com/jobs')
    params = driver.find_elements_by_class_name('js-tab-wrapper')
    params[0].find_element_by_xpath(".//*[@href='#']").click()
    driver.find_element_by_id('tageditor-replacing-tl--input').send_keys(data[5])
    driver.find_element_by_id('tageditor-replacing-td--input').send_keys(data[4])
    params[1].find_element_by_xpath(".//*[@href='#']").click()
    driver.find_element_by_id('s').send_keys(data[6].replace('\n', '').replace(',', ''))
    params[3].find_element_by_xpath(".//*[@href='#']").click()
    Select(driver.find_element_by_id('ms')).select_by_visible_text(data[2].replace('\n', ''))
    Select(driver.find_element_by_id('mxs')).select_by_visible_text(data[3].replace('\n', ''))
    params[0].find_element_by_xpath(".//*[@href='#']").click()
    driver.find_element_by_class_name('btn').click()
    for i in range(int(linkNum / 23)):
        driver.find_element_by_class_name('test-pagination-next').click()
        time.sleep(5)
    site = driver.find_elements_by_class_name('s-link__visited')[int(linkNum % 23)]
    try:
        site.click()
        print("\nClicked on new Job listing.")
    except ElementClickInterceptedException:
        print('It failed to click on a new job link')
        driver.get('https://stackoverflow.com/jobs')
        recursiveApply(linkNum + 1)
    time.sleep(1)
    driver.execute_script('document.getElementsByClassName("sidebar")[0].remove();')
    driver.execute_script('document.getElementById("more-jobs-items").remove();')
    jobTitle = driver.find_element_by_class_name('fc-black-900').text
    print('Looking at job listing "' + jobTitle + '"')
    try:
        driver.find_element_by_class_name('_apply').click()
        driver.find_element_by_class_name('j-apply-btn').click()
        print('We applied to a job titled: ' + jobTitle)
        open('JobsAppliedTo.txt', 'a+').write(jobTitle + '        ' + driver.current_url + '\n')
        recursiveApply(linkNum + 1)
    except NoSuchElementException:
        print('It was not a proper form easy apply site')
        recursiveApply(linkNum + 1)
    except NoSuchWindowException:
        recursiveApply(linkNum + 1)


data = getUserData()
time.sleep(1)
login()
recursiveApply()



