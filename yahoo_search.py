#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Yahoo!検索ワード自動入力＆画面キャプチャ
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

time.sleep(5)#5秒停止

w = driver.execute_script('return document.body.scrollWidth')
h = driver.execute_script('return document.body.scrollHeight')
driver.set_window_size(w, h)
driver.save_screenshot('screenshot.png')#キャプチャ画像出力
driver.quit()#ブラウザを閉じる

