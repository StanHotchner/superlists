from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class List(models.Model):
    def get_absolute_url(self): # 每一个对象实例都有个对应的 url，这个URL 能够从  urls.py 反查，必要时可给出参数
        return reverse('view_list', args=[self.id])
    
class Item(models.Model):
    def __str__(self):
        return self.text
        
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
    
    class Meta:
        ordering = ('id', )
        unique_together = ('list', 'text')

