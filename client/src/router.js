import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import store from '@/store'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/points',
      name: 'Points',
      component: () =>
      import(/* webpackChunkName: "points" */ '@/views/Points.vue'),
      props: (route) => ({ user: route.query.user }),
    },
    {
      path: '/points/:id',
      name: 'Point',
      alias: ['/points/create'],
      props: true,
      component: () =>
      import(/* webpackChunkName: "point" */ '@/views/Point.vue')
    },
    {
      path: '/users',
      name: 'Users',
      component: () =>
      import(/* webpackChunkName: "users" */ '@/views/Users.vue'),
      props: (route) => ({ user: route.query.user }),
    },
  ],
})

router.beforeEach((to, from, next) => {
  /*
   * Check if the user is authenticated or accessing a public page.
   * If the user is not authenticated and not accessing a public page,
   * redirect them to the login or register page.
   */
  const token = store.state.token
  const user = store.state.currentUser
  const exposedPages = ['/login', '/register']

  if (exposedPages.includes(to.path)) {
    next()
  } else if (token && user) {
    next()
  } else {
    if (from.path == '/register') {
      return next('/register')
    } else {
      return next('/login')
    }
  }

})

export default router
