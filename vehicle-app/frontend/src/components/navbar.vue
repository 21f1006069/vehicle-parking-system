<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">

    <a class="navbar-brand">
      Welcome {{ user?.name }}
    </a>

    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navContent"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navContent">

      <ul class="navbar-nav me-auto">

        <!-- ADMIN MENU -->
        <template v-if="user?.role === 'admin'">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/admin/dashboard">Home</RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/admin/users">Users</RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/summary">Summary</RouterLink>
          </li>

          <li class="nav-item">
            <button class="btn btn-link nav-link" @click="logout">Logout</button>
          </li>
        </template>

        <!-- USER MENU -->
        <template v-if="user?.role === 'user'">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/dashboard">Home</RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/summary">Summary</RouterLink>
          </li>

          <li class="nav-item">
            <button class="btn btn-link nav-link" @click="logout">Logout</button>
          </li>
        </template>

      </ul>

      <!-- USER RIGHT MENu -->
      <template v-if="user?.role === 'user'">
        <ul class="navbar-nav ms-auto">

          <li class="nav-item">
            <button class="btn btn-primary me-2" @click="exportCSV">
              Export Parking History
            </button>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/user/add-vehicle">Add Vehicle</RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink class="nav-link" to="/edit-profile">Edit Profile</RouterLink>
          </li>

        </ul>
      </template>

    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  name: "Navbar",

  data() {
    return {
      user: null
    };
  },

  mounted() {
    this.user = JSON.parse(localStorage.getItem("user"));
  },

  methods: {
    logout() {
      localStorage.removeItem("user");
      this.$router.push("/login");
    },

    async exportCSV() {
  try {
    const res = await axios.post(
      "http://localhost:5000/api/user/exportCSV",
      {},
      { withCredentials: true }
    );
    alert(res.data.message);
  } catch (e) {
    alert("Unable to start export.");
  }
}
  }
};
</script>

<style scoped>

@import "/src/assets/style.css";

.navbar-brand {
  font-weight: bold;
}
</style>
