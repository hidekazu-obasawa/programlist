#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Google検索ワード自動入力
from selenium import webdriver
import time

#Chromeを操作
driver = webdriver.Chrome()
#WEBページを開く
driver.get("https://www.google.co.jp/");

time.sleep(5)#5秒停止

search_box =  driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[2]/input")
serch_word = input("検索キーワードを入力してください。")
search_box.send_keys(serch_word)
search_btn = driver.find_element_by_class_name('gNO89b')
search_btn.click()

