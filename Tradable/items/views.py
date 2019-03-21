from django.shortcuts import render

from .models import Item
from .forms import ItemCreateForm


# Create your views here.
def item_detail_view(request):

    #obj = Item.objects.get(id=3)
    #context ={
    #    'object': obj
    #}
    context ={
        'list_of_item': Item.objects.all().values_list('name')
    }

    return render(request, "item_detail.html", context)

def item_create_view(request):

    form = ItemCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        
        #render form after form.save
        form = ItemCreateForm

    context = {
        'form': form
    }

    return render(request, "item_create.html", context)