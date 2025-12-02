from django.utils.timezone import localtime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from app.models import Chat, Pembeli, Penjual

BULAN_INDONESIA = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}

def format_waktu_indonesia(waktu):
    waktu_local = localtime(waktu)
    hari = waktu_local.day
    bulan = BULAN_INDONESIA[waktu_local.month]
    tahun = waktu_local.year
    jam = waktu_local.hour
    menit = waktu_local.minute
    detik = waktu_local.second
    return f"{hari} {bulan} {tahun} {jam:02d}:{menit:02d}"

# ======================================================
# LIST SEMUA CHAT (opsional)
# ======================================================
class ChatListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        chats = Chat.objects.all().order_by("-waktu")

        data = []
        for c in chats:
            data.append({
                "id_chat": c.id_chat,
                "pembeli": c.pembeli.nama,
                "penjual": c.penjual.nama_penjual,
                "pengirim": c.pengirim,
                "pesan": c.isi_pesan,
                "waktu": format_waktu_indonesia(c.waktu)
            })

        return Response(data, status=200)


# ======================================================
# LIST CHAT DARI 1 PEMBELI - PENJUAL
# ======================================================
class ChatByUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_pembeli, id_penjual):
        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        penjual = get_object_or_404(Penjual, id_penjual=id_penjual)

        chats = Chat.objects.filter(
            pembeli=pembeli,
            penjual=penjual
        ).order_by("waktu")

        data = []
        for c in chats:
            data.append({
                "id_chat": c.id_chat,
                "pengirim": c.pengirim,
                "pesan": c.isi_pesan,
                "waktu": format_waktu_indonesia(c.waktu)
            })

        return Response(data, status=200)


# ======================================================
# BUAT / KIRIM PESAN
# ======================================================
class ChatBuatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_pembeli = request.data.get("id_pembeli")
        id_penjual = request.data.get("id_penjual")
        pengirim = request.data.get("pengirim")  # pembeli / penjual
        pesan = request.data.get("isi_pesan")

        if pengirim not in ["pembeli", "penjual"]:
            return Response({"error": "pengirim harus 'pembeli' atau 'penjual'"}, status=400)

        if not all([id_pembeli, id_penjual, pesan]):
            return Response({"error": "id_pembeli, id_penjual, dan isi_pesan wajib diisi"}, status=400)

        pembeli = get_object_or_404(Pembeli, id_pembeli=id_pembeli)
        penjual = get_object_or_404(Penjual, id_penjual=id_penjual)

        chat = Chat.objects.create(
            pembeli=pembeli,
            penjual=penjual,
            pengirim=pengirim,
            isi_pesan=pesan
        )
        

        return Response({
            "message": "Pesan berhasil dikirim",
            "id_chat": chat.id_chat,
            "pengirim": chat.pengirim,
            "pesan": chat.isi_pesan,
            "waktu": chat.waktu,
            "waktu": format_waktu_indonesia(chat.waktu)
        }, status=201)


# ======================================================
# DETAIL CHAT
# ======================================================
class ChatDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_chat):
        chat = get_object_or_404(Chat, id_chat=id_chat)

        return Response({
            "id_chat": chat.id_chat,
            "pembeli": chat.pembeli.nama,
            "penjual": chat.penjual.nama_penjual,
            "pengirim": chat.pengirim,
            "pesan": chat.isi_pesan,
            "waktu": format_waktu_indonesia(chat.waktu),
        }, status=200)


# ======================================================
# HAPUS CHAT
# ======================================================
class ChatHapusView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id_chat):
        chat = get_object_or_404(Chat, id_chat=id_chat)
        chat.delete()

        return Response({"message": "Chat berhasil dihapus"}, status=200)
