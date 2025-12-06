<template>
  <div class="container mt-4">

    <h2>Add Vehicle</h2>

    <div class="card p-4 mt-3">

      <div class="mb-3">
        <label class="form-label"><b>User ID</b></label>
        <input type="text" class="form-control" :value="user_id" readonly>
      </div>

      <div class="mb-3">
        <label class="form-label"><b>Vehicle Number</b></label>
        <input 
          type="text" 
          class="form-control" 
          v-model="vehicle_number" 
          required
        >
      </div>

      <button class="btn btn-primary" @click="addVehicle">
        Add
      </button>

      <button class="btn btn-secondary ms-2" @click="$router.push('/dashboard')">
        Cancel
      </button>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddVehicle",

  data() {
    return {
      user_id: "",
      vehicle_number: ""
    };
  },

  async mounted() {
    const res = await axios.get(
      "http://localhost:5000/api/user/addVehicle",
      { withCredentials: true }
    );

    if (res.data.success) {
        console.log(res.data.user_id)
      this.user_id = res.data.user_id;
    } else {
      alert("Unable to load user info");
      this.$router.push("/dashboard");
    }
  },

  methods: {
    async addVehicle() {
      if (!this.vehicle_number.trim()) {
        alert("Please enter vehicle number");
        return;
      }

      const res = await axios.post(
        "http://localhost:5000/api/user/addVehicle",
        {
          vehicle_number: this.vehicle_number
        },
        { withCredentials: true }
      );

      alert(res.data.message);

      if (res.data.success) {
        this.$router.push("/dashboard");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";
</style>
