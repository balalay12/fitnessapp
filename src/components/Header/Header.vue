<template>
<div>

  <md-toolbar>
    <md-button class="md-icon-button" @click="openSidenav">
      <md-icon>menu</md-icon>
    </md-button>

    <router-link tag="h2" to="/" class="md-title" style="flex: 1">FitnessApp <span class="md-caption">PREalpha v.0.1.0</span></router-link>
  </md-toolbar>

  <Sidenav ref="sidenav" />

</div>
</template>

<script>
import Sidenav from './Sidenav.vue'

export default {
  components: {
    Sidenav
  },

  methods: {
    openSidenav() {
      this.$refs.sidenav.toggleLeftSidenav()
    }
  }
}
</script>

<style>
</style>
