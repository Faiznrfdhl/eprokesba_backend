from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import ( Penjual, Pembeli)
from .serializers import (
    LoginSerializer,
    PembeliRegisterSerializer,
    PenjualRegisterSerializer,
    ProdukSerializer,
    KategoriSerializer
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

        if Penjual.objects.filter(email=email).exists():
            return Response({"error": "Email sudah digunakan"}, status=400)

        Penjual.objects.create(
            nama_penjual=nama,
            email=email,
            password=password
        )
        return Response({"message": "Penjual berhasil registrasi"}, status=201)


# ================================
# REGISTER PEMBELI
# ================================
class RegisterPembeliView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if Pembeli.objects.filter(email=email).exists():
            return Response({"error": "Email sudah digunakan"}, status=400)

        Pembeli.objects.create(
            email=email,
            password=password
        )
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

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            penjual = Penjual.objects.get(email=email)
            if penjual.password == password:
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

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            pembeli = Pembeli.objects.get(email=email)
            if pembeli.password == password:
                return Response({
                    "message": "Login berhasil sebagai Pembeli",
                    "role": "pembeli",
                    "email": pembeli.email
                })
            return Response({"error": "Password salah"}, status=400)

        except Pembeli.DoesNotExist:
            return Response({"error": "Akun pembeli tidak ditemukan"}, status=404)
        
        
# ================================
# LIST SEMUA TRANSAKSI (Admin)
# ================================
class ListTransaksiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        transaksi = Transaksi.objects.all()
        serializer = TransaksiSerializer(transaksi, many=True)
        return Response(serializer.data)

# ================================
# UPDATE STATUS PEMBAYARAN
# ================================
class UpdateStatusPengirimanView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, id):
        try:
            transaksi = Transaksi.objects.get(id_transaksi=id)
        except Transaksi.DoesNotExist:
            return Response({"error": "Transaksi tidak ditemukan"}, status=404)

        status_transaksi = request.data.get("status_transaksi", transaksi.status_transaksi)
        resi = request.data.get("resi", transaksi.resi)

        transaksi.status_transaksi = status_transaksi
        transaksi.resi = resi
        transaksi.save()

        # Sinkron ke tabel pengiriman
        from app.models import Pengiriman  # pastikan model import
        Pengiriman.objects.update_or_create(
            transaksi=transaksi,
            defaults={
                "status_pengiriman": status_transaksi,
                "resi": resi
            }
        )

        return Response({"message": "Status pengiriman berhasil diperbarui"})