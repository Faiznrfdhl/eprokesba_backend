from django.urls import path
from . import views, api_views

urlpatterns = [
    # Web
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('produk/', views.produk, name='produk'),
    path('transaksi/', views.transaksi, name='transaksi'),
    path('laporan/', views.laporan, name='laporan'),
    path('penjual/', views.penjual, name='penjual'),
    path('pembeli/', views.pembeli, name='pembeli'),

    # API (untuk mobile)
    path('api/login/', api_views.api_login, name='api-login'),
    path('api/register/', api_views.api_register, name='api-register'),
]