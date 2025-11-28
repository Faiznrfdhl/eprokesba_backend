from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import Produk, Penjual, Kategori


# ======================================================
# CREATE PRODUK
# ======================================================
class ProdukTambahView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        nama = request.data.get("nama_produk")
        deskripsi = request.data.get("deskripsi_produk")
        harga = request.data.get("harga_produk")
        stok = request.data.get("stok_produk")
        id_penjual = request.data.get("id_penjual")
        id_kategori = request.data.get("id_kategori")

        if not all([nama, harga, stok, id_penjual, id_kategori]):
            return Response({"error": "Semua field wajib diisi"}, status=400)

        penjual = get_object_or_404(Penjual, id_penjual=id_penjual)
        kategori = get_object_or_404(Kategori, id_kategori=id_kategori)

        produk = Produk.objects.create(
            nama_produk=nama,
            deskripsi_produk=deskripsi,
            harga_produk=harga,
            stok_produk=stok,
            id_penjual=penjual,
            id_kategori=kategori
        )

        return Response({
            "message": "Produk berhasil dibuat",
            "id_produk": produk.id_produk
        }, status=201)


# ======================================================
# LIST SEMUA PRODUK
# ======================================================
class ProdukListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        output = []

        for p in Produk.objects.all():
            output.append({
                "id_produk": p.id_produk,
                "nama_produk": p.nama_produk,
                "deskripsi_produk": p.deskripsi_produk,
                "harga_produk": p.harga_produk,
                "stok_produk": p.stok_produk,
                "id_penjual": p.id_penjual.id_penjual,
                "nama_penjual": p.id_penjual.nama_penjual,
                "id_kategori": p.id_kategori.id_kategori,
                "nama_kategori": p.id_kategori.nama_kategori,
            })

        return Response(output, status=200)


# ======================================================
# LIST PRODUK PER PENJUAL
# ======================================================
class ProdukListByPenjualView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_penjual):
        penjual = get_object_or_404(Penjual, id_penjual=id_penjual)
        produk_list = Produk.objects.filter(id_penjual=penjual)

        output = []
        for p in produk_list:
            output.append({
                "id_produk": p.id_produk,
                "nama_produk": p.nama_produk,
                "harga_produk": p.harga_produk,
                "stok_produk": p.stok_produk,
                "kategori": p.id_kategori.nama_kategori
            })

        return Response(output, status=200)


# ======================================================
# LIST PRODUK BY KATEGORI
# ======================================================
class ProdukListByKategoriView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_kategori):
        kategori = get_object_or_404(Kategori, id_kategori=id_kategori)
        produk_list = Produk.objects.filter(id_kategori=kategori)

        output = []
        for p in produk_list:
            output.append({
                "id_produk": p.id_produk,
                "nama_produk": p.nama_produk,
                "harga_produk": p.harga_produk,
                "stok_produk": p.stok_produk,
                "penjual": p.id_penjual.nama_penjual
            })

        return Response(output, status=200)


# ======================================================
# DETAIL PRODUK
# ======================================================
class ProdukDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_produk):
        p = get_object_or_404(Produk, id_produk=id_produk)

        return Response({
            "id_produk": p.id_produk,
            "nama_produk": p.nama_produk,
            "deskripsi_produk": p.deskripsi_produk,
            "harga_produk": p.harga_produk,
            "stok_produk": p.stok_produk,
            "penjual": p.id_penjual.nama_penjual,
            "kategori": p.id_kategori.nama_kategori
        }, status=200)


# ======================================================
# UPDATE PRODUK
# ======================================================
class ProdukUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_produk):
        produk = get_object_or_404(Produk, id_produk=id_produk)

        produk.nama_produk = request.data.get("nama_produk", produk.nama_produk)
        produk.deskripsi_produk = request.data.get("deskripsi_produk", produk.deskripsi_produk)
        produk.harga_produk = request.data.get("harga_produk", produk.harga_produk)
        produk.stok_produk = request.data.get("stok_produk", produk.stok_produk)

        if request.data.get("id_kategori"):
            kategori = get_object_or_404(Kategori, id_kategori=request.data.get("id_kategori"))
            produk.id_kategori = kategori

        produk.save()

        return Response({"message": "Produk berhasil diperbarui"}, status=200)


# ======================================================
# DELETE PRODUK
# ======================================================
class ProdukDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_produk):
        produk = get_object_or_404(Produk, id_produk=id_produk)
        produk.delete()
        return Response({"message": "Produk berhasil dihapus"}, status=200)
