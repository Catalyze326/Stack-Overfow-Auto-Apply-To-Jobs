from selenium import webdriver
import re
import os
import time
emailPattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
experanceLevelPattern = re.compile("^[JjMmSsLl]")


def recursiveApply(linkNum = 0):
    time.sleep(5)
    if linkNum != 24:
        driver.get('https://stackoverflow.com/jobs/')
        site = driver.find_elements_by_class_name('s-link__visited')[linkNum]
        print(site)
        site.click()
        print(driver.page_source)
        if data[2].replace(' ', '') in driver.page_source:
            driver.find_element_by_class_name('_apply').click()
            driver.find_element_by_class_name('j-apply-btn').click()
        recursiveApply(linkNum + 1)
    else:
        driver.get('https://stackoverflow.com/jobs/')
        driver.find_element_by_class_name('test-pagination-next').click()
        recursiveApply(0)


if not os.path.isfile('metadata'):
    f = open("metadata", "w+")
    email = input('What is the email associated with your Stack Overflow account?')
    while not emailPattern.match(email):
        email = input('That is not a valid email address')
    f.write(email + '\n')

    password = input('What is the password you use to log into Stack Overflow. Note this is stored in the metadata file and not put anywhere else.\n Feel free to valadate that.')
    f.write(password + '\n')

    desiredLevel = input('What is the desired level of experance expectation that a job ought to have for you to apply. Options are Studnet, Junior, Mid-Level, Senior, Lead, or Manager')
    while not experanceLevelPattern.match(desiredLevel):
        desiredLevel = input('That is not a valid experance level. Chose one of the following. Student, Junior, Mid-Level, Senior, Lead, or Manager')
    f.write(desiredLevel + '\n')

    tags = input('What tags would you like to look fow as you apply for jobs? Some examples are Java, Python, or Bash. Please list these in a coma seperated form')
    f.write('tags: ' + tags + '\n')
else:
    f = open('metadata', 'r').readlines()
    print(f)
data = open('metadata', 'r').readlines()

driver = webdriver.Firefox() # Initialize the webdriver session
driver.get('https://stackoverflow.com/users/login') # replaces "ie.navigate"
driver.find_element_by_id('email').send_keys(data[0][:-1])
time.sleep(1)
driver.find_element_by_id('password').send_keys(data[1][:-1])
driver.find_element_by_id('submit-button').click()

driver.get('https://stackoverflow.com/jobs')
recursiveApply()