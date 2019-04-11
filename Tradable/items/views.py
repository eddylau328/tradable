from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Item, DescriptionPhoto
from .forms import ItemCreateForm, ItemEditForm
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
            return redirect('home')

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
            # createItem.seller.image.url = request.user.image.url
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
            return redirect('home')

    else:
        form = ItemCreateForm()
        formset = descriptionPhotoFormset(queryset=DescriptionPhoto.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, "item/create.html", context)


@login_required
def my_item_view(request):
    items = Item.objects.filter(seller=request.user)
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

    if (request.method == 'POST'):
        if (request.POST.get('delete')):
            item_id = request.POST.get('delete')
            deleteItem = Item.objects.get(id=item_id)
            deleteItem.delete()

            messages.success(request, f'You deleted your item')
            return render(request, "item/myitem.html", context)

    return render(request, "item/myitem.html", context)


@login_required
def edit_item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if (item != None):
        itemForm = ItemEditForm(instance=item)
        images = DescriptionPhoto.objects.filter(item__id=item.id)
        descriptionPhotoFormset = modelformset_factory(DescriptionPhoto, fields=('photo',), extra=0)
        newDescriptionPhotoFormset = modelformset_factory(DescriptionPhoto, fields=('photo',), extra=4 - images.count())
        formset = descriptionPhotoFormset(queryset=images, prefix='old')
        newformset = newDescriptionPhotoFormset(queryset=DescriptionPhoto.objects.none(), prefix='new')
        if (request.method == 'POST'):
            if (request.POST.get('save')):
                itemForm = ItemEditForm(request.POST, request.FILES, instance=item)
                formset = descriptionPhotoFormset(request.POST or None, request.FILES or None, queryset=images, prefix='old')
                newformset = newDescriptionPhotoFormset(request.POST or None, request.FILES or None, prefix='new')
                if (itemForm.is_valid() and formset.is_valid() and newformset.is_valid()):
                    itemForm.save()
                    deleteList = []
                    i = 0
                    for f in formset:
                        try:
                            cd = f.cleaned_data
                            if(cd.get('photo') is False):
                                deleteList.append(i)
                            else:
                                f.save()
                            i = i + 1
                        except Exception as e:
                            break

                    for f in newformset:
                        try:
                            newItemPhoto = DescriptionPhoto(item=item, photo=f.cleaned_data['photo'])
                            newItemPhoto.save()
                        except Exception as e:
                            continue

                    print(deleteList)
                    for i in images:
                        print(i.photo.url)
                    for i in deleteList:
                        print(images[i].photo.url)
                        images[i].delete()
                    messages.success(request, f'You have edited your item!')
                    return redirect('myitem')
            else:
                return redirect('myitem')

        if (item.seller == request.user):
            context = {
                'item': item,
                'itemForm': itemForm,
                'formset': formset,
                'newformset': newformset
            }
            return render(request, "item/edit_item.html", context)
        else:
            messages.warning(request, f"There are something wrong!")
            return redirect('home')
