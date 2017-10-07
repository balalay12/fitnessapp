import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Vuelidate from 'vuelidate'
import VueMaterial from 'vue-material'
import Cookies from 'js-cookie'
import axios from 'axios'

// set csrf-token to headers
let csrftoken = localStorage.getItem('csrf_token')
axios.defaults.headers.common['cookiename'] = 'csrftoken'
axios.defaults.headers.common['X-CSRFToken'] = csrftoken
axios.defaults.headers.common['Access-Control-Allow-Origin'] = "*"

// Import vue material components
Vue.use(VueMaterial)

Vue.material.registerTheme('default', {
  primary: 'orange',
  accent: 'deep-purple',
  warn: 'red',
  background: 'white'
})

Vue.use(Vuelidate)

Vue.use(VueRouter)

import MainPage from './components/MainPage.vue'
import ProfilePage from './components/Profile.vue'
import BodysizePage from './components/Bodysize.vue'
import Training from './components/Training.vue'
import LoginForm from './forms/Login.vue'
import RegistrationForm from './forms/Registration.vue'
import TrainingAddForm from './forms/TrainingAddForm.vue'

const router = new VueRouter({
  routes: [
    { path: '/', component: MainPage },
    { path: '/login', component: LoginForm },
    { path: '/registration', component: RegistrationForm },
    { path: '/training', component: Training },
    { path: '/training/add', component: TrainingAddForm },

    { path: '/profile', component: ProfilePage },
    { path: '/bodysize', component: BodysizePage }
  ]
})

import store from './store'

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
