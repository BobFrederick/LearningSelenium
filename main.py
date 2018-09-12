#************************************************************************************
# Purpose: Pulls data from http://zimas.lacity.org/
# Inputs:  houseNum, steetName: the address to search
# Returns: dict of the Zimas data
# Title:    main.py
# Author:  Bob Frederick
# Date Created:   2018-09-12 16:39:24
# TODO:    Add a try catch or except to catch the data tabs that aren't always visible.
#          Build an error handler for incorrect user input
#************************************************************************************

def main():

    #import modules/libraries []
 
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
    from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
    import os
    from sys import platform

    # Primary User Input
    houseNum = '4402'
    streetName = 'Berenice'

    '''Setup Chrome Webdriver'''
    # create a new instance of the Chrome driver and set options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # set the options to run headless
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    # set ChromeDriver path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # set os environment and check platform
    if platform == "linux" or platform == "linux2":
        chromedriver = dir_path + "/chromedriver.exe"
    elif platform == "darwin":
        chromedriver = dir_path + "/chromedriver"
    elif platform == "win32":
        chromedriver = dir_path + "/chromedriver.exe"

    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)

    '''Inital startup'''
    # go to the zimas webpage
    driver.get("http://zimas.lacity.org")
    # find the element that's name attribute is btn (the accept user agreement button)
    userAgreement = driver.find_element_by_class_name('btnaccept')
    # accept the agreement 
    userAgreement.click()

    '''Address Input'''
    # wait until Address dialog is loaded
    wait = WebDriverWait(driver, 10)
    addressDialog = wait.until(EC.element_to_be_clickable((By.ID, 'btnSearchGo')))
    # find the house number element and enter the first part of the address
    houseNumInput = driver.find_element_by_id('txtHouseNumber')
    houseNumInput.send_keys(houseNum)
    # find the street name element and enter the second part of the address
    strNameInput = driver.find_element_by_id('txtStreetName')
    strNameInput.send_keys(streetName)
    # find and click the search "Go" button
    goBtn = driver.find_element_by_id("btnSearchGo")
    goBtn.click()

    '''Load Data from UI'''
    # wait until the ALL Zimas Data Tabs are loaded
    ZimasDataElement = wait.until(EC.visibility_of_all_elements_located((By.ID, "divDataTabs")))
    # open all the data tabs by clicking them
    # this method just looks for a unique css onclick value to find the dropdown tabs and opens those tabs
    dataTabs = driver.find_elements_by_css_selector("a[onclick*=toggleDataTab]")
    # The first tab is open by defalult so instead of filtering that tab we just start the loop at 1 and skip opening that tab
    # TODO(bfrederick@rchstudios.com): This click fails sometimes because all of the tabs aren't immediately visible. We might use the Selenium wait.
    for i in range(1,len(dataTabs)):
        dataTabs[i].click()

    '''Get & Process Data'''
    # get all the raw data from the Zimas information tab in Keys and Values and build a Dict
    zimasData = {}
    rawData = []
    dataKeys = []
    dataValues = []
    # get all the tables for each section i.e. Address, Zoning, Assessor
    dataTables = driver.find_elements_by_xpath("//div[contains(@id,'divTab')]/table/tbody")

    # add raw data to a list
    for rows in dataTables:
        rawData.append(rows.text)
 
    # separate the raw data into values and keys     
    for num in range(len(rawData)):
        if num % 2 == 0:
            dataKeys.append(rawData[num])
        else:
            dataValues.append(rawData[num])

    # make the dictionary
    zimasData = dict(zip(dataKeys,dataValues))

    # print values to check
    for k, v in zimasData.items():
        print(k,v)

    # close chromedriver
    driver.quit()

if __name__ == "__main__":
  main()
