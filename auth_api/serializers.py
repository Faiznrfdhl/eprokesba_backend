from rest_framework import serializers
from app.models import (
    Admin, Penjual, Pembeli, Kategori, Produk,
    Keranjang, KeranjangItem, Transaksi, TransaksiItem,
    Pembayaran, Pengiriman, Chat, Ulasan
)

# =========================
#   ADMIN SERIALIZER
# =========================
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

# -------------------------
# REGISTER PENJUAL
# -------------------------
class PenjualRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penjual
        fields = ['nama_penjual', 'email', 'password', 'no_telepon', 'alamat_toko']

    def create(self, validated_data):
        return Penjual.objects.create(**validated_data)

# -------------------------
# REGISTER PEMBELI
# -------------------------
class PembeliRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembeli
        fields = ['nama', 'email', 'password', 'alamat', 'no_telepon']

    def create(self, validated_data):
        return Pembeli.objects.create(**validated_data)


# -------------------------
# LOGIN (UNTUK PEMBELI & PENJUAL)
# -------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
# ------------------------
# PRODUK SERIALIZER 
# ------------------------

class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = '__all__'

# ------------------------
# KATEGORI SERIALIZER  
# ------------------------
class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

# ------------------------
# KERANJANG SERIALIZER
# ------------------------
class KeranjangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keranjang
        fields = '__all__'


class KeranjangItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeranjangItem
        fields = '__all__'


# ------------------------
# TRANSAKSI SERIALIZER
# ------------------------
class TransaksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaksi
        fields = '__all__'

#CREATE TRANSAKSI SERIALIZER
class TransaksiCreateSerializer(serializers.Serializer):
    pembeli = serializers.IntegerField()
    penjual = serializers.IntegerField()
    alamat = serializers.CharField()
    total_harga = serializers.DecimalField(max_digits=12, decimal_places=2)

#ITEM TRANSAKSI SERIALIZER
class TransaksiItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiItem
        fields = '__all__'
        
# ------------------------
# PEMBAYARAN SERIALIZER
# ------------------------
class PembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = '__all__'


class UpdateStatusPembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = ['status_pembayaran']

# ------------------------
# PENGIRIMAN SERIALIZER
# ------------------------
class PengirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengiriman
        fields = '__all__'


class UpdatePengirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengiriman
        fields = ['no_resi']

# ------------------------
# CHAT SERIALIZER
# ------------------------
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

# ------------------------
# ULASAN SERIALIZER
# ------------------------
class UlasanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ulasan
        fields = '__all__'