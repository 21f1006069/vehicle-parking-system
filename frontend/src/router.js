import { createRouter, createWebHistory } from 'vue-router';

import Login from './views/login.vue';

const routes = [
  {
    path: '/',
    redirect: '/login'
  },

  {
    path: '/login',
    name: 'Login',
    component: Login
  },

  {
    path: '/register',
    name: 'Register',
    component: () => import('./views/register.vue')
  },

  {
    path: "/admin/dashboard",
    component: () => import("./views/admin/dashboard.vue")
  },

  {
    path: "/admin/edit-lot/:lotId",
    component: () => import("./views/admin/editLot.vue")
  },

  {
    path: "/admin/delete-lot/:lotId",
    component: () => import("./views/admin/deleteLot.vue")
  },

  {
    path: "/admin/add-lot",
    component: () => import("./views/admin/addLot.vue")
  },

  {
    path: "/admin/view-spot/:lotId/:spotId/:status",
    component: () => import("./views/admin/viewSpot.vue")
  },

  {
    path: "/admin/users",
    component: () => import("./views/admin/users.vue")
  },

  {
    path: "/summary",
    component: () => import("./views/admin/adminSummary.vue")
  },

  {
    path: "/dashboard",
    component: () => import("./views/user/dashboard.vue")
  },

  {
    path: "/user/book/:lot_id/:location",
    name: "BookSpot",
    component: () => import("./views/user/bookSpot.vue")
  },

  {
    path: "/user/add-vehicle",
    name: "AddVehicle",
    component: () => import("./views/user/addVehicle.vue")
  },

  {
    path: "/user/release/:spot_id/:vehicle_number/:lot_id/:parking_time",
    name: "ReleaseSpot",
    component: () => import("./views/user/releaseSpot.vue")
  }



];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
