from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from app.models import Produk, Penjual
from .serializers import ProdukSerializer


# ================================
# LIST SEMUA PRODUK (untuk pembeli)
# ================================
class ProdukListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        kategori = request.GET.get("kategori")
        
        if kategori:
            produk = Produk.objects.filter(id_kategori=kategori)
        else:
            produk = Produk.objects.all()

        serializer = ProdukSerializer(produk, many=True)
        return Response(serializer.data)


# ================================
# DETAIL PRODUK
# ================================
class ProdukDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            produk = Produk.objects.get(id_produk=id)
            serializer = ProdukSerializer(produk)
            return Response(serializer.data)
        except Produk.DoesNotExist:
            return Response({"error": "Produk tidak ditemukan"}, status=404)


# ================================
# TAMBAH PRODUK (Penjual)
# ================================
class ProdukTambahView(APIView):
    def post(self, request):
        serializer = ProdukSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Produk berhasil ditambahkan"})
        return Response(serializer.errors, status=400)


# ================================
# UPDATE PRODUK (Penjual)
# ================================
class ProdukUpdateView(APIView):
    def put(self, request, id):
        try:
            produk = Produk.objects.get(id_produk=id)
        except Produk.DoesNotExist:
            return Response({"error": "Produk tidak ditemukan"}, status=404)

        serializer = ProdukSerializer(produk, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Produk berhasil diupdate"})
        return Response(serializer.errors, status=400)


# ================================
# HAPUS PRODUK (Penjual)
# ================================
class ProdukDeleteView(APIView):
    def delete(self, request, id):
        try:
            produk = Produk.objects.get(id_produk=id)
            produk.delete()
            return Response({"message": "Produk berhasil dihapus"})
        except Produk.DoesNotExist:
            return Response({"error": "Produk tidak ditemukan"}, status=404)


# ================================
# LIST PRODUK MILIK PENJUAL
# ================================
class ProdukPenjualView(APIView):
    def get(self, request, id_penjual):
        produk = Produk.objects.filter(id_penjual=id_penjual)
        serializer = ProdukSerializer(produk, many=True)
        return Response(serializer.data)
