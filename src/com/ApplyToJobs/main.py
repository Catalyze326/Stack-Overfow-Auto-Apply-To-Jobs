from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchWindowException

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
            'What is the desired level of experance expectation that a job ought to have for you to apply. '
            'Options are Studnet, Junior, Mid-Level, Senior, Lead, or Manager. You can pick more than one.')
        while not experanceLevelPattern.match(desiredLevel):
            desiredLevels = input(
                'That is not a valid experance level. Chose one of the following. Student, Junior, Mid-Level, Senior, Lead, or Manager. Be sure to capatlize the first letter of the level you chose.')
        f.write(desiredLevel + '\n')

        tags = input(
            'What are some language or framework that must be a part of the job you want to apply for?')
        f.write(tags + '\n')

        langs = input(
            'What are some languages or frameworks you would like to NOT work with. Put these in a coma seperated list? Be sure to capatalize the first letter of each word')
        f.write(langs)
        return open('metadata', 'r').readlines()
    else:
        return open('metadata', 'r').readlines()


def login():
    driver.get('https://stackoverflow.com/users/login')  # replaces "ie.navigate"
    driver.find_element_by_id('email').clear()
    driver.find_element_by_id('email').send_keys(data[0][:-1])
    time.sleep(1)
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys(data[1][:-1])
    driver.find_element_by_id('submit-button').click()
    driver.get('https://stackoverflow.com/jobs')


# TODO close other links
def recursiveApply(linkNum = 0):
    print("Ran Recursive Apply")
    time.sleep(5.12)
    if linkNum % 23 != 0:
        # TODO get back to the jobs listing without going back to page 0
        driver.get('https://stackoverflow.com/jobs/')
        driver.find_element_by_class_name('test-pagination-next').click()
        site = driver.find_elements_by_class_name('s-link__visited')[int(linkNum % 23)]
        try:
            site.click()
            print("\nClicked on new Job listing.")
        except ElementClickInterceptedException:
            print('It failed to click on a new job link')
            driver.get('https://stackoverflow.com/jobs/')
            recursiveApply(linkNum + 1)
        time.sleep(1)
        driver.execute_script('document.getElementsByClassName("sidebar")[0].remove();')
        driver.execute_script('document.getElementById("more-jobs-items").remove();')
        pureHTML = driver.page_source
        jobTitle = driver.find_element_by_class_name('fc-black-900').text
        print('Looking at job listing "' + jobTitle + '"')
        moveOn = False
        # Things you want in every posting
        for qualitiy in data[2].split(','):
            if qualitiy.replace(' ', '') in pureHTML:
                print('Listing has: ' + qualitiy)
                moveOn = True
        if not moveOn:
            print('The job listing is missing some quality you required.')
            recursiveApply(linkNum + 1)
        # Things to avoid in a posting
        for qualitiy in data[3].split(','):
            if qualitiy.replace(' ', '') in pureHTML:
                print('Found quality: ' + qualitiy + ' which we are avoiding.')
                recursiveApply(linkNum + 1)
        else:
            try:
                driver.find_element_by_class_name('_apply').click()
                driver.find_element_by_class_name('j-apply-btn').click()
                print('We applied to a job titled: ' + jobTitle)
                open('JobsAppliedTo.txt', 'a+').write(jobTitle + '\n')
                recursiveApply(linkNum + 1)
            except NoSuchElementException:
                print('It was not a proper form easy apply site')
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                recursiveApply(linkNum + 1)
            except NoSuchWindowException:
                recursiveApply(linkNum + 1)
    else:
        driver.get('https://stackoverflow.com/jobs/')
        driver.find_element_by_class_name('test-pagination-next').click()
        recursiveApply(linkNum + 1)



data = getUserData()
time.sleep(1)
login()
recursiveApply()



