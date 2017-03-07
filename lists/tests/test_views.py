from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page
from django.utils.html import escape

class HomePageTest(TestCase):

    # ---- 测试根 URL 是否能够正常解析到对应的 view ----
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        
    # ---- 测试能否返回正确的 Home 页面 ----
    
    def test_home_page_return_currect_html(self):
        request = HttpRequest() #模拟客户端发送一个Http请求
        response = home_page(request) #把客户端 http 请求交给 home_page() 来处理
        
        content = response.content.strip()
        #self.assertTrue(content.startswith(b'<html>'))#预期回应的html 的开头要是 <html>
        self.assertIn(b'<title>To-Do lists</title>', content)
        self.assertTrue(content.endswith(b'</html>')) 
     
        
    # ---- 测试如果只是浏览首页的时候不需要保存空值到数据库 ----   
    '''
    def test_home_page_only_saves_items_when_nessary(self):
        request = HttpRequest() #模拟客户端发送一个Http请求
        response = home_page(request) #把客户端 http 请求交给 home_page() 来处理
        self.assertEqual(Item.objects.count(), 0) # 断言数据表 lists_item 应该是空的，因为没有提交任何数据
    '''
    # ---- 测试首页能否显示所有的条目 ----
    '''
    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        request = HttpRequest() #模拟客户端发送一个Http请求
        response = home_page(request) #把客户端 http 请求交给 home_page() 来处理
        
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
     '''
        
class ListViewTest(TestCase):
    def test_validation_errors_end_up_on_list_page(self):
        list_ = List.objects.create()  #增加清单
        
        response = self.client.post('/lists/%d/' % (list_.id), data = {'item_text':''})
        
        # 断言站点应该回应 http 200 而不是转跳 http 302 (根据设计，提交后要转跳到个人清单)
        self.assertEqual(response.status_code, 200)
        
        # 断言站点应该继续使用 list.html 模板
        self.assertTemplateUsed(response, 'list.html')
        
        # 断言页面上应该出现错误信息
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
        
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        # 使用http client 连接站点，以post 方式提交一个空的待办事项
        response = self.client.post('/lists/new', data = {'item_text':''})
        
        # 断言站点应该回应 http 200 而不是转跳 http 302 (根据设计，提交后要转跳到个人清单)
        self.assertEqual(response.status_code, 200)
        
        # 断言站点应该回应 home page（因为提交一个空的代办事项是不对的，所以留在首页）
        self.assertTemplateUsed(response, 'home.html')
        
        # 断言页面上应该出现错误信息
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    
    def test_invalid_list_items_arent_saved(self):
        # 使用http client 连接站点，以post 方式提交一个空的待办事项
        response = self.client.post('/lists/new', data = {'item_text':''}) 
        
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
        
        self.client.post('/lists/%d/' % (correct_list.id), data = {'item_text':'A new item for an existing list'})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_to_list_view(self):
        other_llist = List.objects.create()    #增加第一个清单
        correct_list = List.objects.create()  #增加第二个清单
        response = self.client.post('/lists/%d/' % (correct_list.id), data = {'item_text':'A new item for an existing list'})
        
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,)) #断言提交后应该要转跳
        
    

class NewListTest(TestCase):
    # ---- 测试 home_page 视图在 POST 时，是否能返回正确 html 的内容 ----
    def test_page_can_save_a_POST_request(self): 
        self.client.post('/lists/new', data = {'item_text':'A new list item'})
        
        self.assertEqual(Item.objects.count(), 1) # 断言数据表lists_item 中应该已经有 1 笔刚刚提交的数据了
        new_item = Item.objects.first() # 取回数据库中的第一笔
        self.assertEqual(new_item.text, 'A new list item') # 断言在第一笔数据中，数据表 lists_item 的字段-text 的值应该是 'A new list item'
        
    # ---- 测试 POST 时候能否 Redirect （PRG Patten）----
    def test_home_page_redirects_after_POST(self):
        response = self.client.post('/lists/new', data = {'item_text':'A new list item'})

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,)) #断言提交后应该要转跳
'''    
class NewItemTest(TestCase):    
    # ---- 测试能否在一个已经存在的 List 中增加条目 (观察数据库)----
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()    #增加第一个清单
        correct_list = List.objects.create()  #增加第二个清单
        
        self.client.post('/lists/%d/add_item' % (correct_list.id), data = {'item_text':'A new item for an existing list'})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_to_list_view(self):
        other_llist = List.objects.create()    #增加第一个清单
        correct_list = List.objects.create()  #增加第二个清单
        response = self.client.post('/lists/%d/add_item' % (correct_list.id), data = {'item_text':'A new item for an existing list'})
        
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,)) #断言提交后应该要转跳
'''
        
class empty(object):
    pass        
        