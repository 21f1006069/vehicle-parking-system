<template>
  <div class="container mt-4">

    <h2 class="title">Edit Parking Lot</h2>

    <div class="d-flex justify-content-center">
      <form @submit.prevent="updateLot" class="border p-4 bg-light rounded" style="width: 600px;">
        
        <div class="mb-3">
          <label>Location Name</label>
          <input v-model="form.locationName" type="text" class="form-control" required>
        </div>

        <div class="mb-3">
          <label>Address</label>
          <input v-model="form.address" type="text" class="form-control" required>
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

        <button class="btn btn-primary" type="submit">Update</button>
        <button class="btn btn-secondary ms-2" @click="$router.push('/admin/dashboard')" type="button">Cancel</button>

      </form>
    </div>

  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "EditLot",

  data() {
    return {
      form: {
        locationName: "",
        address: "",
        pincode: "",
        pricePerHour: "",
        maxSpots: "",
        lot_id: null
      }
    };
  },

  async mounted() {
    const lotId = this.$route.params.lotId;
    await this.loadLot(lotId);
  },

  methods: {
    async loadLot(id) {
      try {
        const res = await axios.get(`http://localhost:5000/api/admin/lot/${id}`);

        if (res.data.success) {
          const lot = res.data.lot;
          this.form.locationName = lot.location_name;
          this.form.address = lot.address;
          this.form.pincode = lot.pincode;
          this.form.pricePerHour = lot.price;
          this.form.maxSpots = lot.maxSpots;
          this.form.lot_id = lot.lot_id;
        }
      } catch (err) {
        console.error(err);
        alert("Failed to load lot data!");
      }
    },

    async updateLot() {
      try {
        const res = await axios.post(
          "http://localhost:5000/api/admin/lot/update",
          this.form
        );

        if (res.data.success) {
          alert("Parking lot updated!");
          this.$router.push("/admin/dashboard");
        } else {
          alert(res.data.message);
        }

      } catch (err) {
        console.error(err);
        alert("Error updating lot");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";
</style>
