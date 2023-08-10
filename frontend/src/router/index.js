import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { isAdmin, getToken } from '../helpers/authHelper';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/admin/',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: 'test',
          name: 'admin-test',
          component: () => import('../views/FilterLIst.vue')
        },
        {
          path: 'addvenue',
          name: 'admin-addvenue',
          component: () => import('../views/AddVenue.vue')
        },
        { 
          path: 'addshow',
          name: 'admin-addshow',
          component: () => import('../views/AddShowView.vue')
        },
        {
          path: 'venue/:id/edit',
          name: 'admin-editvenue',
          component: () => import('../views/EditVenueView.vue')
        },
        {
          path: 'venue/:id/addshow',
          name: 'admin-addshowtovenue',
          component: () => import('../views/AddShowToVenueView.vue')
        }
      ]
    },
    {
      path: '/venues',
      name: 'venues',
      component: () => import('../views/VenuesView.vue')
    },
    {
      path: '/venue/:id',
      name: 'venue',
      component: () => import('../views/VenueView.vue')
    },
    {
      path: '/show/:id',
      name: 'show',
      component: () => import('../views/ShowView.vue')
    },
    {
      path: '/bookings',
      name: 'bookings',
      component: () => import('../views/BookingsView.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue')
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: () => import('../views/UnauthorizedView.vue')
    },
  ]
})



router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    // check if user is authenticated and has admin role
    const isUserAdmin = isAdmin();
    if (!isUserAdmin) {
      next('/unauthorized'); // redirect to unauthorized endpoint
    } else {
      console.log("User is admin");
      next();
    }
  } else if (to.name === 'register' || to.name === 'login') {
    // check if user is already authenticated
    const token = getToken();
    if (token) {
      next('/');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
