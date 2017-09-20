<template>
<div>

  <md-toolbar>
    <md-button class="md-icon-button" @click="toggleLeftSidenav">
      <md-icon>menu</md-icon>
    </md-button>

    <router-link tag="h2" to="/" class="md-title" style="flex: 1">FitnessApp <span class="md-caption">PREalpha v.0.1.0</span></router-link>
    <!-- <router-link tag="md-button" to="/login" class="md-raised md-primary">Login</router-link>
    <router-link tag="md-button" to="/registration" class="md-raised md-primary">Registration</router-link> -->
  </md-toolbar>

  <md-sidenav class="md-left md-fixed" ref="leftSidenav">
    <md-toolbar v-if="currentUser.is_auth" class="md-account-header">
      <md-list class="md-transparent">
        <md-list-item class="md-avatar-list">
          <md-avatar class="md-large">
            <img :src="currentUser.data.photo" alt="Avatar">
          </md-avatar>
          <!-- <span>{{ currentUser.data.first_name }} {{ currentUser.data.last_name }}</span> -->
        </md-list-item>
        <md-list-item>
          <div class="md-list-text-container">
            <span>{{ currentUser.data.first_name }} {{ currentUser.data.last_name }}</span>
            <!-- <span>{{ currentUser.data.email }}</span> -->
          </div>
        </md-list-item>
      </md-list>
    </md-toolbar>

    <md-toolbar v-else>
      <h3 class="md-title">Вы не авторизованы</h3>
    </md-toolbar>

    <md-list v-if="currentUser.is_auth">
      <md-list-item @click="linkToTraining">
        <span>Тренировки</span>
        <md-divider></md-divider>
      </md-list-item>
      <md-list-item  @click="logout">
        <span>ВЫЙТИ</span>
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

    linkToTraining() {
      this.$router.push('/training')
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
