<template>
<div>

<md-layout md-tag="form" md-align="center" @submit.stop.prevent="submit" novalidate>

  <md-layout md-tag="md-card" md-column md-flex="30" md-flex-medium="40" md-flex-small="60" md-flex-xsmall="90">
    <md-card-header>
      <div class="md-title">Регистрация</div>
    </md-card-header>

    <md-card-content>
      <md-input-container v-bind:class="{ 'md-input-invalid': $v.first_name.$error }">
        <label>Имя</label>
        <md-input name="first_name" v-model="first_name" @input="$v.first_name.$touch()" required></md-input>
        <span v-if="!$v.first_name.required" class="md-error">Поле обязательно</span>
      </md-input-container>

      <md-input-container v-bind:class="{ 'md-input-invalid': $v.last_name.$error }">
        <label>Фамиля</label>
        <md-input name="last_name" v-model="last_name" @input="$v.last_name.$touch()" required></md-input>
        <span v-if="!$v.last_name.required" class="md-error">Поле обязательно</span>
      </md-input-container>

      <md-input-container v-bind:class="{ 'md-input-invalid': $v.email.$error }">
        <label>Email</label>
        <md-input name="email" v-model="email" @input="$v.email.$touch()" required></md-input>
        <span v-if="!$v.email.required" class="md-error">Поле обязательно</span>
        <span v-if="!$v.email.email" class="md-error">
          Введите корректный адрес электронной почты.
        </span>
      </md-input-container>

      <md-input-container v-bind:class="{ 'md-input-invalid': $v.password.$error }">
        <label>Пароль</label>
        <md-input name="password" v-model="password" type="password" @input="$v.password.$touch()" required></md-input>
        <span v-if="!$v.password.required" class="md-error">Поле обязательно</span>
        <span v-if="!$v.password.minLength" class="md-error">
          Пароль должен быть не менее {{ $v.password.$params.minLength.min }} символов.
        </span>
      </md-input-container>

      <md-input-container v-bind:class="{ 'md-input-invalid': $v.repeatPassword.$error }">
        <label>Пароль</label>
        <md-input name="repeatPassword" v-model="repeatPassword" type="password" @input="$v.repeatPassword.$touch()" required></md-input>
        <span v-if="!$v.repeatPassword.sameAsPassword" class="md-error">Пароли должны совпадать</span>
      </md-input-container>

      <md-layout v-if='errorsMsg.length != 0'>
        <md-list class="md-dense" v-for="msg in errorsMsg" :key="msg.id">
          <md-list-item><span class="md-error">{{ msg }}</span></md-list-item>
        </md-list>
      </md-layout>
    </md-card-content>

    <md-card-actions>
      <md-button @click="submit">Войти</md-button>
    </md-card-actions>

    <md-snackbar :md-position="vertical + ' ' + horizontal" ref="snackbar" :md-duration="duration">
      <span>{{ server_error }}</span>
      <md-button class="md-accent" @click="$refs.snackbar.close()">Закрыть</md-button>
    </md-snackbar>

  </md-layout>
</md-layout>

</div>
</template>

<script>
import axios from 'axios'
import { required, email, minLength, sameAs } from 'vuelidate/lib/validators'

export default {

  data() {
    return {
      first_name: 'test',
      last_name: 'test',
      email: 'test@test.ru',
      password: '11111111',
      repeatPassword: '11111111',
      errorsMsg: [],
      server_error: '',
      vertical: 'top',
      horizontal: 'right',
      duration: 4000
    }
  },

  methods: {
    submit() {
      this.errorsMsg = []
      if (this.$v.email.$invalid
          || this.$v.password.$invalid
          || this.$v.repeatPassword.$invalid) {
        if (this.$v.email.$invalid) {
          this.errorsMsg.push('В поле ввода электронной почты ошибка')
        }
        if (this.$v.password.$invalid) {
          this.errorsMsg.push('В поле ввода пароля ошибка')
        }
        if (this.$v.repeatPassword.$invalid) {
          this.errorsMsg.push('В поле ввода повторного пароля ошибка')
        }
      } else {
        axios.post('/registration', {
          email: this.email,
          first_name: this.first_name,
          last_name: this.last_name,
          password: this.password
        })
        .then(response => {
          if (response.data.error) {
            this.server_error = response.data.error
            this.$refs.snackbar.open();
          } else {
            this.$router.push('/login')
          }
        })
      }
    }
  },

  validations: {
    first_name: {
      required
    },
    last_name: {
      required
    },
    email: {
      required,
      email
    },
    password: {
      required,
      minLength: minLength(8)
    },
    repeatPassword: {
      sameAsPassword: sameAs('password')
    }
  }
}
</script>
