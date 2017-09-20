<template>

  <md-layout md-align="center">

    <md-card v-if="!currentUser.is_auth">
      <md-card-header>
        <div class="md-title">
          Вы не авторизованы
        </div>
      </md-card-header>
      <md-card-content>
        <p>Если вы еще не зарегестрирвоаны на этом сайте, то нажмите на кнопку <router-link tag="a" to="/registration" class="md-raised md-primary">Регистрация</router-link>.</p>
        <p>В том случае если вы уже бывали у нас раньше, то жмите на кнопку <router-link tag="a" to="/login" class="md-raised md-primary">Войти</router-link></p>
        <md-button href="/vk_auth" class="md-raised md-primary">Авторзация с помощью вконтакте</md-button>
      </md-card-content>
      <!-- <md-card-actions>
        <router-link tag="a" to="/login" class="md-raised md-primary">Войти</router-link>
        <router-link tag="md-button" to="/registration" class="md-raised md-primary">Регистрация</router-link>
      </md-card-actions> -->
    </md-card>

  </md-layout>

</template>

<script>
export default {

  data() {
      return {}
  },

  computed: {
    currentUser() {
      return this.$store.getters.currentUser
    }
  }
}
</script>
