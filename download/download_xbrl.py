
#encoding:utf-8

import sys
import time
import codecs
import csv
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def download_xbrl(driver, company):
  code = company[0]
  company_name = company[1]

  print("start " + code + ": " + company_name)
  driver.find_element_by_class_name("kensaku").click()
  driver.find_elements_by_class_name("menuItem")[1].click()

  # set EDINET code
  driver.find_element_by_name("sec").send_keys(code)

  # open pane to set document type
  driver.find_elements(By.XPATH, "//div[@class='panel_silver']")[3].click()
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "doc_kn2")))
  driver.find_element_by_id("doc_kn2").click()

  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "otd1")))
  driver.find_element_by_id("otd1").click()
  time.sleep(1)

  # open pane to set time period
  driver.find_elements(By.XPATH, "//div[@class='panel_silver']")[4].click()

  #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//select[@name='pfs']")))
  WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//select[@name='pfs']")))
  select = Select(driver.find_element(By.XPATH, "//select[@name='pfs']"))
  # set all periods
  select.select_by_index(6)

  # search
  driver.find_element_by_id("sch").click()

  # parse result table
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='result']/table")))
  elements = driver.find_elements(By.XPATH, "//div[@class='result']/table/tbody/tr")
  print("# of rows=" + str(len(elements)))

  for i in range(len(elements)):
    # skip header
    if i == 0:
      continue

    e = elements[i].find_elements(By.XPATH, "./td")
    print(e[1].find_element(By.XPATH,".//a").text)
    try:
      link = elements[i].find_elements(By.XPATH, "./td")[6].find_element(By.XPATH, ".//a")
      link.click()
    except NoSuchElementException:
      print('skip row_' + str(i))

    time.sleep(1)

def get_edinet_code(filename):
  company_list = []
  with codecs.open(filename, "r", "utf_8") as fin:
    csvread = csv.reader(fin)
    for row in csvread:
      if len(row) < 5:
        continue
      if row[1] == u"内国法人・組合":
        company = (row[0], row[6])
        company_list.append(company)

  return company_list

def get_config(filename):
    fp = open(filename,"r")
    config = dict(json.load(fp))
    fp.close()
    print(config)
    return config

#
# main
#
args = sys.argv

config = get_config(args[1])

prefs = {"download.default_directory": config["downloadpath"]}

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)

start_page = "http://disclosure.edinet-fsa.go.jp/"

driver = webdriver.Chrome(config["driverpath"] + "\\chromedriver.exe",chrome_options=options)
driver.get(start_page)

# get list of companies
# You can download csv in http://disclosure.edinet-fsa.go.jp/ and convert to utf8
company_list = get_edinet_code("EdinetcodeDlInfo.utf8.csv")

for company in company_list:
  download_xbrl(driver, company)

driver.quit()
driver.close()
