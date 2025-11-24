from rest_framework import serializers
from app.models import (
    Penjual, Pembeli, Produk, 
    Kategori, Transaksi, Pembayaran, 
    Pengiriman,
)

# -------------------------
# REGISTER PENJUAL
# -------------------------
class PenjualRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penjual
        fields = ['email', 'password', 'nama_penjual', 'no_telepon', 'alamat_toko']


# -------------------------
# REGISTER PEMBELI
# -------------------------
class PembeliRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembeli
        fields = ['email', 'password', 'alamat', 'no_telepon']


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

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class TransaksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaksi
        fields = '__all__'

class TransaksiCreateSerializer(serializers.Serializer):
    id_pembeli = serializers.IntegerField()
    id_penjual = serializers.IntegerField()
    alamat = serializers.CharField()
    total_harga = serializers.DecimalField(max_digits=10, decimal_places=2)
    metode_pembayaran = serializers.CharField()

class UpdateStatusPembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = ['status_pembayaran']

class UpdatePengirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengiriman
        fields = ["no_resi"]
