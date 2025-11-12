from django.shortcuts import render
from .models import Produk

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def produk(request):
    produks = Produk.objects.all()
    return render(request, 'produk.html', {'produks': produks})

def transaksi(request):
    return render(request, 'transaksi.html')

def laporan(request):
    return render(request, 'laporan.html')

def penjual(request):
    return render(request, 'penjual.html')

def pembeli(request):
    return render(request, 'pembeli.html')