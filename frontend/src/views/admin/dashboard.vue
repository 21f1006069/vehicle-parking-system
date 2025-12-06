<template>
  <div class="container mt-4">

    <h2 class="title">Parking Lots</h2>

    <!-- Add Lot Button -->
    <div class="text-center my-4">
      <button class="btn btn-outline-dark" @click="$router.push('/admin/add-lot')">
        + Add Lot
      </button>
    </div>

    <!-- Lots Grid -->
    <div class="d-flex flex-wrap justify-content-evenly">
      <div 
        v-for="lot in lots" 
        :key="lot.lot_id" 
        class="parking_lot"
      >
        <h3>Parking #{{ lot.lot_id }}</h3>
        <h6>{{ lot.location_name }}</h6>

        <div>
          <RouterLink :to="`/admin/edit-lot/${lot.lot_id}`">Edit</RouterLink> |
          <RouterLink :to="`/admin/delete-lot/${lot.lot_id}`">Delete</RouterLink>
        </div>

        <p style="color: green;">
          (Occupied: {{ lot.occupied }} / {{ lot.total }})
        </p>

        <div class="spot">
          <div
            v-for="spot in lot.spots"
            :key="spot.spot_id"
            :class="spot.status === 'O' ? 'occupied' : 'available'"
            @click="goToSpot(lot.lot_id, spot)"
          >
            {{ spot.status }}
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminDashboard",

  data() {
    return {
      lots: []
    };
  },

  async mounted() {
    await this.loadLots();
  },

  methods: {
    async loadLots() {
      try {
        const res = await axios.get("http://localhost:5000/api/admin/dashboard");
        console.log(res.data)
        if (res.data.success) {
          this.lots = res.data.lots;
        }
      } catch (error) {
        console.error("Error loading dashboard:", error);
      }
    },

    goToSpot(lotId, spot) {
      const spotId = spot.spot_id;
      const status = spot.status;
      this.$router.push(`/admin/view-spot/${lotId}/${spotId}/${status}`);
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";


.parking_lot {
  border: 1px solid #dcdcdc;
  padding: 20px;
  width: 260px;
  margin: 20px;
  background: #fff;
  text-align: center;
  border-radius: 12px;
  box-shadow: 0 0 8px rgba(0,0,0,0.1);
}

.spot {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.available, .occupied {
  width: 45px;
  height: 45px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  cursor: pointer;
}

.available {
  background: #dfffd9;
  color: green;
}

.occupied {
  background: #ffdddd;
  color: red;
}
</style>
