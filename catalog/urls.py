from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('profile/',views.ViewProfile,name='view_profile'),
    path('profile/edit/',views.EditProfile,name='edit_profile'),
    path('profile/password/',views.ChangePassword,name='change_password'),
    path('register/',views.Register,name='register'),
    path('items/', views.ItemListView.as_view(), name='items'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('rentors/', views.RentorListView.as_view(), name='rentors'),
    path('rentor/<int:pk>',
         views.RentorDetailView.as_view(), name='rentor-detail'),
]


urlpatterns += [
    path('myitems/', views.LoanedItemsByUserListView.as_view(), name='my-rented'),
]

urlpatterns += [
    path('rentor/create/', views.RentorCreate.as_view(), name='rentor_create'),
    path('rentor/<int:pk>/update/', views.RentorUpdate.as_view(), name='rentor_update'),
    path('rentor/<int:pk>/delete/', views.RentorDelete.as_view(), name='rentor_delete'),
]

urlpatterns += [
    path('item/create/', views.ItemCreate.as_view(), name='item_create'),
    path('item/<int:pk>/update/', views.ItemUpdate.as_view(), name='item_update'),
    path('item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),
    path('item/search/',views.search,name='search'),
]

urlpatterns += [
    path('card/create/', views.CardCreate.as_view(), name='card_create'),
    path('cards/', views.CardByUserListView.as_view(), name = 'card_list'),
    path('card/<int:pk>', views.CardDetailView.as_view(), name = 'card-detail'),
    path('card/<int:pk>/delete/', views.CardDelete.as_view(), name='card_delete'),
]

urlpatterns += [
    path('item/<int:pk>/update/', views.change_status, name='change_status'),
]
