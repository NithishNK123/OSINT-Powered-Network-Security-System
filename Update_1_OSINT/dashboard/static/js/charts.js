/* =====================================================
   charts.js
   SOC / SIEM Dashboard Charts
   Uses Chart.js (v4+)
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

  // Fetch data from global window object injected by Flask
  const dashboardData = window.DASHBOARD_DATA || {
    status: [0, 0, 0, 0],
    timeline_labels: ["None"],
    timeline_values: [0]
  };

  /* ===============================
     GLOBAL CHART DEFAULTS
  ================================ */
  if (typeof Chart !== 'undefined') {
    Chart.defaults.color = "#9aa4bf";
    Chart.defaults.font.family = "Segoe UI, system-ui, sans-serif";
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
  }

  /* =====================================================
     ISSUES BY STATUS (DONUT)
  ===================================================== */
  const issuesStatusCanvas = document.getElementById("statusChart");

  if (issuesStatusCanvas) {
    new Chart(issuesStatusCanvas, {
      type: "doughnut",
      data: {
        labels: ["Low", "Medium", "High", "Critical"],
        datasets: [{
          data: dashboardData.status,
          backgroundColor: [
            "#2ecc71",
            "#f1c40f",
            "#e67e22",
            "#e74c3c"
          ],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "72%",
        plugins: {
          legend: {
            position: "bottom"
          },
          tooltip: {
            backgroundColor: "#0f172a"
          }
        }
      }
    });
  }


  /* =====================================================
     HOSTS BY COUNTRY (BAR)
  ===================================================== */
  const hostsCountryCanvas = document.getElementById("countryChart");

  if (hostsCountryCanvas) {
    new Chart(hostsCountryCanvas, {
      type: "bar",
      data: {
        labels: ["US", "CN", "RU", "IN", "DE", "BR"],
        datasets: [{
          label: "Hosts",
          data: [0, 0, 0, 0, 0, 0], // Keep static for now or use placeholders
          backgroundColor: "#4da3ff",
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { display: false }
          },
          y: {
            beginAtZero: true,
            grid: { color: "#1f2a44" }
          }
        }
      }
    });
  }


  /* =====================================================
     ABUSE SCORE TIMELINE (LINE)
  ===================================================== */
  const severityLineCanvas = document.getElementById("severityChart");

  if (severityLineCanvas) {
    new Chart(severityLineCanvas, {
      type: "line",
      data: {
        labels: dashboardData.timeline_labels,
        datasets: [
          {
            label: "Abuse Score",
            data: dashboardData.timeline_values,
            borderColor: "#4da3ff",
            backgroundColor: "rgba(77,163,255,0.15)",
            tension: 0.4,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom"
          }
        },
        scales: {
          x: {
            grid: { color: "#1f2a44" }
          },
          y: {
            beginAtZero: true,
            max: 100,
            grid: { color: "#1f2a44" }
          }
        }
      }
    });
  }


  /* =====================================================
     CONSOLE CONFIRMATION
  ===================================================== */
  console.log("📊 Charts loaded successfully with live data");

});
