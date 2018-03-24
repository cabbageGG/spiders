#-*- coding: utf-8 -*-

# author: li yangjin

from selenium import webdriver
import time

browser = webdriver.Chrome(executable_path="C:/opt/chromedriver.exe")

browser.get("http://www.zhihu.com/")

browser.find_element_by_css_selector("div.SignFlow-accountInput.Input-wrapper input.Input").send_keys("13246856469")
browser.find_element_by_css_selector("div.SignFlow-password div.SignFlowInput div.Input-wrapper input.Input").send_keys("68ba70ma92wo")
browser.find_element_by_css_selector("button.SignFlow-submitButton").click()



