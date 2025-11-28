from django.db import models

class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nama_admin = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    hak_akses = models.CharField(max_length=50)
    email_admin = models.CharField(max_length=255, default="-")

class Penjual(models.Model):
    id_penjual = models.AutoField(primary_key=True)
    nama_penjual = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    no_telepon = models.CharField(max_length=15)
    alamat_toko = models.TextField()
    status_toko = models.CharField(max_length=50, default="Aktif")

class Pembeli(models.Model):
    id_pembeli = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    alamat = models.TextField()
    no_telepon = models.CharField(max_length=15)

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)
    deskripsi_kategori = models.TextField(blank=True, null=True)

class Produk(models.Model):
    id_produk = models.AutoField(primary_key=True)
    penjual = models.ForeignKey(Penjual, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    nama_produk = models.CharField(max_length=200)
    harga_produk = models.DecimalField(max_digits=12, decimal_places=2)
    stok = models.PositiveIntegerField(default=0)
    deskripsi = models.TextField(null=True, blank=True)

class Keranjang(models.Model):
    id_keranjang = models.AutoField(primary_key=True)
    pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    tanggal_dibuat = models.DateTimeField(auto_now_add=True)

class KeranjangItem(models.Model):
    keranjang = models.ForeignKey(Keranjang, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)


class Transaksi(models.Model):
    id_transaksi = models.AutoField(primary_key=True)
    pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    penjual = models.ForeignKey(Penjual, on_delete=models.CASCADE)
    alamat = models.TextField()
    total_harga = models.DecimalField(max_digits=12, decimal_places=2)
    status_transaksi = models.CharField(max_length=50, default="Pending")
    tanggal = models.DateTimeField(auto_now_add=True)

class TransaksiItem(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.SET_NULL, null=True)
    jumlah = models.PositiveIntegerField(default=1)
    harga_saat_transaksi = models.DecimalField(max_digits=12, decimal_places=2)

class Pembayaran(models.Model):
    transaksi = models.OneToOneField(Transaksi, on_delete=models.CASCADE)
    metode_pembayaran = models.CharField(max_length=100)
    jumlah_pembayaran = models.DecimalField(max_digits=12, decimal_places=2)
    status_pembayaran = models.CharField(max_length=50, default="Belum Dibayar")

class Pengiriman(models.Model):
    transaksi = models.OneToOneField(Transaksi, on_delete=models.CASCADE)
    metode_pengiriman = models.CharField(max_length=100)
    alamat_pembeli = models.TextField()
    no_resi = models.CharField(max_length=100, null=True, blank=True)

class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    penjual = models.ForeignKey(Penjual, on_delete=models.CASCADE)
    pengirim = models.CharField(max_length=10, choices=[("pembeli", "Pembeli"), ("penjual", "Penjual")])
    isi_pesan = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)
    

class Ulasan(models.Model):
    id_ulasan = models.AutoField(primary_key=True)
    pembeli = models.ForeignKey(Pembeli, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)])
    komentar = models.TextField(blank=True, null=True)
    tanggal = models.DateTimeField(auto_now_add=True)

