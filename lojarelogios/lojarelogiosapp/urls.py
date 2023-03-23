from django.urls import path
from . import views

app_name='lojarelogiosapp'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('products', views.products_view, name='products'),
    path('user/', views.index_user_view, name='index_user'),
    path('user/register', views.register_view, name='register'),
    path('user/login', views.login_view, name='login'),
    path('user/logout', views.logout_view, name='logout'),
]