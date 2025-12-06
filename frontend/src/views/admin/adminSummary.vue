<template>
  <div class="container mt-4">

    <h2 class="mb-4">Parking Summary</h2>

    <!-- Top summary cards -->
    <div class="row mb-4">

      <div class="col-md-6 mb-3">
        <div class="card p-3 text-center shadow-sm">
          <h5>Total Parking Lots</h5>
          <h3>{{ summary.total_lots }}</h3>
        </div>
      </div>

      <div class="col-md-6 mb-3">
        <div class="card p-3 text-center shadow-sm">
          <h5>Total Parking Spots</h5>
          <h3>{{ summary.total_spots }}</h3>
        </div>
      </div>

    </div>

    <div class="row">
      <!-- Pie Chart -->
      <div class="col-md-6 mb-3">
        <canvas id="statusChart"></canvas>
      </div>

      <!-- Bar Chart -->
      <div class="col-md-6 mb-3">
        <canvas id="lotChart"></canvas>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  name: "AdminSummary",

  data() {
    return {
      summary: {
        total_lots: 0,
        total_spots: 0,
        status_summary: {},
        lot_spot_data: []
      },

      charts: {
        status: null,
        lots: null
      }
    };
  },

  async mounted() {
    await this.loadSummary();
    this.renderCharts();
  },

  methods: {
    async loadSummary() {
      try {
        const res = await axios.get("http://localhost:5000/api/admin/summary");

        if (res.data.success) {
          this.summary = res.data;
        }

      } catch (err) {
        console.error(err);
        alert("Failed to load summary data");
      }
    },

    renderCharts() {
      // Destroy previous charts before re-rendering
      if (this.charts.status) this.charts.status.destroy();
      if (this.charts.lots) this.charts.lots.destroy();

      const statusLabels = Object.keys(this.summary.status_summary);
      const statusData = Object.values(this.summary.status_summary);

      const lotLabels = this.summary.lot_spot_data.map(item => item[0]);
      const lotData = this.summary.lot_spot_data.map(item => item[1]);

      // Status Pie Chart
      const statusCtx = document.getElementById("statusChart");
      this.charts.status = new Chart(statusCtx, {
        type: "pie",
        data: {
          labels: statusLabels,
          datasets: [
            {
              data: statusData,
              backgroundColor: ["#28a745", "#dc3545"]
            }
          ]
        }
      });

      // Spots Per Lot Bar Chart
      const lotCtx = document.getElementById("lotChart");
      this.charts.lots = new Chart(lotCtx, {
        type: "bar",
        data: {
          labels: lotLabels,
          datasets: [
            {
              label: "Spots per Lot",
              data: lotData,
              backgroundColor: "#007bff"
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";
</style>
