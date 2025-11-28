from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import Ulasan, Pembeli, Produk


# ======================================================
# LIST SEMUA ULASAN
# ======================================================
class UlasanListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ulasan_list = Ulasan.objects.all().order_by("-tanggal")

        data = []
        for u in ulasan_list:
            data.append({
                "id_ulasan": u.id_ulasan,
                "pembeli": u.pembeli.nama,
                "produk": u.produk.nama_produk,
                "rating": u.rating,
                "komentar": u.komentar,
                "tanggal": u.tanggal,
            })

        return Response(data, status=200)


# ======================================================
# LIST ULASAN PER PRODUK
# ======================================================
class UlasanListByProdukView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_produk):
        produk = get_object_or_404(Produk, id_produk=id_produk)
        ulasan_list = Ulasan.objects.filter(produk=produk).order_by("-tanggal")

        data = []
        for u in ulasan_list:
            data.append({
                "id_ulasan": u.id_ulasan,
                "pembeli": u.pembeli.nama,
                "rating": u.rating,
                "komentar": u.komentar,
                "tanggal": u.tanggal,
            })

        return Response(data, status=200)


# ======================================================
# BUAT ULASAN
# ======================================================
class UlasanBuatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_pembeli = request.data.get("id_pembeli")
        id_produk = request.data.get("id_produk")
        rating = request.data.get("rating")
        komentar = request.data.get("komentar")

        # Validasi
        if not all([id_pembeli, id_produk, rating]):
            return Response({"error": "id_pembeli, id_produk, dan rating wajib diisi"}, status=400)

        if int(rating) not in [1, 2, 3, 4, 5]:
            return Response({"error": "Rating harus 1-5"}, status=400)

        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        produk = get_object_or_404(Produk, id_produk=id_produk)

        ulasan = Ulasan.objects.create(
            pembeli=pembeli,
            produk=produk,
            rating=rating,
            komentar=komentar,
        )

        return Response({
            "message": "Ulasan berhasil dibuat",
            "id_ulasan": ulasan.id_ulasan
        }, status=201)


# ======================================================
# DETAIL ULASAN
# ======================================================
class UlasanDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_ulasan):
        u = get_object_or_404(Ulasan, id_ulasan=id_ulasan)

        return Response({
            "id_ulasan": u.id_ulasan,
            "pembeli": u.pembeli.nama,
            "produk": u.produk.nama_produk,
            "rating": u.rating,
            "komentar": u.komentar,
            "tanggal": u.tanggal,
        }, status=200)


# ======================================================
# UPDATE ULASAN
# ======================================================
class UlasanUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_ulasan):
        ulasan = get_object_or_404(Ulasan, id_ulasan=id_ulasan)

        rating = request.data.get("rating")
        komentar = request.data.get("komentar")

        if rating:
            if int(rating) not in [1, 2, 3, 4, 5]:
                return Response({"error": "Rating harus 1-5"}, status=400)
            ulasan.rating = rating

        if komentar is not None:
            ulasan.komentar = komentar

        ulasan.save()

        return Response({"message": "Ulasan berhasil diperbarui"}, status=200)


# ======================================================
# HAPUS ULASAN
# ======================================================
class UlasanHapusView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_ulasan):
        ulasan = get_object_or_404(Ulasan, id_ulasan=id_ulasan)
        ulasan.delete()

        return Response({"message": "Ulasan berhasil dihapus"}, status=200)
