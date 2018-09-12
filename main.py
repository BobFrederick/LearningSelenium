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
    # Create a new instance of the Chrome driver and set options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    #Set ChromeDriver path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    #Set os environment and check platform
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

    '''Load Data'''
    # wait until the ALL Zimas Data Tabs are loaded
    ZimasDataElement = wait.until(EC.visibility_of_all_elements_located((By.ID, "divDataTabs")))
    # open all the data tabs by clicking them

    '''Different Methods for opening the tabs'''
    #this one tries to have a filter for the first tab since it opens on start (still having trouble)
    #dataTabs = driver.find_elements_by_xpath("//a[@onclick='toggleDataTab(this);'][not(contains(text(),'Address'))]")
    #this just uses xpath
    #dataTabs = driver.find_elements_by_xpath("//a[@onclick='toggleDataTab(this);']") 

    #This method just looks for a unique css onclick value
    dataTabs = driver.find_elements_by_css_selector("a[onclick*=toggleDataTab]")
    #Instead of the filter we just start the loop at 1 and skip opening the already open tab
    for i in range(1,len(dataTabs)):
        dataTabs[i].click()

    '''Address/Legal'''
    # get all the Address/Legal Data in Keys and Values and build a Dict
    Address_Legal_Data = {}
    legalRawData = []
    legalKeys = []
    legalValues = []
    #Get single data tab
    legalDataTable = driver.find_element_by_xpath("//div[@id='divTab1']/table/tbody")
    #Get all data tab
    #legalDataTable = driver.find_elements_by_xpath

    #Get the row and cols
    for rows in legalDataTable.find_elements_by_xpath('.//tr'):
        for col in rows.find_elements_by_xpath('.//td'):
            legalRawData.append(col.get_attribute('innerText'))
    #print(legalRawData)

    #Separate the raw data into values and keys     
    for num in range(len(legalRawData)):
        if num % 2 == 0:
            legalKeys.append(legalRawData[num])
        else:
            legalValues.append(legalRawData[num])

    #Make the dictionary
    Address_Legal_Data = dict(zip(legalKeys,legalValues))

    for k, v in Address_Legal_Data.items():
        print(k,v)

    driver.quit()

if __name__ == "__main__":
  main()
