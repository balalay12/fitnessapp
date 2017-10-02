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
import ProfilePage from './components/Profile.vue'
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

    { path: '/profile', component: ProfilePage }
  ]
})

import store from './store'

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
