from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from app.models import Kategori


# ============================
# CREATE KATEGORI
# ============================
class KategoriTambahView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        nama = request.data.get("nama_kategori")
        deskripsi = request.data.get("deskripsi_kategori")

        if not nama:
            return Response({"error": "Nama kategori wajib diisi"}, status=400)

        kategori = Kategori.objects.create(
            nama_kategori=nama,
            deskripsi_kategori=deskripsi
        )

        return Response({
            "message": "Kategori berhasil dibuat",
            "id_kategori": kategori.id_kategori
        }, status=201)


# ============================
# LIST SEMUA KATEGORI
# ============================
class KategoriListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = []

        for item in Kategori.objects.all():
            data.append({
                "id_kategori": item.id_kategori,
                "nama_kategori": item.nama_kategori,
                "deskripsi_kategori": item.deskripsi_kategori
            })

        return Response(data, status=200)


# ============================
# DETAIL KATEGORI
# ============================
class KategoriDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_kategori):
        kategori = get_object_or_404(Kategori, id_kategori=id_kategori)

        return Response({
            "id_kategori": kategori.id_kategori,
            "nama_kategori": kategori.nama_kategori,
            "deskripsi_kategori": kategori.deskripsi_kategori
        }, status=200)


# ============================
# UPDATE KATEGORI
# ============================
class KategoriUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_kategori):
        kategori = get_object_or_404(Kategori, id_kategori=id_kategori)

        kategori.nama_kategori = request.data.get("nama_kategori", kategori.nama_kategori)
        kategori.deskripsi_kategori = request.data.get("deskripsi_kategori", kategori.deskripsi_kategori)
        kategori.save()

        return Response({"message": "Kategori berhasil diperbarui"}, status=200)


# ============================
# DELETE KATEGORI
# ============================
class KategoriDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_kategori):
        kategori = get_object_or_404(Kategori, id_kategori=id_kategori)
        kategori.delete()

        return Response({"message": "Kategori berhasil dihapus"}, status=200)
