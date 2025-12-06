<template>
  <div class="container mt-4">

    <h2>Release Parking Spot</h2>

    <div class="card p-4 mt-3">

      <div class="mb-3"><b>Spot ID:</b> {{ form.spot_id }}</div>
      <div class="mb-3"><b>Vehicle Number:</b> {{ form.vehicle_number }}</div>
      <div class="mb-3"><b>Parking Time:</b> {{ form.parking_time }}</div>
      <div class="mb-3"><b>Release Time:</b> {{ form.release_time }}</div>
      <div class="mb-3"><b>Total Cost:</b> ₹ {{ form.total_cost }}</div>

      <button class="btn btn-success" @click="confirmRelease">
        Release Spot
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
  name: "ReleaseSpot",

  data() {
    return {
      form: {
        spot_id: "",
        vehicle_number: "",
        parking_time: "",
        release_time: "",
        total_cost: "",
        lot_id: ""
      }
    };
  },

  async mounted() {
    const { spot_id, vehicle_number, lot_id, parking_time } = this.$route.params;

    const res = await axios.post(
      "http://localhost:5000/api/user/releaseSpot",
      {
        spot_id,
        vehicle_number,
        lot_id,
        parking_time
      },
      { withCredentials: true }
    );

    if (res.data.success) {
      this.form = res.data;
    } else {
      alert(res.data.message);
      this.$router.push("/dashboard");
    }
  },

  methods: {
    async confirmRelease() {
      const res = await axios.post(
        "http://localhost:5000/api/user/confirmRelease",
        {
          spot_id: this.form.spot_id,
          lot_id: this.form.lot_id,
          vehicle_number: this.form.vehicle_number
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
