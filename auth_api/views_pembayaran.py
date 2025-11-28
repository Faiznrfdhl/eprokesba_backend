from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from app.models import Pembayaran
from .serializers import PembayaranSerializer, UpdateStatusPembayaranSerializer


class DetailPembayaranView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id_transaksi):
        try:
            pembayaran = Pembayaran.objects.get(transaksi_id=id_transaksi)
            serializer = PembayaranSerializer(pembayaran)
            return Response(serializer.data)
        except Pembayaran.DoesNotExist:
            return Response({"error": "Pembayaran tidak ditemukan"}, status=404)


class UpdateStatusPembayaranView(APIView):
    permission_classes = [AllowAny]
    def patch(self, request, id_transaksi):
        try:
            pembayaran = Pembayaran.objects.get(transaksi_id=id_transaksi)
        except Pembayaran.DoesNotExist:
            return Response({"error": "Pembayaran tidak ditemukan"}, status=404)

        serializer = UpdateStatusPembayaranSerializer(pembayaran, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status pembayaran diperbarui"})
        return Response(serializer.errors, status=400)
