import time
import pygsheets
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#scrape data
driver = webdriver.Chrome()

user_agent = UserAgent()
opt = webdriver.ChromeOptions()
opt.add_argument("--user-agent=%s" % user_agent)
opt.add_argument("--headless")  # 啟用 headless 模式
opt.add_argument("--disable-gpu")  # 關閉 GPU 
user_agent.random

# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })

driver.get('https://www.dcard.tw/f/nba')

element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'atm_cs_1urozh')))
time.sleep(10)
driver.execute_script("window.scrollTo(0,600)")

eles_url = driver.find_elements(By.CLASS_NAME,'atm_cs_1urozh')

ta_url=[]
for ele in eles_url:
    href = ele.get_attribute("href")
    ta_url.append(href)
#89 72 33 04 36 89

ta_url.pop(0)
ta_url.pop(0)


driver.quit()

article = []
title =[]
comment = []


for i in ta_url:
    driver = webdriver.Chrome()
    opt = webdriver.ChromeOptions()
    user_agent = UserAgent()
    opt.add_argument("--user-agent=%s" % user_agent)
    opt.add_argument("--headless")  # 啟用 headless 模式
    opt.add_argument("--disable-gpu")  # 關閉 GPU 
    user_agent.random
    
    driver.get(i)
    
    time.sleep(1)  
    
    for i in range(2):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    
    # print(driver.find_element(By.XPATH,'//*[@id="dcard-comment-anchor"]/div/div/div[3]').text == '')

    try:
        if driver.find_element(By.XPATH,'//*[@id="dcard-comment-anchor"]/div/div/div[3]').text == '':
            eles = driver.find_element(By.XPATH,'//*[@id="dcard-comment-anchor"]/div/div/div[2]')    
            eles2 = eles.find_elements(By.CLASS_NAME,'atm_vv_1btx8ck')
            print(1)
            
            for ele in eles2:
                comment.append(ele.text)
                
                #title
                title.append(driver.find_elements(By.CLASS_NAME,"atm_cs_1udz34")[0].text)
                #article
                source = driver.page_source
                soup = bs(source, 'html.parser')
                ind = soup.select('div.atm_lo_c0ivcw')
                article.append(ind[0].text)
                 
        else:
            eles = driver.find_element(By.XPATH,'//*[@id="dcard-comment-anchor"]/div/div/div[3]')
            eles2 = eles.find_elements(By.CLASS_NAME,'atm_vv_1btx8ck')  
            print(2)
            
            for ele in eles2:
                comment.append(ele.text)
                
                #title
                title.append(driver.find_elements(By.CLASS_NAME,"atm_cs_1udz34")[0].text) 
                #article
                source = driver.page_source
                soup = bs(source, 'html.parser')
                ind = soup.select('div.atm_lo_c0ivcw')
                article.append(ind[0].text)
    except:
        # title
        title.append(driver.find_elements(By.CLASS_NAME,"atm_cs_1udz34")[0].text)
        #article
        source = driver.page_source
        soup = bs(source, 'html.parser')
        ind = soup.select('div.atm_lo_c0ivcw')
        article.append(ind[0].text) 
        print('not data')
              
    driver.quit()     
# .get_attribute('data-original-title') 
#data-original-title="<img src='https://t.jpg'>

#write in
#mail: interview@interview-2023.iam.gserviceaccount.com
auth_file = "C:\\Users\A0258\\interview\\interview-2023-7f639a103409.json"
gc = pygsheets.authorize(service_file = auth_file)

sheet_url = 'https://docs.google.com/spreadsheets/d/18eLDSUBnEbJmUYgvJ5ECYXXi6sBFICLtp5fL2ELS9_s/'
sheet = gc.open_by_url(sheet_url)
sheet_one = sheet.worksheet_by_title('sheet 1')

my_dict = { 'title':title,
          'article':article,
          'comment':comment
    }
all_df = pd.DataFrame(my_dict)

sheet_one.set_dataframe(all_df,(1,1)) # Place DataFrame from row 1 column 1 
# print(stu.get_row(4,include_tailing_empty=False)) # for testing 
