from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form' : ItemForm()}) 

def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    error = None
    
    if request.method == 'POST':
        
        try:
            item = Item(list = list_, text = request.POST['text'])
            item.full_clean()
            item.save()
            return redirect(list_)
            
        except:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list' : list_, 'error':error}) 
    
def new_list(request):
    list_ = List.objects.create()
    item = Item(list = list_, text = request.POST['text'])
    
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error' : error})
        
    return redirect(list_)


