from django.urls import path
from . import views

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


]