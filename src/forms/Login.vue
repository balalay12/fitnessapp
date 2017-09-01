<template>
	<div>

		<md-layout md-tag="form" md-align="center" @submit.stop.prevent="submit" novalidate>

			<md-layout md-tag="md-card" md-column md-flex="30" md-flex-medium="40" md-flex-small="60" md-flex-xsmall="90">
				<md-card-header>
					<div class="md-title">Вход</div>
				</md-card-header>

				<md-card-content>
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
		</md-layout></md-layout>

</div>
</template>

<script>
import axios from 'axios'
import { required, email } from 'vuelidate/lib/validators'

export default {

  data() {
    return {
			email: 'test@test.ru',
			password: '11111111',
			errorsMsg: []
		}
	},

	methods: {
		submit() {
      this.errorsMsg = []
      if (this.$v.email.$invalid
          || this.$v.password.$invalid) {
        if (this.$v.email.$invalid) {
          this.errorsMsg.push('В поле ввода электронной почты ошибка')
        }
        if (this.$v.password.$invalid) {
          this.errorsMsg.push('В поле ввода пароля ошибка')
        }
      } else {
        console.log('send data')
				axios.post('/login', {
          email: this.email,
          password: this.password
        })
        .then(response => {
          console.log(response.data)
        })
      }
    }
	},
	
	validations: {
		email: {
      required,
      email
    },
		password: {
			required
		},
	}
}
</script>