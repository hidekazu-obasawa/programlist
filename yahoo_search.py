#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Yhoo!検索ワード自動入力
from selenium import webdriver
import time

#Chromeを操作
driver = webdriver.Chrome()
#WEBページを開く
driver.get("https://www.yahoo.co.jp/");

time.sleep(5)#5秒停止

search_box = driver.find_element_by_class_name('_1wsoZ5fswvzAoNYvIJgrU4')
serch_word = input("検索キーワードを入力してください。")
search_box.send_keys(serch_word)
search_btn = driver.find_element_by_class_name('PHOgFibMkQJ6zcDBLbga8')
search_btn.click()

