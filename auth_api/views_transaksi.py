from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from app.models import Transaksi, Pembeli, Penjual, Pembayaran, Pengiriman
from .serializers import (TransaksiSerializer,
                            TransaksiCreateSerializer, 
                            UpdateStatusPembayaranSerializer,
                            UpdatePengirimanSerializer,
                            )


class BuatTransaksiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TransaksiCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        id_pembeli = serializer.validated_data['id_pembeli']
        id_penjual = serializer.validated_data['id_penjual']
        alamat = serializer.validated_data['alamat']
        total_harga = serializer.validated_data['total_harga']
        metode = serializer.validated_data['metode_pembayaran']

        # cek pembeli
        try:
            pembeli = Pembeli.objects.get(id=id_pembeli)
        except Pembeli.DoesNotExist:
            return Response({"error": "Pembeli tidak ditemukan"}, status=404)

        # cek penjual
        try:
            penjual = Penjual.objects.get(id_penjual=id_penjual)
        except Penjual.DoesNotExist:
            return Response({"error": "Penjual tidak ditemukan"}, status=404)

        # 1. Buat transaksi
        transaksi = Transaksi.objects.create(
            id_pembeli=pembeli,
            id_penjual=penjual,
            alamat=alamat,
            total_harga=total_harga,
            status_transaksi="Pending"
        )

        # 2. Buat pembayaran otomatis
        pembayaran = Pembayaran.objects.create(
            id_transaksi=transaksi,
            status_pembayaran="Belum Dibayar",
            jumlah_pembayaran=total_harga,
            metode_pembayaran=metode
        )

        return Response({
            "message": "Transaksi berhasil dibuat",
            "id_transaksi": transaksi.id_transaksi,
            "id_pembayaran": pembayaran.id_pembayaran
        }, status=201)

class ListTransaksiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        transaksi = Transaksi.objects.all()
        serializer = TransaksiSerializer(transaksi, many=True)
        return Response(serializer.data)
    
# ================================
# UPDATE STATUS PEMBAYARAN
# ================================
class UpdateStatusPembayaranView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_pembayaran):
        try:
            pembayaran = Pembayaran.objects.get(id_pembayaran=id_pembayaran)
        except Pembayaran.DoesNotExist:
            return Response({"error": "Data pembayaran tidak ditemukan"}, status=404)

        serializer = UpdateStatusPembayaranSerializer(pembayaran, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()

            # =========================================
            #  FIX: Buat pengiriman otomatis
            # =========================================
            if pembayaran.status_pembayaran.lower() == "lunas":

                # Cek apakah sudah ada pengiriman
                sudah_ada = Pengiriman.objects.filter(id_transaksi=pembayaran.id_transaksi).exists()

                if not sudah_ada:
                    Pengiriman.objects.create(
                        id_transaksi=pembayaran.id_transaksi,
                        alamat_pembeli=pembayaran.id_transaksi.alamat,
                        metode_pengiriman="Belum ditentukan",
                        no_resi=""
                    )

            # =========================================

            return Response({"message": "Status pembayaran diperbarui", "data": serializer.data})
        
        return Response(serializer.errors, status=400)


# ================================
# UPDATE STATUS PENGIRIMAN
# ================================
class UpdateStatusPengirimanView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, id):
        # cek transaksi
        try:
            transaksi = Transaksi.objects.get(id_transaksi=id)
        except Transaksi.DoesNotExist:
            return Response({"error": "Transaksi tidak ditemukan"}, status=404)

        # update status transaksi (opsional)
        status_transaksi = request.data.get("status_transaksi")
        if status_transaksi:
            transaksi.status_transaksi = status_transaksi
            transaksi.save()

        # update tabel pengiriman (resi)
        no_resi = request.data.get("no_resi")
        if no_resi:
            pengiriman, created = Pengiriman.objects.get_or_create(
                id_transaksi=transaksi
            )
            pengiriman.no_resi = no_resi
            pengiriman.save()

        return Response({"message": "Status pengiriman berhasil diperbarui"})


