<template>
  <div class="container mt-4">

    <h2 class="title">Add New Parking Lot</h2>

    <div class="d-flex justify-content-center mt-4">
      <form @submit.prevent="addLot" 
            class="border p-4 bg-white rounded shadow" 
            style="width: 700px;">

        <div class="mb-3">
          <label>Location Name</label>
          <input v-model="form.locationName" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Address</label>
          <input v-model="form.address" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Pincode</label>
          <input v-model="form.pincode" type="number" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Price Per Hour</label>
          <input v-model="form.pricePerHour" type="number" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Maximum Spots</label>
          <input v-model="form.maxSpots" type="number" class="form-control" required>
        </div>

        <button class="btn btn-primary" type="submit">Add Lot</button>
        <button class="btn btn-secondary ms-2" type="button"
                @click="$router.push('/admin/dashboard')">
          Cancel
        </button>

      </form>
    </div>

  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "AddLot",

  data() {
    return {
      form: {
        locationName: "",
        address: "",
        pincode: "",
        pricePerHour: "",
        maxSpots: ""
      }
    };
  },

  methods: {
    async addLot() {
      try {
        const res = await axios.post(
          "http://localhost:5000/api/admin/lot/add",
          this.form
        );

        if (res.data.success) {
          alert("Parking Lot Added Successfully!");
          this.$router.push("/admin/dashboard");
        } else {
          alert(res.data.message);
        }

      } catch (err) {
        console.error(err);
        alert("Error adding parking lot");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";
</style>
