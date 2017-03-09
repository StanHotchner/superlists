from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))

        
class ItemModelTest(TestCase):
        
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create() # 创建一个待办事项清单，取回 id 号 / create() == 先创建一笔数据的实例，然后再调用 .save()
        item = Item(list = list_, text = '') # 创建一笔空字符的待办事项
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
            
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')
        
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list = list_, text = 'abc123')

        self.assertIn(item, list_.item_set.all())
             
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list = list_, text = 'abcdefg')
        
        with self.assertRaises(ValidationError):
            item = Item(list = list_, text = 'abcdefg')
            item.full_clean()
            #item.save()
            
    def test_CAN_save_same_item_to_different_lists(self):
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        
        Item.objects.create(list = list_1, text = 'abcdefg')
        
        
        item = Item(list = list_2, text = 'abcdefg')
        item.full_clean()
        
    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list = list1, text = 'abc01')
        item2 = Item.objects.create(list = list1, text = 'abc02')
        item3 = Item.objects.create(list = list1, text = 'abc03')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])
        
    def test_string_representation(self):
        item = Item(text = 'abc01')
        self.assertEqual(str(item), 'abc01')
        
        
        
        