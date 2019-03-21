from django.shortcuts import render, get_object_or_404

from .models import Item
from .forms import ItemCreateForm


# Create your views here.
#item_dynamic_lookup_view render item page for sepcific item 
def item_dynamic_lookup_view(request, item_id):
    obj = get_object_or_404(Item, id= item_id)
    context = {
        "object": obj
    }
    return render(request, "item_lookup.html", context)

# item_list_all_view render a page listing all item 
def item_list_all_view(request):

    querysetOfItem = Item.objects.all()
    context ={
        'list_all_item': querysetOfItem
    }

    return render(request, "item_list_all.html", context)

# item_create_view  remder a page to create item 
# you may also look at .forms.py
def item_create_view(request):

    form = ItemCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        
        #render a new form after form.save
        form = ItemCreateForm

    context = {
        'form': form
    }

    return render(request, "item_create.html", context)