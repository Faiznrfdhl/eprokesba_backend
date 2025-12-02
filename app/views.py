from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from app.models import Pembeli, Penjual, Produk, Transaksi, TransaksiItem

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
    total_produk = Produk.objects.count()
    total_penjual = Penjual.objects.count()
    total_pembeli = Pembeli.objects.count()
    total_transaksi = Transaksi.objects.count()

    context = {
        "total_produk": total_produk,
        "total_penjual": total_penjual,
        "total_pembeli": total_pembeli,
        "total_transaksi": total_transaksi,
    }
    return render(request, "dashboard.html", context)

@login_required
def produk(request):
    data = Produk.objects.all()
    return render(request, 'produk.html', {'produk_list': data})

@login_required
def transaksi(request):
    transaksi_qs = Transaksi.objects.all().order_by("id_transaksi")
    transaksi_data = []

    for t in transaksi_qs:
        items = TransaksiItem.objects.filter(transaksi=t)

        produk_list = []
        total_jumlah = 0

        for item in items:
            produk_list.append(f"{item.produk.nama_produk} ({item.jumlah})")
            total_jumlah += item.jumlah

        transaksi_data.append({
            "id": t.id_transaksi,
            "penjual": t.penjual.nama_penjual,
            "pembeli": t.pembeli.nama,
            "produk": ", ".join(produk_list),
            "total_jumlah": total_jumlah,
            "harga": t.total_harga,
            "tanggal": t.tanggal,
            "status": t.status_transaksi,
        })

    return render(request, "transaksi.html", {"transaksi_list": transaksi_data})


@login_required
def laporan(request):
    total_transaksi = Transaksi.objects.count()
    total_penjual = Penjual.objects.count()
    total_pembeli = Pembeli.objects.count()
    total_pendapatan = Transaksi.objects.filter(status_transaksi="Selesai") \
                                        .aggregate(total=Sum("total_harga"))["total"] or 0
                                        
    monthly_sales = (
        Transaksi.objects.filter(status_transaksi="Selesai")
        .annotate(month=TruncMonth("tanggal"))
        .values("month")
        .annotate(total=Sum("total_harga"))
        .order_by("month")
    )

    labels = [m["month"].strftime("%b") for m in monthly_sales]
    data = [m["total"] for m in monthly_sales]

    transaksi_list = []
    for trx in Transaksi.objects.all().order_by("-tanggal"):
        items = TransaksiItem.objects.filter(transaksi=trx)

        produk_list = ", ".join([f"{i.produk.nama_produk} ({i.jumlah})" for i in items])

        transaksi_list.append({
            "id": trx.id_transaksi,
            "pembeli": trx.pembeli.nama,
            "penjual": trx.penjual.nama_penjual,
            "produk": produk_list,
            "total": trx.total_harga,
            "status": trx.status_transaksi,
            "tanggal": trx.tanggal,
        })

    return render(request, "laporan.html", {
        "total_transaksi": total_transaksi,
        "total_penjual": total_penjual,
        "total_pembeli": total_pembeli,
        "total_pendapatan": total_pendapatan,
        "transaksi_list": transaksi_list,
        "chart_labels": labels,
        "chart_data": data,
    })

@login_required
def penjual(request):
    data = Penjual.objects.all()
    return render(request, 'penjual.html', {'penjual_list': data})

@login_required
def pembeli(request):
    data = Pembeli.objects.all()
    return render(request, 'pembeli.html', {'pembeli_list': data})

def logout_view(request):
    logout(request)
    return redirect('login')