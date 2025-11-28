from django.urls import path

#==========================
# AUTHENTIKASI
#==========================
from .views import (
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
    ProdukUpdateView, ProdukDeleteView, ProdukListByPenjualView,
    ProdukListByKategoriView
)

#============================
# KATEGORI
#============================
from .views_kategori import (
    KategoriListView, KategoriDetailView, KategoriTambahView,
    KategoriUpdateView, KategoriDeleteView
)

#=============================
# KERANJANG # UPDATE ITEM???
#=============================
from .views_keranjang import (
    KeranjangTambahView,
    KeranjangListView,
    KeranjangUpdateView,
    KeranjangHapusItemView,
    HapusSemuaKeranjangView,
    # KeranjangTambahItem,
    # KeranjangUpdateItemView,
)

#=============================
# TRANSAKSI
#=============================
from .views_transaksi import (
    TransaksiBuatView,
    TransaksiListPembeliView,
    TransaksiDetailView,
    TransaksiUpdateStatusView,
    TransaksiHapusView,
    # TransaksiListView,???????
)

#=============================
# PEMBAYARAN
#=============================
from .views_pembayaran import (
    PembayaranListView,
    PembayaranBuatView,
    PembayaranDetailView,
    PembayaranUpdateStatusView,
    PembayaranHapusView,
)

#==============================
# PENGIRIMAN
#==============================
from .views_pengiriman import (
    PengirimanListView,
    PengirimanBuatView,
    PengirimanDetailView,
    PengirimanUpdateView,
    PengirimanHapusView,
)

#=============================
# ULASAN
#=============================
from .views_ulasan import (
    UlasanListView,
    UlasanBuatView,
    UlasanListByProdukView,
    UlasanDetailView,
    UlasanUpdateView,
    UlasanHapusView,
)

#=============================
# CHAT
#=============================
from .views_chat import (
    ChatListView,
    ChatByUserView,
    ChatBuatView,
    ChatDetailView,
    ChatHapusView,
)

urlpatterns = [
    # AUTH
    path('register/penjual/', RegisterPenjualView.as_view()),
    path('register/pembeli/', RegisterPembeliView.as_view()),
    path('login/penjual/', LoginPenjualView.as_view()),
    path('login/pembeli/', LoginPembeliView.as_view()),

    # PRODUK
    path('produk/', ProdukListView.as_view()),
    path('produk/<int:id>/', ProdukDetailView.as_view()),
    path('produk/tambah/', ProdukTambahView.as_view()),
    path('produk/update/<int:id>/', ProdukUpdateView.as_view()),
    path('produk/delete/<int:id>/', ProdukDeleteView.as_view()),
    path('produk/kategori/<int:id_kategori>/', ProdukListByKategoriView.as_view()),
    path('produk/penjual/<int:id_penjual>/', ProdukListByPenjualView.as_view()),

    # KATEGORI
    path('kategori/', KategoriListView.as_view()),
    path('kategori/tambah/', KategoriTambahView.as_view()),
    path('kategori/<int:id>/', KategoriDetailView.as_view()),
    path('kategori/update/<int:id>/', KategoriUpdateView.as_view()),
    path('kategori/delete/<int:id>/', KategoriDeleteView.as_view()),

    # KERANJANG
    path('keranjang/tambah/', KeranjangTambahView.as_view()),
    path('keranjang/list/<int:id_pembeli>/', KeranjangListView.as_view()),
    path('keranjang/update/<int:id_keranjang>/', KeranjangUpdateView.as_view()),
    path('keranjang/hapus-item/<int:id_keranjang>/', KeranjangHapusItemView.as_view()),
    path('keranjang/hapus-semua/<int:id_pembeli>/', HapusSemuaKeranjangView.as_view()),
    # path('keranjang/item-tambah/', KeranjangTambahItem.as_view()), ??????????????????

    # TRANSAKSI
    path('transaksi/', TransaksiBuatView.as_view()),
    path('transaksi/list/', TransaksiListPembeliView.as_view()),
    path('transaksi/<int:id_transaksi>/', TransaksiDetailView.as_view()),
    path('transaksi/update-status/<int:id_transaksi>/', TransaksiUpdateStatusView.as_view()),
    path('transaksi/hapus/<int:id_transaksi>/', TransaksiHapusView.as_view()),

    # PEMBAYARAN
    path('pembayaran/list/', PembayaranListView.as_view()),
    path('pembayaran/buat/<int:id_transaksi>/', PembayaranBuatView.as_view()),
    path('pembayaran/<int:id_transaksi>/', PembayaranDetailView.as_view()),
    path('pembayaran/update-status/<int:id_transaksi>/', PembayaranUpdateStatusView.as_view()),
    path('pembayaran/hapus/<int:id_transaksi>/', PembayaranHapusView.as_view()),

    # PENGIRIMAN
    path('pengiriman/list/', PengirimanListView.as_view()),
    path('pengiriman/buat/<int:id_transaksi>/', PengirimanBuatView.as_view()),
    path('pengiriman/<int:id_transaksi>/', PengirimanDetailView.as_view()),
    path('pengiriman/update/<int:id_transaksi>/', PengirimanUpdateView.as_view()),
    path('pengiriman/hapus/<int:id_transaksi>/', PengirimanHapusView.as_view()),

    # ULASAN
    path('ulasan/list/', UlasanListView.as_view()),
    path('ulasan/produk/<int:id_produk>/', UlasanListByProdukView.as_view()),
    path('ulasan/buat/', UlasanBuatView.as_view()),
    path('ulasan/<int:id_ulasan>/', UlasanDetailView.as_view()),
    path('ulasan/update/<int:id_ulasan>/', UlasanUpdateView.as_view()),  # ★ TAMBAHAN FIX
    path('ulasan/hapus/<int:id_ulasan>/', UlasanHapusView.as_view()),
    # CHAT
    path('chat/list/', ChatListView.as_view()),
    path('chat/user/<int:id_pembeli>/<int:id_penjual>/', ChatByUserView.as_view()),
    path('chat/buat/', ChatBuatView.as_view()),
    path('chat/detail/<int:id_chat>/', ChatDetailView.as_view()),
    path('chat/hapus/<int:id_chat>/', ChatHapusView.as_view()),
]
