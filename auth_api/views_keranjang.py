from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from app.models import Keranjang, KeranjangItem, Pembeli, Produk
from .serializers import KeranjangSerializer, KeranjangItemSerializer


# ================================================================
# 1. TAMBAH KERANJANG (satu keranjang per pembeli)
# ================================================================
class KeranjangTambahView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pembeli_id = request.data.get("pembeli_id")

        if not pembeli_id:
            return Response({"error": "pembeli_id wajib diisi"}, status=400)

        try:
            pembeli = Pembeli.objects.get(id=pembeli_id)
        except Pembeli.DoesNotExist:
            return Response({"error": "Pembeli tidak ditemukan"}, status=404)

        # Jika keranjang sudah ada, langsung return
        keranjang, created = Keranjang.objects.get_or_create(pembeli=pembeli)

        serializer = KeranjangSerializer(keranjang)
        return Response(serializer.data, status=201 if created else 200)


# ================================================================
# 2. TAMBAH ITEM KE KERANJANG
# ================================================================
class KeranjangTambahItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        keranjang_id = request.data.get("keranjang_id")
        produk_id = request.data.get("produk_id")
        jumlah = int(request.data.get("jumlah", 1))

        if not keranjang_id or not produk_id:
            return Response({"error": "keranjang_id dan produk_id wajib diisi"}, status=400)

        try:
            keranjang = Keranjang.objects.get(id=keranjang_id)
        except Keranjang.DoesNotExist:
            return Response({"error": "Keranjang tidak ditemukan"}, status=404)

        try:
            produk = Produk.objects.get(id=produk_id)
        except Produk.DoesNotExist:
            return Response({"error": "Produk tidak ditemukan"}, status=404)

        # Cek apakah produk sudah ada di keranjang → update jumlah
        item, created = KeranjangItem.objects.get_or_create(
            keranjang=keranjang,
            produk=produk,
            defaults={"jumlah": jumlah}
        )

        if not created:
            item.jumlah += jumlah
            item.save()

        serializer = KeranjangItemSerializer(item)
        return Response(serializer.data, status=201)


# ================================================================
# 3. LIHAT ISI KERANJANG
# ================================================================
class KeranjangLihatView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pembeli_id):
        try:
            keranjang = Keranjang.objects.get(pembeli_id=pembeli_id)
        except Keranjang.DoesNotExist:
            return Response({"error": "Keranjang tidak ditemukan"}, status=404)

        serializer = KeranjangSerializer(keranjang)
        return Response(serializer.data, status=200)


# ================================================================
# 4. UPDATE JUMLAH ITEM
# ================================================================
class KeranjangUpdateItemView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, item_id):
        jumlah = request.data.get("jumlah")

        if jumlah is None:
            return Response({"error": "jumlah wajib diisi"}, status=400)

        try:
            item = KeranjangItem.objects.get(id=item_id)
        except KeranjangItem.DoesNotExist:
            return Response({"error": "Item tidak ditemukan"}, status=404)

        item.jumlah = jumlah
        item.save()

        serializer = KeranjangItemSerializer(item)
        return Response(serializer.data, status=200)


# ================================================================
# 5. HAPUS ITEM
# ================================================================
class KeranjangHapusItemView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, item_id):
        try:
            item = KeranjangItem.objects.get(id=item_id)
        except KeranjangItem.DoesNotExist:
            return Response({"error": "Item tidak ditemukan"}, status=404)

        item.delete()
        return Response({"message": "Item berhasil dihapus"}, status=200)
