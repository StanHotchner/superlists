# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class LayoutAndStyingTest(FunctionalTest):
    def test_layout_and_styling(self):
        #伊迪丝访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        
        #她看到输入框完美的居中显示
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] /2 , 512, delta = 5)
        
        #她新建了一个清单，看到输入框仍然完美居中
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] /2 , 512, delta = 5)
