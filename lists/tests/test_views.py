from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page
from django.utils.html import escape
from django.template.loader import render_to_string
from lists.forms import ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from unittest import skip

class HomePageTest(TestCase):
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_home_page_uses_item_form(self): # 检查home page 是否使用了 ItemForm
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
    
class ListViewTest(TestCase):
    # 产生不合法输入的提交
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/%d/' % (list_.id), data = {'text':''})
    
    def test_display_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')
        
    def test_for_invaild_input_nothing_saved_to_db(self): # 不合法输入产生时，不会有任何数据保存到数据库中
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
        
    # 不合法输入产生时，要渲染 list.html 模版
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.status_code, 200)
        
    # !!!!! 不合法输入产生时，要传递表单（form）给模板
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        
    # 不合法输入产生时，页面要显示错误信息
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
    
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create() 
        item1 = Item.objects.create(list = list1, text = 'abc123')
        response = self.client.post('/lists/%d/' % (list1.id), data = {'text':'abc123'})
        
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)
 
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
        
    # 如果验证有错误，数据库不会保存任何东西
    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new', data = {'text':''}) 
        
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

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
        