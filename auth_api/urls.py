from django.urls import path
from .views import (
    RegisterPenjualView,
    RegisterPembeliView,
    LoginPembeliView,
    LoginPenjualView
)

urlpatterns = [
    path('register/penjual/', RegisterPenjualView.as_view()),
    path('register/pembeli/', RegisterPembeliView.as_view()),
    path('login/penjual/', LoginPenjualView.as_view()),
    path('login/pembeli/', LoginPembeliView.as_view()),
]

from .views_produk import (
    ProdukListView, ProdukDetailView, ProdukTambahView,
    ProdukUpdateView, ProdukDeleteView, ProdukPenjualView
)

urlpatterns += [
    path('produk/', ProdukListView.as_view()),
    path('produk/<int:id>/', ProdukDetailView.as_view()),

    path('produk/tambah/', ProdukTambahView.as_view()),
    path('produk/update/<int:id>/', ProdukUpdateView.as_view()),
    path('produk/delete/<int:id>/', ProdukDeleteView.as_view()),

    path('produk/penjual/<int:id_penjual>/', ProdukPenjualView.as_view()),
]
