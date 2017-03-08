from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page
from django.utils.html import escape
from django.template.loader import render_to_string
from lists.forms import ItemForm, EMPTY_LIST_ERROR

class HomePageTest(TestCase):
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_home_page_uses_item_form(self): # 检查home page 是否使用了 ItemForm
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
    
class ListViewTest(TestCase):
    def test_validation_errors_end_up_on_list_page(self):
        list_ = List.objects.create()  #增加清单
        
        response = self.client.post('/lists/%d/' % (list_.id), data = {'text':''})
        
        # 断言站点应该回应 http 200 而不是转跳 http 302 (根据设计，提交后要转跳到个人清单)
        self.assertEqual(response.status_code, 200)
        
        # 断言站点应该继续使用 list.html 模板
        self.assertTemplateUsed(response, 'list.html')
        
        # 断言页面上应该出现错误信息
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    
    # 如果验证有错误，应该渲染首页模版并且返回200响应
    def test_for_invalid_input_renders_home_page_template(self):
        response = self.client.post('/lists/new', data = {'text':''})#故意给空白值
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)
        
    # 如果验证有错误，响应中应该包含错误消息
    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data = {'text':''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        
    # 如果验证有错误，应该把表单对象传入模版
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data = {'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)
        
        
    def test_invalid_list_items_arent_saved(self):
        # 使用http client 连接站点，以post 方式提交一个空的待办事项
        response = self.client.post('/lists/new', data = {'text':''}) 
        
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
    
    def test_use_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,)) #用测试客户端，真的用http client 去测试 
        self.assertTemplateUsed(response, 'list.html')
        
    def test_displays_only_items_for_that_list(self): #测试是否能够正常显示特定list的条目
        correct_list = List.objects.create() #放入第1笔数据
        Item.objects.create(text = 'itemey 1', list=correct_list)
        Item.objects.create(text = 'itemey 2', list=correct_list)
        
        other_list = List.objects.create()#放入第2笔数据
        Item.objects.create(text = 'other list item 1', list=other_list)
        Item.objects.create(text = 'other list item 2', list=other_list)
        
        response = self.client.get('/lists/%d/' % (correct_list.id,)) #用测试客户端，真的用http client 去测试 
        
        self.assertContains(response, 'itemey 1') #返回的HTML里面应该要有 'itemey 1'
        self.assertContains(response, 'itemey 2')
        
        self.assertNotContains(response, 'other list item 1') 
        self.assertNotContains(response, 'other list item 2')
        
    def test_passes_correct_list_to_template(self): # 判断是否正确的传递了 List（context/参数） 给模板渲染网页
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()    #增加第一个清单
        correct_list = List.objects.create()  #增加第二个清单
        
        self.client.post('/lists/%d/' % (correct_list.id), data = {'text':'A new item for an existing list'})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_to_list_view(self):
        other_llist = List.objects.create()    #增加第一个清单
        correct_list = List.objects.create()  #增加第二个清单
        response = self.client.post('/lists/%d/' % (correct_list.id), data = {'text':'A new item for an existing list'})
        
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,)) #断言提交后应该要转跳
        
class NewListTest(TestCase):
    # ---- 测试 home_page 视图在 POST 时，是否能返回正确 html 的内容 ----
    def test_page_can_save_a_POST_request(self): 
        self.client.post('/lists/new', data = {'text':'A new list item'})
        
        self.assertEqual(Item.objects.count(), 1) # 断言数据表lists_item 中应该已经有 1 笔刚刚提交的数据了
        new_item = Item.objects.first() # 取回数据库中的第一笔
        self.assertEqual(new_item.text, 'A new list item') # 断言在第一笔数据中，数据表 lists_item 的字段-text 的值应该是 'A new list item'
        
    # ---- 测试 POST 时候能否 Redirect （PRG Patten）----
    def test_home_page_redirects_after_POST(self):
        response = self.client.post('/lists/new', data = {'text':'A new list item'})

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,)) #断言提交后应该要转跳

        
class empty(object):
    pass        
        