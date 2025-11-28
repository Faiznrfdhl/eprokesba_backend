from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import (
    Transaksi, TransaksiItem, Pembeli, Penjual,
    Keranjang, KeranjangItem, Produk
)


# ======================================================
# BUAT TRANSAKSI (CHECKOUT)
# ======================================================
class TransaksiBuatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_pembeli = request.data.get("id_pembeli")
        id_penjual = request.data.get("id_penjual")
        alamat = request.data.get("alamat")

        if not all([id_pembeli, id_penjual, alamat]):
            return Response({"error": "id_pembeli, id_penjual, alamat wajib diisi"}, status=400)

        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        penjual = get_object_or_404(Penjual, id_penjual=id_penjual)

        keranjang_items = KeranjangItem.objects.filter(keranjang__pembeli=pembeli)

        if not keranjang_items.exists():
            return Response({"error": "Keranjang kosong, tidak ada yang bisa di-checkout!"}, status=400)

        # Hitung total harga
        total = 0
        for item in keranjang_items:
            total += item.produk.harga_produk * item.jumlah

        # Buat transaksi
        transaksi = Transaksi.objects.create(
            pembeli=pembeli,
            penjual=penjual,
            alamat=alamat,
            total_harga=total,
            status_transaksi="Pending"
        )

        # Buat TransaksiItem
        for item in keranjang_items:
            TransaksiItem.objects.create(
                transaksi=transaksi,
                produk=item.produk,
                jumlah=item.jumlah,
                harga_saat_transaksi=item.produk.harga_produk
            )

        # Kosongkan keranjang
        KeranjangItem.objects.filter(keranjang__pembeli=pembeli).delete()

        return Response({
            "message": "Transaksi berhasil dibuat",
            "id_transaksi": transaksi.id_transaksi,
            "total": total
        }, status=201)


# ======================================================
# LIST TRANSAKSI PEMBELI
# ======================================================
class TransaksiListPembeliView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_pembeli):
        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        list_transaksi = Transaksi.objects.filter(pembeli=pembeli)

        result = []
        for t in list_transaksi:
            result.append({
                "id_transaksi": t.id_transaksi,
                "penjual": t.penjual.nama_penjual,
                "total_harga": t.total_harga,
                "status": t.status_transaksi,
                "tanggal": t.tanggal
            })

        return Response(result, status=200)


# ======================================================
# DETAIL TRANSAKSI
# ======================================================
class TransaksiDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_transaksi):
        transaksi = get_object_or_404(Transaksi, id_transaksi=id_transaksi)
        items = TransaksiItem.objects.filter(transaksi=transaksi)

        detail_items = []
        for i in items:
            detail_items.append({
                "produk": i.produk.nama_produk if i.produk else "Produk terhapus",
                "jumlah": i.jumlah,
                "harga_saat_transaksi": i.harga_saat_transaksi
            })

        return Response({
            "id_transaksi": transaksi.id_transaksi,
            "pembeli": transaksi.pembeli.nama,
            "penjual": transaksi.penjual.nama_penjual,
            "alamat": transaksi.alamat,
            "total_harga": transaksi.total_harga,
            "status_transaksi": transaksi.status_transaksi,
            "items": detail_items,
            "tanggal": transaksi.tanggal
        }, status=200)


# ======================================================
# UPDATE STATUS TRANSAKSI
# ======================================================
class TransaksiUpdateStatusView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, id_transaksi):
        transaksi = get_object_or_404(Transaksi, id_transaksi=id_transaksi)
        status_baru = request.data.get("status")

        if not status_baru:
            return Response({"error": "status diperlukan"}, status=400)

        transaksi.status_transaksi = status_baru
        transaksi.save()

        return Response({"message": "Status transaksi diperbarui"}, status=200)


# ======================================================
# HAPUS TRANSAKSI
# ======================================================
class TransaksiHapusView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_transaksi):
        transaksi = get_object_or_404(Transaksi, id_transaksi=id_transaksi)
        transaksi.delete()

        return Response({"message": "Transaksi dihapus"}, status=200)
