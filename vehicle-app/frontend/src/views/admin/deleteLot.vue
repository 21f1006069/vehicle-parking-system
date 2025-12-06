<template>
  <div class="container mt-5 text-center">

    <h3 class="mb-4">
      Do you want to delete Parking Lot {{ lotId }}?
    </h3>

    <div class="d-flex justify-content-center gap-3">

      <button class="btn btn-danger" @click="deleteLot">
        Delete
      </button>

      <button class="btn btn-secondary" @click="$router.push('/admin/dashboard')">
        Cancel
      </button>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DeleteLot",

  data() {
    return {
      lotId: this.$route.params.lotId
    };
  },

  methods: {
    async deleteLot() {
      try {
        const res = await axios.post(
          `http://localhost:5000/api/admin/lot/delete/${this.lotId}`
        );

        if (res.data.success) {
          alert("Parking lot deleted successfully");
          this.$router.push("/admin/dashboard");
        } else {
          alert(res.data.message);
        }

      } catch (err) {
        console.error(err);
        alert("Failed to delete parking lot");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";

.delete-confirmation-box {
  padding: 30px;
  border-radius: 12px;
  background: #f8f8f8;
  width: 400px;
  margin: 0 auto;
}
</style>
