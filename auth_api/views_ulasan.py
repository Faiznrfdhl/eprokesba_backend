# views_ulasan.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from app.models import Ulasan, Produk, Transaksi, Pembeli
from django.shortcuts import get_object_or_404


class UlasanTambahView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_produk = request.data.get("id_produk")
        id_pembeli = request.data.get("id_pembeli")
        rating = request.data.get("rating")
        komentar = request.data.get("komentar")

        # ============================
        # 1. Validasi input
        # ============================
        if not id_produk or not id_pembeli or not rating:
            return Response(
                {"error": "id_produk, id_pembeli, dan rating wajib diisi."},
                status=status.HTTP_400_BAD_REQUEST
            )

        produk = get_object_or_404(Produk, id=id_produk)
        pembeli = get_object_or_404(Pembeli, id=id_pembeli)

        # ============================
        # 2. Cek apakah pembeli pernah beli produk ini
        # ============================
        transaksi = Transaksi.objects.filter(
            pembeli=pembeli,
            produk=produk,
            status_pembayaran="selesai",     # WAJIB selesai
            status_pengiriman="selesai"      # WAJIB sudah diterima
        ).first()

        if not transaksi:
            return Response(
                {"error": "Anda belum menyelesaikan transaksi untuk produk ini. Tidak bisa memberi ulasan."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ============================
        # 3. Cegah spam ulasan (1 transaksi = 1 ulasan)
        # ============================
        sudah_ada = Ulasan.objects.filter(
            produk=produk,
            pembeli=pembeli
        ).exists()

        if sudah_ada:
            return Response(
                {"error": "Anda sudah memberikan ulasan untuk produk ini."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ============================
        # 4. Simpan ulasan
        # ============================
        ulasan = Ulasan.objects.create(
            produk=produk,
            pembeli=pembeli,
            rating=rating,
            komentar=komentar
        )

        return Response(
            {"success": "Ulasan berhasil ditambahkan.", "data": {
                "id": ulasan.id,
                "produk": produk.nama_produk,
                "pembeli": pembeli.nama,
                "rating": rating,
                "komentar": komentar
            }},
            status=status.HTTP_201_CREATED
        )


class UlasanListByProdukView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_produk):
        produk = get_object_or_404(Produk, id=id_produk)
        ulasan_list = Ulasan.objects.filter(produk=produk)

        data = [{
            "id": u.id,
            "pembeli": u.pembeli.nama,
            "rating": u.rating,
            "komentar": u.komentar,
            "tanggal": u.created_at
        } for u in ulasan_list]

        return Response({"produk": produk.nama_produk, "ulasan": data}, status=status.HTTP_200_OK)
# ============================
# UPDATE ULASAN
# ============================
class UlasanUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_ulasan):
        ulasan = get_object_or_404(Ulasan, id=id_ulasan)

        rating = request.data.get("rating")
        komentar = request.data.get("komentar")

        if rating:
            ulasan.rating = rating
        if komentar:
            ulasan.komentar = komentar

        ulasan.save()

        return Response({"success": "Ulasan berhasil diperbarui."}, status=status.HTTP_200_OK)


# ============================
# DELETE ULASAN
# ============================
class UlasanDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_ulasan):
        ulasan = get_object_or_404(Ulasan, id=id_ulasan)
        ulasan.delete()
        return Response({"success": "Ulasan berhasil dihapus."}, status=status.HTTP_200_OK)