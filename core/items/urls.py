from django.urls import path
from .views import ItemListCreateView, ItemRetrieveUpdateDestroyView

urlpatterns = [
    path('items', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:item_id>', ItemRetrieveUpdateDestroyView.as_view(), name='item-detail-update-delete')
]