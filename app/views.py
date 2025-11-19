from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Username atau password salah.'})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def produk(request):
    return render(request, 'produk.html')

@login_required
def transaksi(request):
    return render(request, 'transaksi.html')

@login_required
def laporan(request):
    return render(request, 'laporan.html')

@login_required
def penjual(request):
    return render(request, 'penjual.html')

@login_required
def pembeli(request):
    return render(request, 'pembeli.html')

def logout_view(request):
    logout(request)
    return redirect('login')