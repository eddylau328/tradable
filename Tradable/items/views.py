from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Item, DescriptionPhoto
from .forms import ItemCreateForm, ItemEditForm
from django.forms import modelformset_factory
from users.models import Profile
from django.db.models import Q


def item_base_view(request, *args, **kwargs):
    return render(request, "item/base.html", {})

# Create your views here.
# item_dynamic_lookup_view render item page for sepcific item

# It renders the specific item that is selected by users (registered users or non-registered users).
def item_dynamic_lookup_view(request, item_id, *args, **kwargs):
    # searches the selected item by the item id from the url “items/<int:item_id>/”. If the item is in the database, it gets it out. Otherwise, it will generate a 404 error
    obj = get_object_or_404(Item, id=item_id)
    photo = DescriptionPhoto.objects.select_related().filter(item=item_id)
    context = {
        "object": obj,
        "photo": photo
    }
    if (request.method == 'POST'):
        # When it gets a POST with an id “seller”, it redirects the website to the message page
        if (request.POST.get("seller")):
            # the registered user can buy the item and use the message function, it is needed to validate the user is already login or not
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
        # When it gets a POST with an id “back”, it redirects the website to the home page.
        elif (request.POST.get("back")):
            return redirect('home')

    return render(request, "item/lookup.html", context)

# item_list_all_view render a page listing all item


def item_list_view(request):

    items = Item.objects.filter(isSoldOut=False) #check if item is sold
    search_term = ''

    #sort according to create time and price
    if 'recent' in request.GET:
        # directly get the sorted query set from database
        items = items.order_by('createdDateTime')
        items = items.reverse()
    if 'low' in request.GET:
        # directly get the sorted query set from database
        items = items.order_by('price')
    if 'high' in request.GET:
        # directly get the sorted query set from database
        items = items.order_by('price')
        items = items.reverse()

    #use get method to retrieve the user desired string
    if 'search' in request.GET:
        search_term = request.GET['search']
        # directly get the sorted query set from database
        qlookup = Q(name__icontains=search_term) | Q(price__icontains=search_term) | Q(seller__username__icontains=search_term)
        items = items.filter(qlookup)
        
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

# It lets the registered user to create an item. In this view function
@login_required
def item_create_view(request):
    # The formset saves the description photos which is limited at 4 photos at maximum.
    descriptionPhotoFormset = modelformset_factory(DescriptionPhoto, fields=('photo',), extra=4)
    if request.method == 'POST':
        form = ItemCreateForm(request.POST or None, request.FILES or None)
        formset = descriptionPhotoFormset(request.POST or None, request.FILES or None)
        # they are valid by the model preset validation function. If they are passed, the form will be saved without other process. The formset will be extract out and saved one by one
        if form.is_valid() and formset.is_valid():
            createItem = form.save()
            createItem.seller = request.user
            createItem.save()
            for f in formset:
                try:
                    descriptionPhoto = DescriptionPhoto(item=createItem, photo=f.cleaned_data['photo'])
                    descriptionPhoto.save()
                except Exception as e:
                    break
            # redirect back to the home with a success notification.
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

    page = request.GET.get('page')  # GET method to retrieve user selected page
    items = paginator.get_page(page)  #display the item list of specific page

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

# it provides editing function for the seller to change the data of the item and the description photos
@login_required
def edit_item_view(request, item_id):
    # searches the item from the database. If it cannot be found, 404 error will be generated.
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
                    # deleting the previous description photos first and save the new description photos.
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
                    for i in deleteList:
                        images[i].delete()
                    messages.success(request, f'You have edited your item!')
                    return redirect('myitem')
            else:
                return redirect('myitem')

        if (item.seller == request.user):
            photo = DescriptionPhoto.objects.select_related().filter(item=item_id)
            context = {
                'item': item,
                'photo': photo,
                'itemForm': itemForm,
                'formset': formset,
                'newformset': newformset
            }
            return render(request, "item/edit_item.html", context)
        else:
            messages.warning(request, f"There are something wrong!")
            return redirect('home')
