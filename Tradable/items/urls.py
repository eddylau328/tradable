from django.urls import path
from items.views import item_list_view, item_create_view, item_dynamic_lookup_view, item_base_view

urlpatterns = [

    path('create/', item_create_view, name='createitem'),
    path('<int:item_id>/', item_dynamic_lookup_view, name='lookupitem'),

]
