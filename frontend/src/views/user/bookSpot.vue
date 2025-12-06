<template>
  <div class="container mt-4">

    <h2>Book Parking Spot</h2>

    <div class="card p-4 mt-3">

      <div class="mb-3">
        <label class="form-label">Location</label>
        <input type="text" class="form-control" :value="form.location_name" readonly>
      </div>

      <div class="mb-3">
        <label class="form-label">User ID</label>
        <input type="text" class="form-control" :value="form.user_id" readonly>
      </div>

      <div class="mb-3">
        <label class="form-label">Lot ID</label>
        <input type="text" class="form-control" :value="form.lot_id" readonly>
      </div>

      <div class="mb-3">
        <label class="form-label">Spot ID</label>
        <input type="text" class="form-control" :value="form.spot_id" readonly>
      </div>

      <div class="mb-3">
        <label class="form-label">Choose Vehicle</label>
        <select class="form-select" v-model="selectedVehicle">
          <option disabled value="">Select vehicle</option>
          <option v-for="v in form.vehicles" :key="v" :value="v">{{ v }}</option>
        </select>
      </div>

      <button class="btn btn-success" @click="confirmBooking">
        Book
      </button>

      <button class="btn btn-danger ms-2" @click="$router.push('/dashboard')">
        Cancel
      </button>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "BookSpot",

  data() {
    return {
      form: {
        lot_id: "",
        spot_id: "",
        location_name: "",
        user_id: "",
        vehicles: []
      },
      selectedVehicle: ""
    };
  },

  async mounted() {
    const lotId = this.$route.params.lot_id;
    const locationName = this.$route.params.location;

    const res = await axios.post("http://localhost:5000/api/user/bookSpot",
      {
        lot_id: lotId,
        locationName: locationName
      },
      { withCredentials: true }
    );

    if (res.data.success) {
      this.form = res.data;
    } else {
      alert(res.data.success);
      this.$router.push("/dashboard");
    }
  },

  methods: {
    async confirmBooking() {
      if (!this.selectedVehicle) {
        alert("Please select vehicle");
        return;
      }

      const res = await axios.post(
        "http://localhost:5000/api/user/confirmBooking",
        {
          lot_id: this.form.lot_id,
          spot_id: this.form.spot_id,
          user_id: this.form.user_id,
          vehicle_number: this.selectedVehicle,
          locationName: this.form.location_name
        },
        { withCredentials: true }
      );

      alert(res.data.message);
      this.$router.push("/dashboard");
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";
</style>
