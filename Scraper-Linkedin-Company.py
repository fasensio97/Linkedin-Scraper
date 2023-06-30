#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
#import xlsxwriter
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
#from unidecode import unidecode
import os


# # Opcion scrapear Google

# In[2]:


#Ingresar en la cuenta
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
driver.find_element(By.ID, 'username').send_keys('pablitogomez19234@gmail.com') #Enter username of linkedin account here
driver.find_element(By.ID,'password').send_keys('')  #Enter Password of linkedin account here
driver.find_element(By.XPATH,"//*[@type='submit']").click()

            


# In[25]:



#*********** Search Result ***************#
search_key = " Techint" # Enter your Search key here to find people
key = search_key.split()
keyword = ""
for key1 in key:
    keyword = keyword + str(key1).capitalize() +"%20"
keyword = keyword.rstrip("%20")
for no in range(1,2):
        start = "&page={}".format(no) 
        search_url = "https://www.linkedin.com/search/results/companies/?keywords={}&origin=SUGGESTION{}".format(keyword,start)
        driver.get(search_url)
        driver.maximize_window()


# In[26]:


# Hace clic en el enlace de la primera empresa de la lista
# Hace clic en el enlace de la primera empresa de la lista
first_company_link = driver.find_element(By.XPATH, "//a[contains(@href, 'company')]")
first_company_link.click()
#driver.find_element(By.XPATH,'//*[@id="0EpSOFaqQhKd1hivdJqypA=="]/div/ul/li[1]/div/div/div[2]/div[1]/div[1]/div/span/span/a').click()


# In[28]:


#empleado = driver.find_element(By.XPATH, '//*[@id="ember225"]/h3' ).text
#empleado

employee_info = driver.find_element(By.XPATH, "//h3[@class='t-16 t-bold mb3 hoverable-link-text']")
print(employee_info.text)
employee_info = driver.find_element(By.XPATH, "//span[@class='org-top-card-secondary-content__see-all t-normal t-black--light link-without-visited-state link-without-hover-state']")
print(employee_info.text)

#employee_info = driver.find_element(By.XPATH, "//div[@class='mt2']//h3")
#employee_info
#<<h3 class="t-16 t-bold mb3 hoverable-link-text">
        #  1.802 empleados trabajan en Buenos Aires
      #  </h3>
#//*[@id="ember224"]/h3


# In[ ]:




