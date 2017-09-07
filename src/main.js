import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Vuelidate from 'vuelidate'
import VueMaterial from 'vue-material'

// Import vue material components
Vue.use(VueMaterial)

Vue.use(Vuelidate)

Vue.use(VueRouter)

import MainPage from './components/MainPage.vue'
import LoginForm from './forms/Login.vue'
import RegistrationForm from './forms/Registration.vue'

const router = new VueRouter({
  routes: [
    { path: '/', component: MainPage },
    { path: '/login', component: LoginForm },
    { path: '/registration', component: RegistrationForm }
  ]
})

import store from './store'

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});