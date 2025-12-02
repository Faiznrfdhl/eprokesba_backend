from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import Keranjang, Produk, Pembeli, KeranjangItem

# ======================================================
# TAMBAH PRODUK KE KERANJANG
# ======================================================
class KeranjangTambahItemView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id_pembeli):
        produk_id = request.data.get("produk_id")
        jumlah = request.data.get("jumlah", 1)

        # validasi keranjang hanya milik pembeli tersebut
        keranjang = Keranjang.objects.filter(pembeli_id=id_pembeli).first()
        if not keranjang:
            return Response({"error": "Keranjang tidak ditemukan"}, status=404)

        # ambil produk
        try:
            produk = Produk.objects.get(id_produk=produk_id)
        except Produk.DoesNotExist:
            return Response({"error": "Produk tidak ditemukan"}, status=404)

        # cek apakah item sudah ada
        item, created = KeranjangItem.objects.get_or_create(
            keranjang=keranjang,
            produk=produk
        )

        if not created:
            item.jumlah += int(jumlah)
        else:
            item.jumlah = int(jumlah)

        item.save()

        return Response({"message": "Produk ditambahkan ke keranjang", "keranjang_id": keranjang.id_keranjang})


# ======================================================
# LIST KERANJANG PEMBELI
# ======================================================
class KeranjangListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pembeli_id):

        try:
            keranjang = Keranjang.objects.get(pembeli_id=pembeli_id)
        except Keranjang.DoesNotExist:
            return Response({"detail": "Keranjang tidak ditemukan"}, status=404)

        data = {
            "id_keranjang": keranjang.id_keranjang,
            "pembeli_id": keranjang.pembeli_id,
            "tanggal_dibuat": keranjang.tanggal_dibuat
        }

        return Response(data, status=200)

class KeranjangItemView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, keranjang_id):
        items = KeranjangItem.objects.filter(keranjang_id=keranjang_id)
        
        data = []
        for item in items:
            data.append({
                "produk_id": item.produk_id,
                "jumlah": item.jumlah,
                "nama_produk": item.produk.nama_produk,
                "harga": item.produk.harga_produk
            })
        
        return Response(data, status=200)

    def post(self, request, keranjang_id):
        produk_id = request.data.get("produk_id")
        jumlah = request.data.get("jumlah", 1)

        KeranjangItem.objects.create(
            keranjang_id=keranjang_id,
            produk_id=produk_id,
            jumlah=jumlah
        )

        return Response({"message": "Produk dimasukkan ke keranjang"}, status=201)

# ======================================================
# UPDATE JUMLAH PRODUK DALAM KERANJANG
# ======================================================
class KeranjangUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_keranjang):
        keranjang = get_object_or_404(Keranjang, id_keranjang=id_keranjang)
        
        jumlah_baru = request.data.get("jumlah")
        if not jumlah_baru:
            return Response({"error": "jumlah wajib diisi"}, status=400)

        keranjang.jumlah = jumlah_baru
        keranjang.save()

        return Response({"message": "Jumlah keranjang diperbarui"}, status=200)


# ======================================================
# HAPUS PRODUK DARI KERANJANG
# ======================================================
class KeranjangHapusItemView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_keranjang):
        keranjang = get_object_or_404(Keranjang, id_keranjang=id_keranjang)
        keranjang.delete()

        return Response({"message": "Produk dihapus dari keranjang"}, status=200)


# ======================================================
# HAPUS SEMUA KERANJANG PEMBELI
# ======================================================
class HapusSemuaKeranjangView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_pembeli):
        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        Keranjang.objects.filter(id_pembeli=pembeli).delete()

        return Response({"message": "Seluruh keranjang pembeli dihapus"}, status=200)
