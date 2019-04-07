from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Item, DescriptionPhoto
from .forms import ItemCreateForm
from django.forms import modelformset_factory
from users.models import Profile


def item_base_view(request, *args, **kwargs):
    return render(request, "item/base.html", {})

# Create your views here.
# item_dynamic_lookup_view render item page for sepcific item


def item_dynamic_lookup_view(request, item_id, *args, **kwargs):
    obj = get_object_or_404(Item, id=item_id)
    photo = DescriptionPhoto.objects.select_related().filter(item=item_id)
    context = {
        "object": obj,
        "photo": photo
    }
    if (request.method == 'POST'):
        if (request.POST.get("seller")):
            if (request.user.is_authenticated):
                if (request.user != obj.seller):
                    request.session['seller'] = f'{obj.seller}'
                    request.session['item_id'] = f'{obj.id}'
                    return redirect("/messages/")
                else:
                    messages.warning(request, "This item belongs to you!")
                    return render(request, "item/lookup.html", context)
            else:
                return redirect(f'/users/login/?next=/items/{obj.id}/')
        elif (request.POST.get("back")):
            print("back")
            return redirect('/items/list/')

    return render(request, "item/lookup.html", context)

# item_list_all_view render a page listing all item


def item_list_view(request):

    items = Item.objects.all()
    search_term = ''

    if 'recent' in request.GET:
        items = items.order_by('createdDateTime')
        items = items.reverse()

    if 'low' in request.GET:
        items = items.order_by('price')

    if 'high' in request.GET:
        items = items.order_by('price')
        items = items.reverse()

    if 'search' in request.GET:
        search_term = request.GET['search']
        items = items.filter(name__icontains=search_term)

    paginator = Paginator(items, 15)  # show 15 items per page

    page = request.GET.get('page')
    items = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    search_string = ''

    context = {'items': items, 'params': params, 'search_term': search_term}

    return render(request, "item/list_item.html", context)

#  item_create_view  remder a page to create item
#  you may also look at .forms.py


@login_required
def item_create_view(request):
    descriptionPhotoFormset = modelformset_factory(DescriptionPhoto, fields=('photo',), extra=4)
    if request.method == 'POST':
        form = ItemCreateForm(request.POST or None, request.FILES or None)
        formset = descriptionPhotoFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            createItem = form.save()
            createItem.seller = request.user
            #createItem.seller.image.url = request.user.image.url
            createItem.save()

            for f in formset:
                try:
                    descriptionPhoto = DescriptionPhoto(item=createItem, photo=f.cleaned_data['photo'])
                    descriptionPhoto.save()
                except Exception as e:
                    break
    #        # render a new form after form.save
    #        form = ItemCreateForm()

            messages.success(request, f'You created a new item')
            return redirect('listitem')

    else:
        form = ItemCreateForm()
        formset = descriptionPhotoFormset(queryset=DescriptionPhoto.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, "item/create.html", context)
