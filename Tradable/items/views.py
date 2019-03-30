from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Item
from .forms import ItemCreateForm
	
def item_base_view(request, *args, **kwargs):
    return render(request, "item/base.html", {})

# Create your views here.
# item_dynamic_lookup_view render item page for sepcific item
def item_dynamic_lookup_view(request, item_id):
    obj = get_object_or_404(Item, id=item_id)
    context = {
        "object": obj
    }
    return render(request, "item/lookup.html", context)

# item_list_all_view render a page listing all item


# def item_list_all_view(request):

    # querysetOfItem = Item.objects.all()
    # context = {
        # 'list_all_item': querysetOfItem
    # }

    # return render(request, "item/list_all.html", context)
def item_list_all_view(request):
	item_list = Item.objects.get_queryset().order_by('id')
	paginator = Paginator(item_list, 15) #show 15 items per page
	
	page = request.GET.get('page')
	items = paginator.get_page(page)
	return render(request, "item/list_all.html", {'items': items})
# item_create_view  remder a page to create item
# you may also look at .forms.py


@login_required
def item_create_view(request):

    form = ItemCreateForm(request.POST or None)

    if form.is_valid(request):
        form.save()
#        # render a new form after form.save
#        form = ItemCreateForm()
        messages.success(request, f'You created a new item')
        return redirect('listallitem')

    context = {
        'form': form
    }

    return render(request, "item/create.html", context)
