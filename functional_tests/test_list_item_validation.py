# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页，他不小心提交了一个空的待办事项。输入框没有输入内容，他就按下了回车
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        time.sleep(2)
        
        # 首页刷新了，显示一个错误消息 - “提交的待办事项不能为空”
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # 她输入了一些文字，然后再次提交。这次没有问题了
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        self.check_for_row_in_list_table('1:Buy milk')
        
        # 她有点调皮，又提交了一个空的待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        
        # 在清单页面他看到了一个相同的错误消息
        self.check_for_row_in_list_table('1:Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # 输入一些问题后再次提交就没有问题了
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Make tea')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        self.check_for_row_in_list_table('1:Buy milk')
        self.check_for_row_in_list_table('2:Make tea')
        
