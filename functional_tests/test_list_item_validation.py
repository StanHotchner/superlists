# -*- coding: utf-8 -*-
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页，他不小心提交了一个空的待办事项。输入框没有输入内容，他就按下了回车
        
        # 首页刷新了，显示一个错误消息 - “提交的待办事项不能为空”
        
        # 她输入了一些文字，然后再次提交。这次没有问题了
        
        # 她有点调皮，又提交了一个空的待办事项
        
        # 在清单页面他看到了一个相同的错误消息
        
        # 输入一些问题后再次提交就没有问题了
        pass
