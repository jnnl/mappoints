import Vue from "vue"
import Toasted from 'vue-toasted';
import BootstrapVue from "bootstrap-vue"
import "bootstrap"
import "bootstrap-vue/dist/bootstrap-vue.css"
import "bootstrap/dist/css/bootstrap.min.css"
import _ from 'lodash'

import App from "./App.vue"
import store from "./store"
import router from "./router"
import leaflet from "./leaflet"

// Use vue-toasted and bootstrap-vue
Vue.use(Toasted, { duration: 5000 })
Vue.use(BootstrapVue)

// Initialize leaflet
leaflet()

// Bind lodash globally
Vue.prototype._ = _

Vue.config.productionTip = false

// Create the Vue instance
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app")
