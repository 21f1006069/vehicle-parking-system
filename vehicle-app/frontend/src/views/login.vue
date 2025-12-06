<template>
 <div class="title">Vehicle Parking System</div>
  <div class="center-wrapper">
    <div class="form-container">
      <h2 class="form-title">Login</h2>

      <form @submit.prevent="loginUser">

        <div class="mb-3">
          <label>Email</label>
          <input type="email"
            v-model="email"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label>Password</label>
          <input
            type="password"
            v-model="password"
            class="form-control"
            required
          />
        </div>

        <button class="btn btn-primary w-100" type="submit">
          Login
        </button>

        <p class="mt-3 text-center">
          Don't have an account?
          <RouterLink to="/register">Register</RouterLink>
        </p>
      </form>
    </div>
  </div>
  
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },

  methods: {
    async loginUser() {
      try {
        const res = await axios.post(
          "http://localhost:5000/api/login",
          {
            email: this.email,
            password: this.password,
          },
          { withCredentials: true }
        );

        if (!res.data.success) {
          alert("Invalid username or password");
          return;
        }

        // Save user in localStorage
        localStorage.setItem("user", JSON.stringify(res.data));

        // Redirect based on role
        if (res.data.role === "admin") {
          this.$router.push("/admin/dashboard");
        } else {
          this.$router.push("/dashboard");
        }

      } catch (error) {
        console.error(error);
        alert("Login failed. There is an issue with API.");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";   /* Your uploaded CSS */

/* Additional component-specific fixes */
.center-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
}
</style>
