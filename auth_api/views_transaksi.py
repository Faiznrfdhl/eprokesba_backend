from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from app.models import (
    Transaksi, Pembeli, Penjual, Produk,
    Pembayaran, Pengiriman, TransaksiItem
)
from .serializers import (
    TransaksiSerializer,
    # UpdateStatusPembayaranSerializer,
)

class TransaksiListCreate(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        transaksi = Transaksi.objects.all()
        serializer = TransaksiSerializer(transaksi, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Validasi pembeli
        try:
            pembeli = Pembeli.objects.get(id=data.get("pembeli_id"))
        except Pembeli.DoesNotExist:
            return Response({"error": "Pembeli tidak ditemukan"}, status=404)

        # Validasi produk
        try:
            produk = Produk.objects.get(id=data.get("produk_id"))
        except Produk.DoesNotExist:
            return Response({"error": "Produk tidak ditemukan"}, status=404)

        jumlah = int(data.get("jumlah", 1))
        total_harga = produk.harga_produk * jumlah

        transaksi_baru = Transaksi.objects.create(
            pembeli=pembeli,
            produk=produk,
            jumlah=jumlah,
            total_harga=total_harga,
            status="pending"
        )

        serializer = TransaksiSerializer(transaksi_baru)
        return Response(serializer.data, status=201)


class TransaksiDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, transaksi_id):
        try:
            trx = Transaksi.objects.get(id=transaksi_id)
        except Transaksi.DoesNotExist:
            return Response({"error": "Transaksi tidak ditemukan"}, status=404)

        serializer = TransaksiSerializer(trx)
        return Response(serializer.data)

    def delete(self, request, transaksi_id):
        try:
            trx = Transaksi.objects.get(id=transaksi_id)
        except Transaksi.DoesNotExist:
            return Response({"error": "Transaksi tidak ditemukan"}, status=404)

        trx.delete()
        return Response({"message": "Transaksi berhasil dihapus"}, status=200)
