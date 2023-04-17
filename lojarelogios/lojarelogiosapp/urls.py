from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='lojarelogiosapp'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('privacy', views.privacy_view, name='privacy'),
    path('products', views.products_view, name='products'),
    path('products/<int:pk>/details', views.DetailsView.as_view(), name='details'),
    path('products/<int:id_produto>/add_cart', views.add_cart, name='add_cart'),
    path('products/<int:id_produto>/remove_cart', views.remove_cart, name='remove_cart'),
    path('user/', views.index_user_view, name='index_user'),
    path('user/register', views.register_view, name='register'),
    path('user/login', views.login_view, name='login'),
    path('user/logout', views.logout_view, name='logout'),
    path('user/delete', views.delete_user_view, name='delete_user'),

    # Payment
    # path('payment', login_required(views.payment_view, login_url='/lojarelogiosapp/user/login'), name='payment'),
    path('payment/checkout', login_required(views.checkout_view, login_url='/lojarelogiosapp/user/login'), name='checkout'),
    path('payment/success', login_required(views.success_view, login_url='/lojarelogiosapp/user/login'), name='success'),
    path('payment/cancel', login_required(views.cancel_view, login_url='/lojarelogiosapp/user/login'), name='cancel'),

    # Esqueci minha senha
    path('user/switch-pass', views.switch_password, name='switch_pass'),
]