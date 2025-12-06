<template>
  <div class="container mt-4">

    <h2 class="title">Registered Users</h2>

    <table class="table table-striped table-bordered mt-4">
      <thead class="table-dark">
        <tr>
          <th>Id</th>
          <th>Email</th>
          <th>Full Name</th>
          <th>Address</th>
          <th>Pincode</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.fullname }}</td>
          <td>{{ user.address }}</td>
          <td>{{ user.pincode }}</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "Users",

  data() {
    return {
      users: []
    };
  },

  async mounted() {
    await this.loadUsers();
  },

  methods: {
    async loadUsers() {
      try {
        const res = await axios.get("http://localhost:5000/api/admin/users");

        if (res.data.success) {
          this.users = res.data.users;
        }

      } catch (err) {
        console.error(err);
        alert("Failed to load users");
      }
    }
  }
};
</script>

<style scoped>
@import "/src/assets/style.css";

.table {
  font-size: 16px;
}
</style>
