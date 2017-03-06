# -*- coding: utf-8 -*-
#from django.test import LiveServerTestCase
import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return 
        super().setUpClass()
        cls.server_url = cls.live_server_url
    @classmethod
    def tearDown(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
            
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrive_it_later(self): #可以开启一个列表并且之后可以重新读取
        #伊迪丝听说有一个很酷的在线代办事项应用
        #他去看了这个应用的首页（他应该要能正常的开启页面）
        self.browser.get(self.server_url)
        
        #他注意到网页的标题和头部都包含了To-Do这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        #页面上有个地方可以让他输入一个待办事项(应该是一个文本框，文本框中要有一个占位符 xxxx)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
      
        #伊迪丝钓鱼时喜欢用孔雀羽毛做成的假苍蝇为钓饵
        #他在文本框中输入了 "Buy peacock feathers"
        inputbox.send_keys('Buy peacock feathers')
        
        #他点击回车后页面更新了
        inputbox.send_keys(Keys.ENTER) # Form summit 提交了
        time.sleep(2)
        
        #伊迪丝提交了第一个待办事项后，我们希望应用创建一个新清单，并在这个清单中添加一个待办事项，然后把他带到显示这个清单的页面 
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+') # 
        
        #待办事项表格中应该要显示了 "1:Buy peacock feathers"
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        
        #页面中又显示了一个文本框，可以输入其他的待办事项
        #他输入了 "Use peacock feathers to make a fly"并且按下回车
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER) 
        time.sleep(2)
        
        #页面再次更新并且显示了这两个待办事项
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')
        
        #伊迪丝想知道这个网站是否能记住他的清单
        
        #现在一个叫做佛朗西斯的用户访问了网站
        #我们使用了一个新的浏览器回话，确保伊迪丝的信息不会从cookie中泄露
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #佛朗西斯访问首页，页面中看不到伊迪丝的清单
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text) #1
        self.assertNotIn('to make a fly', page_text)#2
        
        #佛朗西斯输入一个新待办事项，新建一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        
        #佛朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')#3
        self.assertNotEqual(edith_list_url, francis_list_url) #4
        
        #这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
    
class LayoutAndStyingTest(FunctionalTest):
    def test_layout_and_styling(self):
        #伊迪丝访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        
        #她看到输入框完美的居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] /2 , 512, delta = 5)
        
        #她新建了一个清单，看到输入框仍然完美居中
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] /2 , 512, delta = 5)

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页，他不小心提交了一个空的待办事项。输入框没有输入内容，他就按下了回车
        
        # 首页刷新了，显示一个错误消息 - “提交的待办事项不能为空”
        
        # 她输入了一些文字，然后再次提交。这次没有问题了
        
        # 她有点调皮，又提交了一个空的待办事项
        
        # 在清单页面他看到了一个相同的错误消息
        
        # 输入一些问题后再次提交就没有问题了
        pass
        
        
        
        #self.fail('Finish the test with fail!')
        
#if __name__ == '__main__':
#    unittest.main(warnings = 'ignore')
        
    
