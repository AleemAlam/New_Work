from django.urls import path
from . import views
urlpatterns = [
    path('', views.seller_login, name = "login"),
    path('logout/', views.seller_logout, name = "logout"),
    path('sign_up/', views.seller_sign_up, name = 'signup'),
    path('dashboard/', views.seller_dashboard, name = 'dashboard'),
    path('add_product/', views.seller_add_product, name = 'add_product'),
    path('edit_product/<int:pk>/', views.seller_edit_product, name = 'edit_product'),
    path('delete_product/<int:pk>/', views.seller_delete_product, name = 'delete_product'),
    path('product/<int:pk>/', views.seller_view_product, name = 'view_product'),
]