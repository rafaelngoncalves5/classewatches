from django.urls import path
from . import views

app_name='lojarelogiosapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('user/register', views.register, name='register'),
    path('user/login', views.login, name='login'),
    path('user/logout', views.logout, name='logout'),
]