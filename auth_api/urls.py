from django.urls import path
#========================================
# AUTHENTIKASI
#========================================
from .views import (
    ListTransaksiView,
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

#========================================
# PRODUK
#========================================
from .views_produk import (
    ProdukListView, ProdukDetailView, ProdukTambahView,
    ProdukUpdateView, ProdukDeleteView, ProdukByPenjualView
)

urlpatterns += [
    path('produk/', ProdukListView.as_view()),
    path('produk/<int:id>/', ProdukDetailView.as_view()),

    path('produk/tambah/', ProdukTambahView.as_view()),
    path('produk/update/<int:id>/', ProdukUpdateView.as_view()),
    path('produk/delete/<int:id>/', ProdukDeleteView.as_view()),

    path('produk/penjual/<int:id_penjual>/', ProdukByPenjualView.as_view()),
]

#========================================
# KATEGORI
#========================================
from .views_kategori import (
    KategoriListView, KategoriTambahView,
    KategoriUpdateView, KategoriDeleteView
)

urlpatterns += [
    path('kategori/', KategoriListView.as_view()),
    path('kategori/tambah/', KategoriTambahView.as_view()),
    path('kategori/update/<int:id>/', KategoriUpdateView.as_view()),
    path('kategori/delete/<int:id>/', KategoriDeleteView.as_view()),
]

#========================================
# TRANSAKSI
#========================================
from .views_transaksi import (
    BuatTransaksiView, ListTransaksiView,
    UpdateStatusPembayaranView, UpdateStatusPengirimanView
)

urlpatterns += [
    path('transaksi/', ListTransaksiView.as_view()),
    path('transaksi/buat/', BuatTransaksiView.as_view()),
    path('pembayaran/<int:id_pembayaran>/update-status/', UpdateStatusPembayaranView.as_view()),
    path('transaksi/<int:id_transaksi>/update-status-pengiriman/', UpdateStatusPengirimanView.as_view()),
]

#========================================
# PENGIRIMAN
#========================================
from .views import UpdatePengirimanView

urlpatterns += [
    path('update-pengiriman/<int:id_pengiriman>/', UpdatePengirimanView.as_view(), name='update_pengiriman'),
]
