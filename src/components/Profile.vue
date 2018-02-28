<template>
	<md-layout md-gutter md-align="center">
		<md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">

			<md-card class="md-accent">
				<md-card-header>
					<md-avatar class="md-large">
					 	<img v-if="currentUser.data.photo" :src="currentUser.data.photo" alt="Avatar">
						<img v-else src="http://vk.com/images/camera_b.gif" alt="Avatar">
					</md-avatar>
					<md-card-header-text>
						<div class="md-title">
							{{ currentUser.data.first_name }} {{ currentUser.data.last_name }}
						</div>
						<div class="md-subhead" v-if="currentUser.data.role == 'user'">
							Пользователь
						</div>
						<div class="md-subhead" v-if="currentUser.data.role == 'trainer'">
							Тренер
						</div>
					</md-card-header-text>

				</md-card-header>
			</md-card>

		</md-layout>

		<md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" md-gutter>
			<md-list>
				
				<md-list-item v-if="currentUser.data.role == 'user'">
					<span>Upgrade ur account: </span>
					<md-button class="md-raised md-primary" @click="changeRole">
						Стать тренером
					</md-button>
				</md-list-item>

				<md-list-item v-if="!showGoalForm">
					<p v-if="currentUser.data.goal">Цель: {{ currentUser.data.goal }}</p>
					<span v-else>Цель будет напоминать вам о том, чего вы хотите добиться (а так же будет видна тренерам)</span>
					<md-button class="md-icon-button md-raised" @click="showInputHandle('goal')">
						<md-icon>add</md-icon>
					</md-button>
				</md-list-item>

				<!-- goal input -->
				<md-layout class="text-content" md-collumn v-if="showGoalForm">
					<md-input-container>
						<label>Цель</label>
						<md-textarea v-model="goal"></md-textarea>
					</md-input-container>
					<md-button class="md-raised" @click="showInputHandle('goal')">Отменить</md-button>
					<md-button class="md-raised md-primary" @click="saveGoal">Сохранить</md-button>
				</md-layout>

				<md-list-item>
					<span v-if="currentUser.data.email">Email: {{ currentUser.data.email }}</span>
					<span v-else >Email: нет данных</span>
				</md-list-item>

				<md-list-item>
					<span v-if="currentUser.data.vk_id">VK: {{ currentUser.data.vk_id }}</span>
					<span v-else>VK: нет данных</span>
				</md-list-item>

			</md-list>

			<!-- If user have trainer -->
			<md-whiteframe md-tag="div" v-if="currentUser.data.trainer">
				<md-subheader>Ваш тренер</md-subheader>

				<md-card>
					<md-card-header>
						<md-avatar class="md-large">
						 	<img v-if="currentUser.data.trainer.photo" :src="currentUser.data.trainer.photo" alt="Avatar">
							<img v-else src="http://vk.com/images/camera_b.gif" alt="Avatar">
						</md-avatar>
						<md-card-header-text>
							<div class="md-title">
								{{ currentUser.data.trainer.first_name }} {{ currentUser.data.trainer.last_name }}
							</div>
							<div class="md-subhead">
								Тренер
							</div>
						</md-card-header-text>
					</md-card-header>
					<md-card-content>
						<p v-if="currentUser.data.trainer.goal"><span>Цель: </span>{{ currentUser.data.trainer.goal }}</p>
						<p v-if="currentUser.data.trainer.description"><span>Описание: </span>{{ currentUser.data.trainer.description }}</p>
						<p v-if="currentUser.data.trainer.price"><span>Стоимость: </span>{{ currentUser.data.trainer.price }} р.</p>
					</md-card-content>
				</md-card>

			</md-whiteframe>

			<!-- Trainer add info here -->
			<md-whiteframe md-tag="div" v-if="currentUser.data.role == 'trainer'">
				<md-subheader>Тренерская информация</md-subheader>
				<span class="md-caption text-content">Эта информация будет видна для людей, которые ищут тренера для себя.</span>
				<md-list>

					<md-list-item v-if="!showpriceForm">
						Стоимость: {{ currentUser.data.price }} р.
						<md-button class="md-icon-button md-raised" @click="showInputHandle('price')">
							<md-icon>add</md-icon>
						</md-button>
					</md-list-item>

					<!-- price input -->
					<md-layout class="text-content" md-collumn v-if="showpriceForm">
						<md-input-container>
							<label>Стоимость</label>
							<md-input v-model="price"></md-input>
						</md-input-container>
						<md-button class="md-raised" @click="showInputHandle('price')">Отменить</md-button>
						<md-button class="md-raised md-primary" @click="saveTrainerInfo('price')">Сохранить</md-button>
					</md-layout>

					<md-list-item v-if="!showDescFrom">
						Описание: {{ currentUser.data.description }}
						<md-button class="md-icon-button md-raised" @click="showInputHandle('description')">
							<md-icon>add</md-icon>
						</md-button>
					</md-list-item>

					<!-- descriptiion input -->
					<md-layout class="text-content" md-collumn v-if="showDescFrom">
						<md-input-container>
							<label>Описание</label>
							<md-textarea v-model="description"></md-textarea>
						</md-input-container>
						<md-button class="md-raised" @click="showInputHandle('description')">Отменить</md-button>
						<md-button class="md-raised md-primary" @click="saveTrainerInfo('description')">Сохранить</md-button>
					</md-layout>

				</md-list>
			</md-whiteframe>

		</md-layout>

		<Snackbar ref="snackbar"></Snackbar>

	</md-layout>

</template>

<script>
import axios from 'axios'
import Snackbar from './Snackbar.vue'

export default {
	data() {
		return {
			showGoalForm: false,
			showpriceForm: false,
			showDescFrom: false,
			goal: '',
			price: '',
			description: ''
		}
	},

	components: {
		Snackbar
	},

	computed: {
		currentUser() {
			return this.$store.getters.currentUser
		}
	},

	methods: {
		showInputHandle(name) {
			if (name == 'goal') {
				this.goal = this.currentUser.data.goal	
				this.showGoalForm = !this.showGoalForm
			}
			else if (name == 'price') {
				// TODO: i guess needed change this shitting code
				this.price = this.currentUser.data.price
				this.description = this.currentUser.data.description
				this.showpriceForm = !this.showpriceForm
			} 
			else if (name == 'description') {
				// TODO: i guess needed change this shitting code
				this.description = this.currentUser.data.description
				this.price = this.currentUser.data.price
				this.showDescFrom = !this.showDescFrom
			}
		},
		saveGoal() {
			axios.post('/goal', {
				goal: this.goal
			})
			.then(response => {
				if (response.data.error) {
            		this.$refs.snackbar.openSnackbar(response.data.error)
            	} else {
            		this.$store.dispatch('userUpdate')
            		this.showInputHandle('goal')
            	}
			})
		},
		changeRole() {
			// change user role to trainer
			axios.get('/change_role_to_trainer')
			.then(response => {
				if (response.data.error) {
            		this.$refs.snackbar.openSnackbar(response.data.error)
            	} else {
            		this.$store.dispatch('userUpdate')
            	}
			})
		},
		saveTrainerInfo(name) {
			axios.post('/trainer_info', {
				price: this.price,
				description: this.description
			})
			.then(response => {
				if (response.data.error) {
            		this.$refs.snackbar.openSnackbar(response.data.error)
            	} else {
            		this.$store.dispatch('userUpdate')
            		this.showInputHandle(name)
            	}
			})
		}
	}
}
</script>

<style>

</style>