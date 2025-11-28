from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from app.models import Chat
from .serializers import ChatSerializer


class KirimChatView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Pesan terkirim", "data": serializer.data}, status=201)
        return Response(serializer.errors, status=400)


class RiwayatChatView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pembeli_id, penjual_id):
        chat = Chat.objects.filter(
            pembeli_id=pembeli_id,
            penjual_id=penjual_id
        ).order_by("waktu")

        serializer = ChatSerializer(chat, many=True)
        return Response(serializer.data)
