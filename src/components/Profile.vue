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

			<!-- if user have trainer -->
			<md-whiteframe md-tag="div" v-if="currentUser.data.trainer">
				<md-subheader>Ваш тренер</md-subheader>
				<h1 class="text-content">{{ currentUser.data.trainer.first_name }} {{ currentUser.data.trainer.last_name }}</h1>
				<div class="md-body-1 text-content">Стоимость {{ currentUser.data.trainer.price ? currentUser.data.trainer.price : '-' }}</div>
				<div v-if="currentUser.data.trainer.description" class="md-body-1 text-content">{{ currentUser.data.trainer.description }}</div>
				<md-button class="md-raised md-warn" @click="deleteTrainer">Отказаться от услуг</md-button>
			</md-whiteframe>

			<!-- Trainer information -->
			<md-whiteframe md-tag="div" v-if="currentUser.data.role == 'trainer'">
				<md-subheader>Тренерская информация</md-subheader>
				<span class="md-caption text-content">Эта информация будет видна для людей, которые ищут тренера для себя.</span>
				<md-list v-if="!showInforamtionForm">

					<md-list-item>
						Стоимость: {{ currentUser.data.price ? currentUser.data.price + " руб" : "Информация не указана" }}
					</md-list-item>

					<md-list-item>
						Описание: {{ currentUser.data.description ? currentUser.data.description : "Информация не указана" }}
					</md-list-item>

				</md-list>

				<!-- price input -->
				<md-layout class="text-content" md-collumn v-if="showInforamtionForm">
					<md-input-container>
						<label>Стоимость</label>
						<md-input v-model="price"></md-input>
					</md-input-container>

					<md-input-container>
						<label>Описание</label>
						<md-textarea v-model="description"></md-textarea>
					</md-input-container>
					<md-button class="md-raised" @click="showInforamtionForm = false">Отменить</md-button>
					<md-button class="md-raised md-primary" @click="saveTrainerInfo">Сохранить</md-button>
				</md-layout>

				
				<md-button 
					v-if="!showInforamtionForm" 
					class="md-raised md-primary" 
					@click="showInforamtionForm = true; description = currentUser.data.description; price = currentUser.data.price"
					>Редактировать</md-button>
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
			showInforamtionForm: false,
			showGoalForm: false,
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
		saveTrainerInfo() {
			axios.post('/trainer_info', {
				price: this.price,
				description: this.description
			})
			.then(response => {
				if (response.data.error) {
            		this.$refs.snackbar.openSnackbar(response.data.error)
            	} else {
            		this.$store.dispatch('userUpdate')
            		this.showInforamtionForm = false
            	}
			})
		},
		deleteTrainer() {
			axios.get('/delete_trainer')
			.then(response => {
				if (response.data.error) {
            		this.$refs.snackbar.openSnackbar(response.data.error)
            	} else {
            		this.$store.dispatch('userUpdate')
            	}
			})
		}
	}
}
</script>

<style>

</style>