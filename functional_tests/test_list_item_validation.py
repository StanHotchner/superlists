# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
        
    def test_error_message_are_closed_on_input(self):
        # 伊迪丝新建一个清单，但错误的输入了一个空白，所以出现了一个验证错误
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('')
        inputbox.send_keys(Keys.ENTER) 
        time.sleep(2)
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())
        
        # 为了消除错误他开始在输入框中输入内容
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy fruit')
        time.sleep(2)
        
        # 看到错误消失了他很高兴
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
        
    def test_cannot_add_duplicate_items(self):
        # 伊迪丝访问首页，新建了一个清单
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER) # Form summit 提交了
        time.sleep(2)
        self.check_for_row_in_list_table('1:Buy peacock feathers')

        
        # 他不小心输入了重复的待办事项
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER) # Form summit 提交了
        time.sleep(2)
        
        # 他看到了一条有帮助的错误消息
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")
        
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页，他不小心提交了一个空的待办事项。输入框没有输入内容，他就按下了回车
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        time.sleep(2)
        
        # 首页刷新了，显示一个错误消息 - “提交的待办事项不能为空”
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # 她输入了一些文字，然后再次提交。这次没有问题了
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        self.check_for_row_in_list_table('1:Buy milk')
        
        # 她有点调皮，又提交了一个空的待办事项
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        
        # 在清单页面他看到了一个相同的错误消息
        self.check_for_row_in_list_table('1:Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # 输入一些问题后再次提交就没有问题了
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Make tea')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        self.check_for_row_in_list_table('1:Buy milk')
        self.check_for_row_in_list_table('2:Make tea')
        
