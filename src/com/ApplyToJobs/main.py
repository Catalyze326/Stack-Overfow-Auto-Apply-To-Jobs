from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

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
            'What is the password you use to log into Stack Overflow. Note this is stored in the metadata file and not put anywhere else.\n Feel free to valadate that.')
        f.write(password + '\n')

        desiredLevel = input(
            'What is the desired level of experance expectation that a job ought to have for you to apply. Options are Studnet, Junior, Mid-Level, Senior, Lead, or Manager')
        while not experanceLevelPattern.match(desiredLevel):
            desiredLevel = input(
                'That is not a valid experance level. Chose one of the following. Student, Junior, Mid-Level, Senior, Lead, or Manager')
        f.write(desiredLevel + ',')

        tags = input(
            'What is a language or framework that you would like to work with?')
        f.write(tags + '\n')
        return open('metadata', 'r').readlines()
    else:
        return open('metadata', 'r').readlines()


def login():
    driver.get('https://stackoverflow.com/users/login')  # replaces "ie.navigate"
    driver.find_element_by_id('email').send_keys(data[0][:-1])
    time.sleep(1)
    driver.find_element_by_id('password').send_keys(data[1][:-1])
    driver.find_element_by_id('submit-button').click()
    driver.get('https://stackoverflow.com/jobs')


# TODO close other links
def recursiveApply(linkNum = 0):
    time.sleep(5)
    if linkNum != 24:
        driver.get('https://stackoverflow.com/jobs/')
        site = driver.find_elements_by_class_name('s-link__visited')[linkNum]
        try:
            site.click()
        except ElementClickInterceptedException:
            print('It failed to click on a new job link')
            driver.get('https://stackoverflow.com/jobs/')
            recursiveApply(linkNum + 1)
        jobInfo = driver.find_elements_by_class_name('fw-bold')
        moveOn = False
        for qualitiy in data[2].split(','):
            for info in jobInfo:
                if qualitiy.replace(' ', '') in info.text:
                    moveOn = True
        if not moveOn:
            print('The listing did not contain the experience level preference of the user')
            driver.get('https://stackoverflow.com/jobs/')
            recursiveApply(linkNum + 1)

        try:
            driver.find_element_by_class_name('_apply').click()
            driver.find_element_by_class_name('j-apply-btn').click()
        except NoSuchElementException:
            print('It did not find the second apply button therefore it is not an easy apply site')
        recursiveApply(linkNum + 1)
    else:
        driver.get('https://stackoverflow.com/jobs/')
        driver.find_element_by_class_name('test-pagination-next').click()
        recursiveApply(0)


data = getUserData()
login()
recursiveApply()