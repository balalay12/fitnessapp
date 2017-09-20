<template>
  <div id="app">
    <app-header></app-header>
    <router-view></router-view>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {

  data () {
    return {
    }
  },

  components: {
    'app-header': Header,
  },

  created() {
    if (!this.$store.getters.currentUser.data.length) {
      this.$store.dispatch('userInit')
    }
  }
}
</script>

<style>

</style>
