<template>
  <div class="container mt-5">

    <h2 class="title">View / Delete Parking Spot</h2>

    <div class="view-Spot border p-4 rounded mt-4" style="max-width: 400px; margin: auto;">

      <div class="mb-3">
        <label><b>ID:</b></label>
        <input class="form-control" type="text" :value="spot.spot_id" readonly>
      </div>

      <div class="mb-3">
        <label><b>Status:</b></label>
        <input class="form-control" type="text" :value="spot.status" readonly>
      </div>

      <div class="mt-3">

        <!-- Show Delete button only for Available spots -->
        <button v-if="spot.status === 'A'"
                class="btn btn-danger"
                @click="deleteSpot">
          Delete
        </button>

        <button class="btn btn-secondary ms-2"
                @click="$router.push('/admin/dashboard')">
          Close
        </button>

      </div>
    </div>

  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "ViewSpot",

  data() {
    return {
      spot: {
        spot_id: null,
        lot_id: null,
        status: null
      }
    };
  },

  async mounted() {
    const { lotId, spotId, status } = this.$route.params;

    await this.loadSpot(lotId, spotId, status);
  },

  methods: {
    async loadSpot(lotId, spotId, status) {
      try {
        const res = await axios.get(
          `http://localhost:5000/api/admin/spot/${lotId}/${spotId}/${status}`
        );

        if (res.data.success) {
          this.spot = res.data.spot;
        }

      } catch (err) {
        console.error(err);
        alert("Failed to load spot info");
      }
    },

    async deleteSpot() {
      try {
        const res = await axios.post(
          "http://localhost:5000/api/admin/spot/delete",
          {
            spot_id: this.spot.spot_id,
            lot_id: this.spot.lot_id
          }
        );

        if (res.data.success) {
          alert("Spot deleted successfully");
          this.$router.push("/admin/dashboard");
        }

      } catch (err) {
        console.error(err);
        alert("Failed to delete spot");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";
</style>
