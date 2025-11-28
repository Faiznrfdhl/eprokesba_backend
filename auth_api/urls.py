from django.urls import path
#==========================
# AUTHENTIKASI
#==========================
from .views import (
    ListTransaksiView,
    RegisterPenjualView,
    RegisterPembeliView,
    LoginPembeliView,
    LoginPenjualView
)
#===========================
# PRODUK
#===========================
from .views_produk import (
    ProdukListView, ProdukDetailView, ProdukTambahView,
    ProdukUpdateView, ProdukDeleteView, ProdukByPenjualView
)
#============================
# KATEGORI
#============================
from .views_kategori import (
    KategoriListView, KategoriTambahView,
    KategoriUpdateView, KategoriDeleteView
)
#=============================
# KERANJANG
#=============================
from .views_keranjang import (
    KeranjangTambahView,
    KeranjangTambahItem,
    KeranjangLihatView,
    KeranjangUpdateItemView,
    KeranjangHapusItemView,
)
#=============================
# TRANSAKSI
#=============================
from .views_transaksi import (
    TransaksiListCreate,
    TransaksiDetail,
)
#=============================
# PEMBAYARAN
#=============================
from .views_pembayaran import (
    DetailPembayaranView,
    UpdateStatusPembayaranView
)
#==============================
# PENGIRIMAN
#==============================
from .views_pengiriman import (
    # PengirimanListView,
    # PengirimanDetailView,
    # UpdateMetodePengirimanView,
    # UpdateNomorResiView,
    # UpdatePengirimanView,
    PengirimanListCreate,
    PengirimanDetail,
)
#=============================
# ULASAN
#=============================
from .views_ulasan import (
    UlasanTambahView,
    UlasanListByProdukView,
    UlasanUpdateView,
    UlasanDeleteView,
)
#=============================
# CHAT
#=============================
from .views_chat import (
    KirimChatView, 
    RiwayatChatView
)

urlpatterns = [
    path('register/penjual/', RegisterPenjualView.as_view()),
    path('register/pembeli/', RegisterPembeliView.as_view()),
    path('login/penjual/', LoginPenjualView.as_view()),
    path('login/pembeli/', LoginPembeliView.as_view()),

    path('produk/', ProdukListView.as_view()),
    path('produk/<int:id>/', ProdukDetailView.as_view()),
    path('produk/tambah/', ProdukTambahView.as_view()),
    path('produk/update/<int:id>/', ProdukUpdateView.as_view()),
    path('produk/delete/<int:id>/', ProdukDeleteView.as_view()),
    path('produk/penjual/<int:id_penjual>/', ProdukByPenjualView.as_view()),

    path('kategori/', KategoriListView.as_view()),
    path('kategori/tambah/', KategoriTambahView.as_view()),
    path('kategori/update/<int:id>/', KategoriUpdateView.as_view()),
    path('kategori/delete/<int:id>/', KategoriDeleteView.as_view()),
    
    path('keranjang/tambah/', KeranjangTambahView.as_view()),
    path('keranjang/item-tambah/', KeranjangTambahItem.as_view()),

    path('transaksi/', TransaksiListCreate.as_view()),
    #error
    path('transaksi/<int:transaksi_id>/', TransaksiDetail.as_view()),
    # path('transaksi/buat/', BuatTransaksiView.as_view()),
    # path('pembayaran/<int:id_pembayaran>/update-status/', UpdateStatusPembayaranView.as_view()),
    
    path('pembayaran/<int:id_transaksi>/', DetailPembayaranView.as_view()),
    #error
    path('pembayaran/update-status/<int:id_transaksi>/', UpdateStatusPembayaranView.as_view()),

    path('pengiriman/', PengirimanListCreate.as_view()),
    path('pengiriman/<int:pengiriman_id>/', PengirimanDetail.as_view()),
    
    path('ulasan/tambah/', UlasanTambahView.as_view()),
    path('ulasan/produk/<int:id_produk>/', UlasanListByProdukView.as_view()),
    path('ulasan/hapus/<int:id_ulasan>/', UlasanDeleteView.as_view()),
    
    path('chat/kirim/', KirimChatView.as_view()),
    path('chat/riwayat/<int:pembeli_id>/<int:penjual_id>/', RiwayatChatView.as_view()),

    # path('pengiriman/', PengirimanListView.as_view()),
    # path('pengiriman/<int:id_transaksi>/', PengirimanDetailView.as_view()),
    # path('pengiriman/update-metode/<int:id_transaksi>/', UpdateMetodePengirimanView.as_view()),
    # path('pengiriman/update-resi/<int:id_transaksi>/', UpdateNomorResiView.as_view()),
    # path('pengiriman/update/<int:id_pengiriman>/', UpdatePengirimanView.as_view()),
]