from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

class ListAndItemModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))
        
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create() # 创建一个待办事项清单，取回 id 号 / create() == 先创建一笔数据的实例，然后再调用 .save()
        item = Item(list = list_, text = '') # 创建一笔空字符的待办事项
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    # ---- 测试能否正确的保存数据到数据库并且读回 ----
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        # 创建第一个条目并保存
        first_item = Item()
        first_item.text = 'The first(ever) list item'
        first_item.list = list_
        first_item.save()
        
        # 创建第二个条目并保存
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2) #已经保存的条目应该要有2个
        
        first_saved_item = saved_items[0] # 从已经被保存的条目集中取出第1个
        second_saved_item = saved_items[1] # 从已经被保存的条目集中取出第2个
        self.assertEqual(first_saved_item.text, 'The first(ever) list item') #断言第 1 笔条目的字符应该是...
        self.assertEqual(first_saved_item.list, list_) #断言已保存的第 1 笔条目所属的 list 应该要与前面创建的一致
        self.assertEqual(second_saved_item.text, 'Item the second') #断言第 2 笔条目的字符应该是...
        self.assertEqual(second_saved_item.list, list_) #断言已保存的第 1 笔条目所属的 list 应该要与前面创建的一致