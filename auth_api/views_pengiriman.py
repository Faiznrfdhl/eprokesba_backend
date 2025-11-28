from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import Pengiriman, Transaksi


# ======================================================
# LIST SEMUA PENGIRIMAN
# ======================================================
class PengirimanListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pengiriman_list = Pengiriman.objects.all()

        result = []
        for p in pengiriman_list:
            result.append({
                "id_transaksi": p.transaksi.id_transaksi,
                "metode_pengiriman": p.metode_pengiriman,
                "alamat_pembeli": p.alamat_pembeli,
                "no_resi": p.no_resi,
            })

        return Response(result, status=200)


# ======================================================
# BUAT PENGIRIMAN
# ======================================================
class PengirimanBuatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_transaksi = request.data.get("id_transaksi")
        metode = request.data.get("metode_pengiriman")
        alamat = request.data.get("alamat_pembeli")

        if not all([id_transaksi, metode, alamat]):
            return Response({"error": "id_transaksi, metode_pengiriman, dan alamat_pembeli wajib diisi"}, status=400)

        transaksi = get_object_or_404(Transaksi, id_transaksi=id_transaksi)

        # Cek apakah sudah ada data pengiriman
        if Pengiriman.objects.filter(transaksi=transaksi).exists():
            return Response({"error": "Pengiriman untuk transaksi ini sudah ada"}, status=400)

        pengiriman = Pengiriman.objects.create(
            transaksi=transaksi,
            metode_pengiriman=metode,
            alamat_pembeli=alamat,
            no_resi=None
        )

        return Response({
            "message": "Pengiriman berhasil dibuat",
            "id_transaksi": transaksi.id_transaksi,
            "metode_pengiriman": pengiriman.metode_pengiriman,
        }, status=201)


# ======================================================
# DETAIL PENGIRIMAN
# ======================================================
class PengirimanDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_transaksi):
        pengiriman = get_object_or_404(Pengiriman, transaksi__id_transaksi=id_transaksi)

        return Response({
            "id_transaksi": pengiriman.transaksi.id_transaksi,
            "pembeli": pengiriman.transaksi.pembeli.nama,
            "penjual": pengiriman.transaksi.penjual.nama_penjual,
            "metode_pengiriman": pengiriman.metode_pengiriman,
            "alamat_pembeli": pengiriman.alamat_pembeli,
            "no_resi": pengiriman.no_resi,
        }, status=200)


# ======================================================
# UPDATE PENGIRIMAN (update metode / alamat / resi)
# ======================================================
class PengirimanUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_transaksi):
        pengiriman = get_object_or_404(Pengiriman, transaksi__id_transaksi=id_transaksi)

        metode = request.data.get("metode_pengiriman")
        alamat = request.data.get("alamat_pembeli")
        resi = request.data.get("no_resi")

        if metode:
            pengiriman.metode_pengiriman = metode
        
        if alamat:
            pengiriman.alamat_pembeli = alamat
        
        if resi:
            pengiriman.no_resi = resi

        pengiriman.save()

        return Response({"message": "Data pengiriman diperbarui"}, status=200)


# ======================================================
# HAPUS PENGIRIMAN
# ======================================================
class PengirimanHapusView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_transaksi):
        pengiriman = get_object_or_404(Pengiriman, transaksi__id_transaksi=id_transaksi)
        pengiriman.delete()

        return Response({"message": "Pengiriman berhasil dihapus"}, status=200)
