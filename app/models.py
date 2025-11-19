from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nama_admin = models.CharField(max_length=100)
    hak_akses = models.CharField(max_length=50)

class Penjual(models.Model):
    id_penjual = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ✅ OneToOne
    nama_penjual = models.CharField(max_length=100)
    no_telepon = models.CharField(max_length=15)
    status_toko = models.CharField(max_length=50, default="Aktif")
    mengelola_produk = models.TextField(blank=True, null=True)
    alamat_toko = models.TextField()

class Pembeli(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ✅ OneToOne
    alamat = models.TextField()
    no_telepon = models.CharField(max_length=15)
    email = models.EmailField()

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)
    deskripsi_kategori = models.TextField(blank=True, null=True)

class Produk(models.Model):
    id_produk = models.AutoField(primary_key=True)
    id_penjual = models.ForeignKey(Penjual, on_delete=models.CASCADE)
    id_kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    nama_produk = models.CharField(max_length=200)
    harga_produk = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.PositiveIntegerField(default=0)

class Transaksi(models.Model):
    id_transaksi = models.AutoField(primary_key=True)
    id_pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    id_penjual = models.ForeignKey(Penjual, on_delete=models.CASCADE)
    id_pembayaran = models.ForeignKey('Pembayaran', on_delete=models.CASCADE)
    alamat = models.TextField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status_transaksi = models.CharField(max_length=50, default="Pending")

class Pembayaran(models.Model):
    id_pembayaran = models.AutoField(primary_key=True)
    id_transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    status_pembayaran = models.CharField(max_length=50, default="Belum Dibayar")
    jumlah_pembayaran = models.DecimalField(max_digits=10, decimal_places=2)
    metode_pembayaran = models.CharField(max_length=100)

class Pengiriman(models.Model):
    id_pengiriman = models.AutoField(primary_key=True)
    id_transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    alamat_pembeli = models.TextField()
    metode_pengiriman = models.CharField(max_length=100)
    no_resi = models.CharField(max_length=100, blank=True, null=True)

class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    id_pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    id_penjual = models.ForeignKey(Penjual, on_delete=models.CASCADE)
    isi_pesan = models.TextField()
    waktu_pesan = models.DateTimeField(auto_now_add=True)

class Ulasan(models.Model):
    id_ulasan = models.AutoField(primary_key=True)
    id_penjual = models.ForeignKey(Penjual, on_delete=models.CASCADE)
    id_pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    komentar = models.TextField(blank=True, null=True)