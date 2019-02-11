
"""
Created on Mon Feb 11 08:47:20 2019

Author: Juan Diaz Amorin
Contact: juandiazamorin96@gmail.com
         juan.diaz1@unmsm.edu.pe

"""
import time

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from datetime import datetime


chromedriver = 'C:/Users/juan.diaz/Desktop/chromedriver'
driver = webdriver.Chrome(chromedriver)

region = []
authorized_amount = []
registered_amount = []
variable = []
year = []

current_year = datetime.now().year

start = time.time()
for k in range(2004, current_year):
    print('Year:', str(k))
    driver.get('http://apps5.mineco.gob.pe/transferencias/gl/default.aspx')
    
    driver.switch_to_frame('superior')
    year_selection = Select(driver.find_element_by_id('drpAno'))
    year_selection.select_by_value(str(k))
    
    driver.switch_to_default_content()
    driver.switch_to_frame('inferior')
    driver.find_element_by_id('BTRecurso').click()
    
    driver.switch_to_default_content()
    driver.switch_to_frame('superior')   
    
    soup_level1 = BeautifulSoup(driver.page_source,'html.parser')
    items = soup_level1.find_all(class_='Resultados')
      
    for i in range(0,len(items)):
        x = items[i].get_text().replace('\n','').replace('  ','')
        driver.switch_to_default_content()
        driver.switch_to_frame('superior')
        driver.find_element_by_id('tr'+str(i)).click()
        driver.switch_to_default_content()
        driver.switch_to_frame('inferior')
        driver.find_element_by_name('BTDepartamento').click()
        
        driver.switch_to_default_content()
        driver.switch_to_frame('superior')
        soup_level2 = BeautifulSoup(driver.page_source,'html.parser')
        regions = soup_level2.find_all(class_ = 'Resultados')

        for j in range(0, len(regions)):
            regions = soup_level2.find("tr", {"id": "tr"+str(j)}).select('td')
            m1 = regions[1].get_text().replace('\n','').replace('  ','')
            region.append(m1)
            m2 = regions[2].get_text().replace('\n','').replace('  ','').replace(',','')
            authorized_amount.append(float(m2))
            m3 = regions[3].get_text().replace('\n','').replace('  ','').replace(',','')
            registered_amount.append(float(m3))
            variable.append(x)
            year.append(k)
        
        return_items = driver.find_element_by_id('ImgBack').click()
  

data = {'variable': variable, 'year':year, 'region': region,
        'authorized_amount': authorized_amount, 'registered_amount': registered_amount}
 
data = pd.DataFrame(data=data)
end = time.time()
print('Elapsed time:',end-start)
