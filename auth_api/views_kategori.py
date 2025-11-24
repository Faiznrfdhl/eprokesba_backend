from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from app.models import Kategori
from .serializers import KategoriSerializer


# =========================================
# LIST SEMUA KATEGORI (untuk pembeli/penjual)
# =========================================
class KategoriListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        kategori = Kategori.objects.all()
        serializer = KategoriSerializer(kategori, many=True)
        return Response(serializer.data)


# =========================================
# TAMBAH KATEGORI (Admin)
# =========================================
class KategoriTambahView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = KategoriSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kategori berhasil dibuat"}, status=201)
        return Response(serializer.errors, status=400)


# =========================================
# UPDATE KATEGORI (Admin)
# =========================================
class KategoriUpdateView(APIView):
    permission_classes = [AllowAny]
    
    def put(self, request, id):
        try:
            kategori = Kategori.objects.get(id_kategori=id)
        except Kategori.DoesNotExist:
            return Response({"error": "Kategori tidak ditemukan"}, status=404)

        serializer = KategoriSerializer(kategori, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kategori berhasil diupdate"})
        return Response(serializer.errors, status=400)


# =========================================
# HAPUS KATEGORI (Admin)
# =========================================
class KategoriDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id):
        try:
            kategori = Kategori.objects.get(id_kategori=id)
            kategori.delete()
            return Response({"message": "Kategori berhasil dihapus"})
        except Kategori.DoesNotExist:
            return Response({"error": "Kategori tidak ditemukan"}, status=404)
