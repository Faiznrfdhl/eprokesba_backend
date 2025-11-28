from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from app.models import Pengiriman, Transaksi
from .serializers import PengirimanSerializer


class PengirimanListCreate(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pengiriman = Pengiriman.objects.all()
        serializer = PengirimanSerializer(pengiriman, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data

        # Pastikan transaksi valid
        try:
            transaksi = Transaksi.objects.get(id=data.get("transaksi_id"))
        except Transaksi.DoesNotExist:
            return Response({"error": "Transaksi tidak ditemukan"}, status=404)

        pengiriman_baru = Pengiriman.objects.create(
            transaksi=transaksi,
            alamat=data.get("alamat"),
            ekspedisi=data.get("ekspedisi"),
            resi=data.get("resi", None),
            status="packing"
        )

        serializer = PengirimanSerializer(pengiriman_baru)
        return Response(serializer.data, status=201)


class PengirimanDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pengiriman_id):
        try:
            item = Pengiriman.objects.get(id=pengiriman_id)
        except Pengiriman.DoesNotExist:
            return Response({"error": "Pengiriman tidak ditemukan"}, status=404)

        serializer = PengirimanSerializer(item)
        return Response(serializer.data)

    def delete(self, request, pengiriman_id):
        try:
            item = Pengiriman.objects.get(id=pengiriman_id)
        except Pengiriman.DoesNotExist:
            return Response({"error": "Pengiriman tidak ditemukan"}, status=404)

        item.delete()
        return Response({"message": "Pengiriman berhasil dihapus"}, status=200)
