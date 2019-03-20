from django.shortcuts import render

from .models import Item
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