document.addEventListener('DOMContentLoaded', function() {

  const labels = JSON.parse(document.getElementById("chart-labels").textContent);
  const data = JSON.parse(document.getElementById("chart-data").textContent);

  const ctx = document.getElementById('salesChart');

  new Chart(ctx, {
      type: 'bar',
      data: {
          labels: labels,
          datasets: [{
              label: 'Pendapatan',
              data: data,
              backgroundColor: '#1abc9c'
          }]
      },
      options: {
          responsive: true,
          scales: { y: { beginAtZero: true } }
      }
  });

});
