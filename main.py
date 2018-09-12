#import modules/libraries []
#testing selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutExceptions
from selenium.webdriver.common.by import By 
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC 
import os
import time

#Set ChromeDriver options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
#Set ChromeDriver path
dir_path = os.path.dirname(os.path.realpath(__file__))
chromedriver = dir_path + "/chromedriver"
#Set os environment
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=options, executable_path= chromedriver)
