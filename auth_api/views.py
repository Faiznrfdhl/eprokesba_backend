from app.views import pembeli
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from app.models import ( Penjual, Pembeli, Keranjang)
from .serializers import (
    LoginSerializer,
    PembeliRegisterSerializer,
    PenjualRegisterSerializer,
)


# ================================
# REGISTER PENJUAL
# ================================
class RegisterPenjualView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        nama = request.data.get("nama_penjual")
        email = request.data.get("email")
        password = request.data.get("password")
        no_telepon = request.data.get("no_telepon")
        alamat_toko = request.data.get("alamat_toko")
        status_toko = request.data.get("status_toko", "Aktif")

        if Penjual.objects.filter(no_telepon=no_telepon).exists():
            return Response({"error": "No telepon sudah digunakan"}, status=400)

        Penjual.objects.create(
            nama_penjual=nama,
            email=email,
            password=make_password(password),
            no_telepon=no_telepon,
            alamat_toko=alamat_toko,
            status_toko=status_toko
        )
        return Response({"message": "Penjual berhasil registrasi"}, status=201)


# ================================
# REGISTER PEMBELI
# ================================
class RegisterPembeliView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        nama = request.data.get("nama")
        email = request.data.get("email")
        password = request.data.get("password")
        alamat = request.data.get("alamat")
        no_telepon = request.data.get("no_telepon")

        if Pembeli.objects.filter(no_telepon=no_telepon).exists():
            return Response({"error": "No telepon sudah digunakan"}, status=400)

        pembeli = Pembeli.objects.create(
            nama=nama,
            email=email,
            password=make_password(password),
            alamat=alamat,
            no_telepon=no_telepon
        )
        Keranjang.objects.create(pembeli=pembeli)
        return Response({"message": "Pembeli berhasil registrasi"}, status=201)


# ================================
# LOGIN PENJUAL
# ================================
class LoginPenjualView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        no_telepon = serializer.validated_data['no_telepon']
        password = serializer.validated_data['password']

        try:
            penjual = Penjual.objects.get(no_telepon=no_telepon)
            if check_password(password, penjual.password):
                return Response({
                    "message": "Login berhasil sebagai Penjual",
                    "role": "penjual",
                    "nama": penjual.nama_penjual
                })
            return Response({"error": "Password salah"}, status=400)

        except Penjual.DoesNotExist:
            return Response({"error": "Akun penjual tidak ditemukan"}, status=404)


# ================================
# LOGIN PEMBELI
# ================================
class LoginPembeliView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        no_telepon = serializer.validated_data['no_telepon']
        password = serializer.validated_data['password']

        try:
            pembeli = Pembeli.objects.get(no_telepon=no_telepon)
            if check_password(password, pembeli.password):
                return Response({
                    "message": "Login berhasil sebagai Pembeli",
                    "role": "pembeli",
                    "no_telepon": pembeli.no_telepon
                })
            return Response({"error": "Password salah"}, status=400)

        except Pembeli.DoesNotExist:
            return Response({"error": "Akun pembeli tidak ditemukan"}, status=404)
