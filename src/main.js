import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Vuelidate from 'vuelidate'
import VueMaterial from 'vue-material'
import Cookies from 'js-cookie'
import axios from 'axios'

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

// dynamin import components
const MainPage = () => import(/* webpackChunkName: "MainPage" */ './components/MainPage.vue');
const ProfilePage = () => import(/* webpackChunkName: "ProfilePage" */ './components/Profile.vue');
const BodysizePage = () => import(/* webpackChunkName: "BodysizePage" */ './components/Bodysize/Bodysize.vue');
const Training = () => import(/* webpackChunkName: "Training" */ './components/Training/Training.vue');
const Programms = () => import(/* webpackChunkName: "Programms" */ './components/Programms/Programms.vue');
const LoginForm = () => import(/* webpackChunkName: "LoginForm" */ './components/Login.vue');
const RegistrationForm = () => import(/* webpackChunkName: "RegistrationForm" */ './components/Registration.vue');
const TrainingAddForm = () => import(/* webpackChunkName: "TrainingAddForm" */ './components/Training/TrainingAddForm.vue');
const Notifications = () => import(/* webpackChunkName: "Notifications" */ './components/Notifications.vue');
const TrainersList = () => import(/* webpackChunkName: "TrainersList" */ './components/TrainersList.vue');

const router = new VueRouter({
    routes: [
        {path: '/', component: MainPage},
        {path: '/login', component: LoginForm},
        {path: '/registration', component: RegistrationForm},
        {path: '/training', component: Training},
        {path: '/training/add', component: TrainingAddForm},

        {path: '/profile', component: ProfilePage},
        {path: '/bodysize', component: BodysizePage},
        {path: '/programms', component: Programms},
        {path: '/notifications', component: Notifications},
        {path: '/trainers', component: TrainersList}
    ]
})

import store from './store'

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});
