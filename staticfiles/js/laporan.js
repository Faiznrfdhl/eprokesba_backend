// ChartJS + Filter (opsional: bisa di-load hanya di laporan.html)
document.addEventListener('DOMContentLoaded', function() {
  const ctx = document.getElementById('salesChart');
  if (ctx) {
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt'],
        datasets: [{
          label: 'Penjualan (Rp)',
          data: [40000000, 35000000, 50000000, 65000000, 70000000, 55000000, 80000000, 78000000, 72000000, 90000000],
          backgroundColor: '#1abc9c'
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }
});