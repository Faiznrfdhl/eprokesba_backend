from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import Keranjang, Produk, Pembeli


# ======================================================
# TAMBAH PRODUK KE KERANJANG
# ======================================================
class KeranjangTambahView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_pembeli = request.data.get("id_pembeli")
        id_produk = request.data.get("id_produk")
        jumlah = request.data.get("jumlah")

        if not all([id_pembeli, id_produk, jumlah]):
            return Response({"error": "id_pembeli, id_produk, dan jumlah wajib diisi"}, status=400)

        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        produk = get_object_or_404(Produk, id_produk=id_produk)

        # apakah produk sudah ada di keranjang?
        keranjang_item, created = Keranjang.objects.get_or_create(
            id_pembeli=pembeli,
            id_produk=produk,
            defaults={"jumlah": jumlah}
        )

        if not created:
            keranjang_item.jumlah += int(jumlah)
            keranjang_item.save()

        return Response({
            "message": "Produk ditambahkan ke keranjang",
            "id_keranjang": keranjang_item.id_keranjang
        }, status=201)


# ======================================================
# LIST KERANJANG PEMBELI
# ======================================================
class KeranjangListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_pembeli):
        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        items = Keranjang.objects.filter(id_pembeli=pembeli)

        output = []
        total_semua = 0

        for i in items:
            subtotal = i.jumlah * i.id_produk.harga_produk
            total_semua += subtotal

            output.append({
                "id_keranjang": i.id_keranjang,
                "id_produk": i.id_produk.id_produk,
                "nama_produk": i.id_produk.nama_produk,
                "harga": i.id_produk.harga_produk,
                "jumlah": i.jumlah,
                "subtotal": subtotal
            })

        return Response({
            "pembeli": pembeli.nama_pembeli,
            "total_semua": total_semua,
            "keranjang": output
        }, status=200)


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
