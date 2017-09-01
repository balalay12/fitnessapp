import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Vuelidate from 'vuelidate'
import VueMaterial from 'vue-material'

// Import vue material components
Vue.use(VueMaterial)

Vue.use(Vuelidate)

Vue.use(VueRouter)

import LoginForm from './forms/Login.vue'
import RegistrationForm from './forms/Registration.vue'

const router = new VueRouter({
  routes: [
    {path: '/login', component: LoginForm},
    {path: '/registration', component: RegistrationForm}
  ]
})

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
