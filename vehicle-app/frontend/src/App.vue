<template>
  <div>
    <!-- Navbar appears on all pages except login and register -->
    <Navbar v-if="showNavbar" />

    <!-- Page content -->
    <router-view />
  </div>
</template>

<script>
import Navbar from "./components/navbar.vue";

export default {
  name: "App",

  components: {
    Navbar
  },

  computed: {
    showNavbar() {
      // Do NOT show navbar on login or register routes
      const hiddenRoutes = ["/login", "/register"];
      return !hiddenRoutes.includes(this.$route.path);
    }
  }
};
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
