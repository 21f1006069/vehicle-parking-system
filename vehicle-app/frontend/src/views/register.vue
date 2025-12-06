<template>
 <div class="title">Vehicle Parking System</div>
    <div class="form-container">
      <h2 class="form-title">Register</h2>

      <form @submit.prevent="registerUser">

        <div class="mb-3">
          <label>Email</label>
          <input
            type="email"
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

        <div class="mb-3">
          <label>Name</label>
          <input
            type="text"
            v-model="fullname"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label>Address</label>
          <input
            type="text"
            v-model="address"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label>Pincode</label>
          <input
            type="text"
            v-model="pincode"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label>Phone Number</label>
          <input
            type="text"
            v-model="phone_no"
            class="form-control"
            required
          />
        </div>

        <button class="btn btn-success w-100" type="submit">
          Register
        </button>

        <p class="mt-3 text-center">
          Already have an account?
          <RouterLink to="/login">Login</RouterLink>
        </p>

      </form>
    </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      fullname: "",
      address: "",
      pincode: "",
      phone_no: ""
    };
  },

  methods: {
    async registerUser() {
      try {
        const res = await axios.post(
          "http://localhost:5000/api/register",
          {
            email: this.email,
            password: this.password,
            fullname: this.fullname,
            address: this.address,
            pincode: this.pincode,
            phone_no: this.phone_no
          }
        );

        if (res.data.success) {
          alert("Registration successful!");
          this.$router.push("/login");
        } else {
          alert(res.data.message);
        }

      } catch (error) {
        console.error(error);
        alert("Failed to register. Check your API.");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";

</style>
