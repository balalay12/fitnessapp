<template>
<div>

  <md-toolbar>
    <md-button class="md-icon-button" @click="toggleLeftSidenav">
      <md-icon>menu</md-icon>
    </md-button>

    <router-link tag="h2" to="/" class="md-title" style="flex: 1">FitnessApp</router-link>
    <router-link tag="md-button" to="/login" class="md-raised md-primary">Login</router-link>
    <router-link tag="md-button" to="/registration" class="md-raised md-primary">Registration</router-link>
  </md-toolbar>

  <md-sidenav class="md-left md-fixed" ref="leftSidenav">
    <md-toolbar class="md-large">
      <div class="md-toolbar-container">
        <h3 class="md-title">Здесь будет фото юзверя елси он убдет авторизован</h3>
      </div>
    </md-toolbar>

    <p>А здесь будут друзья у тренеров, а что будет у обычных пользователей пока не понятно</p>
  </md-sidenav>

</div>
</template>

<script>
// import { mapActions, mapGetters } from 'vuex'

export default {
  data () {
    return {
    }
  },

  methods: {
    toggleLeftSidenav() {
      this.$refs.leftSidenav.toggle();
    }
  }
}
</script>

<style>
</style>
