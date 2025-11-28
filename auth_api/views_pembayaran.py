from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import Pembayaran, Transaksi


# ======================================================
# LIST SEMUA PEMBAYARAN
# ======================================================
class PembayaranListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pembayaran_list = Pembayaran.objects.all()

        result = []
        for p in pembayaran_list:
            result.append({
                "id_transaksi": p.transaksi.id_transaksi,
                "metode_pembayaran": p.metode_pembayaran,
                "jumlah_pembayaran": p.jumlah_pembayaran,
                "status_pembayaran": p.status_pembayaran,
            })

        return Response(result, status=200)


# ======================================================
# BUAT PEMBAYARAN
# ======================================================
class PembayaranBuatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_transaksi = request.data.get("id_transaksi")
        metode = request.data.get("metode_pembayaran")
        jumlah = request.data.get("jumlah_pembayaran")

        if not all([id_transaksi, metode, jumlah]):
            return Response({"error": "id_transaksi, metode_pembayaran dan jumlah_pembayaran wajib diisi"}, status=400)

        transaksi = get_object_or_404(Transaksi, id_transaksi=id_transaksi)

        # Cek apakah sudah ada pembayaran
        if Pembayaran.objects.filter(transaksi=transaksi).exists():
            return Response({"error": "Pembayaran untuk transaksi ini sudah ada"}, status=400)

        pembayaran = Pembayaran.objects.create(
            transaksi=transaksi,
            metode_pembayaran=metode,
            jumlah_pembayaran=jumlah,
            status_pembayaran="Belum Dibayar"
        )

        return Response({
            "message": "Pembayaran berhasil dibuat",
            "id_transaksi": transaksi.id_transaksi,
            "jumlah_pembayaran": pembayaran.jumlah_pembayaran,
            "metode_pembayaran": pembayaran.metode_pembayaran
        }, status=201)


# ======================================================
# DETAIL PEMBAYARAN
# ======================================================
class PembayaranDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_transaksi):
        pembayaran = get_object_or_404(Pembayaran, transaksi__id_transaksi=id_transaksi)

        return Response({
            "id_transaksi": pembayaran.transaksi.id_transaksi,
            "pembeli": pembayaran.transaksi.pembeli.nama,
            "penjual": pembayaran.transaksi.penjual.nama_penjual,
            "total_harga": pembayaran.transaksi.total_harga,
            "metode_pembayaran": pembayaran.metode_pembayaran,
            "jumlah_pembayaran": pembayaran.jumlah_pembayaran,
            "status_pembayaran": pembayaran.status_pembayaran,
        }, status=200)


# ======================================================
# UPDATE STATUS PEMBAYARAN
# ======================================================
class PembayaranUpdateStatusView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_transaksi):
        pembayaran = get_object_or_404(Pembayaran, transaksi__id_transaksi=id_transaksi)
        status_baru = request.data.get("status_pembayaran")

        if not status_baru:
            return Response({"error": "status_pembayaran wajib diisi"}, status=400)

        pembayaran.status_pembayaran = status_baru
        pembayaran.save()

        return Response({"message": "Status pembayaran diperbarui"}, status=200)


# ======================================================
# HAPUS PEMBAYARAN
# ======================================================
class PembayaranHapusView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_transaksi):
        pembayaran = get_object_or_404(Pembayaran, transaksi__id_transaksi=id_transaksi)
        pembayaran.delete()

        return Response({"message": "Pembayaran dihapus"}, status=200)
