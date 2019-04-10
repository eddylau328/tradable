from django.urls import path
from items.views import item_list_view, item_create_view, item_dynamic_lookup_view, item_base_view, my_item_view, edit_item_view

urlpatterns = [

    path('create/', item_create_view, name='createitem'),
    path('<int:item_id>/', item_dynamic_lookup_view, name='lookupitem'),
    path('myitem/', my_item_view, name='myitem'),
    path('edit/<int:item_id>/', edit_item_view, name='edititem'),
]
