from django.urls import path
from . import views

app_name='lojarelogiosapp'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('products', views.products_view, name='products'),
    path('products/<int:pk>/details', views.DetailsView.as_view(), name='details'),
    path('products/<int:id_produto>/add_cart', views.add_cart, name='add_cart'),
    path('products/<int:id_produto>/remove_cart', views.remove_cart, name='remove_cart'),
    path('user/', views.index_user_view, name='index_user'),
    path('user/register', views.register_view, name='register'),
    path('user/login', views.login_view, name='login'),
    path('user/logout', views.logout_view, name='logout'),
]