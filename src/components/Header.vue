<template>
<div>

  <md-toolbar>
    <md-button class="md-icon-button" @click="toggleLeftSidenav">
      <md-icon>menu</md-icon>
    </md-button>

    <router-link tag="h2" to="/" class="md-title" style="flex: 1">FitnessApp <span class="md-caption">PREalpha v.0.1.0</span></router-link>
  </md-toolbar>

  <md-sidenav class="md-left md-fixed" ref="leftSidenav" md-swipeable>
    <md-toolbar v-if="currentUser.is_auth" class="md-account-header">
      <md-list class="md-transparent">
        <md-list-item class="md-avatar-list" @click="linkToProfile">
          <md-avatar class="md-large">
            <img v-if="currentUser.data.photo" :src="currentUser.data.photo" alt="Avatar">
            <img v-else src="http://vk.com/images/camera_b.gif" alt="Avatar">
          </md-avatar>
        </md-list-item>
        <md-list-item>
          <div class="md-list-text-container">
            <span>{{ currentUser.data.first_name }} {{ currentUser.data.last_name }}</span>
            <span v-if="currentUser.data.email">{{ currentUser.data.email }}</span>
          </div>
        </md-list-item>
      </md-list>
    </md-toolbar>

    <md-toolbar v-else>
      <h3 class="md-title">Вы не авторизованы</h3>
    </md-toolbar>

    <md-list v-if="currentUser.is_auth">
      <router-link tag="md-list-item" to="/training">
        Тренировки
      </router-link>
      <router-link tag="md-list-item" to="/bodysize">
        Размеры тела
      </router-link>
      <router-link tag="md-list-item" to="/programms">
        Программы тренировок
        <md-divider></md-divider>
      </router-link>
      <md-list-item  @click="logout">
        <span>Выход</span>
      </md-list-item>
    </md-list>
  </md-sidenav>

</div>
</template>

<script>
// import { mapActions, mapGetters } from 'vuex'
import axios from 'axios'

export default {
  data () {
    return {
    }
  },

  methods: {
    toggleLeftSidenav() {
      this.$refs.leftSidenav.toggle();
    },
    linkToProfile() {
      this.$router.push('/profile')
    },
    logout() {
      axios.get('/logout')
      .then(response => {
        this.$store.dispatch('userLogout')
      })
    }
  },

  computed: {
    currentUser() {
      return this.$store.getters.currentUser
    }
  }
}
</script>

<style>
</style>
