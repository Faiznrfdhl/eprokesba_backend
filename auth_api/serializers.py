from rest_framework import serializers
from app.models import Penjual, Pembeli


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
