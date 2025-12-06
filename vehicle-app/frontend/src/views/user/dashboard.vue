<template>
  <div class="container-fluid">

    <!-- Recent Parking History -->
    <h2 class="title">Recent Parking History</h2>

    <table class="table table-striped table-bordered text-center mt-3">
      <thead>
        <tr>
          <th>Id</th>
          <th>Location</th>
          <th>Vehicle Number</th>
          <th>TimeStamp</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="p in user_parking_data" :key="p.reserve_id">
          <td>{{ p.reserve_id }}</td>
          <td>{{ p.location }}</td>
          <td>{{ p.vehicle_number }}</td>
          <td>{{ p.parking_timestamp }}</td>
          <td>
            <button
              v-if="p.status === 'O'"
              class="btn btn-danger"
              @click="releaseSpot(p)"
            >
              Release Out
            </button>

            <button
              v-else
              class="btn btn-success"
              disabled
            >
              Parked Out
            </button>
          </td>
        </tr>

        <tr v-if="user_parking_data.length === 0">
          <td colspan="5">No parking history found</td>
        </tr>
      </tbody>
    </table>

    <hr />

    <!-- Search Parking -->
    <h3 style="font-weight: bold;" class="mt-4">Available Parking Lots</h3>

    <input
      v-model="filterText"
      placeholder="Search Location..."
      class="form-control mb-3"
    />

    <table class="table table-striped table-bordered text-center">
      <thead>
        <tr>
          <th>Id</th>
          <th>Location</th>
          <th>Availability</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="lot in filteredAvailability" :key="lot.lot_id">
          <td>{{ lot.lot_id }}</td>
          <td>{{ lot.location }}</td>
          <td>{{ lot.availability }}</td>
          <td>
            <button
              class="btn btn-success"
              @click="bookSpot(lot)"
            >
              Book
            </button>
          </td>
        </tr>

        <tr v-if="filteredAvailability.length === 0">
          <td colspan="4">No matching locations found</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserDashboard",

  data() {
    return {
      user_parking_data: [],
      availability_data: [],
      filterText: ""
    };
  },

  computed: {
    filteredAvailability() {
      return this.availability_data.filter((lot) =>
        lot.location.toLowerCase().includes(this.filterText.toLowerCase())
      );
    }
  },

  async mounted() {
    await this.loadDashboard();
  },

  methods: {
    async loadDashboard() {
      const res = await axios.get("http://localhost:5000/api/user/dashboard", {
        withCredentials: true
      });

      if (res.data.success) {
        this.user_parking_data = res.data.user_parking_data;
        this.availability_data = res.data.availability_data;
      }
    },

    async releaseSpot(parking) {
    this.$router.push({
        name: "ReleaseSpot",
        params: {
        spot_id: parking.reserve_id,
        vehicle_number: parking.vehicle_number,
        lot_id: parking.lot_id,
        parking_time: parking.parking_timestamp
        }
    });
},

    bookSpot(lot) {
        this.$router.push({
            name: "BookSpot",
            params: {
                lot_id: lot.lot_id,
                location: lot.location
            }
    });
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";
</style>
