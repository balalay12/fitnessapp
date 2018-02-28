<template>
	<md-layout md-gutter md-align="center">
		<md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" >
			<h1 class="md-title text-content">Список тренеров которым вы можете подать заявку</h1>
			<span class="text-content">Пока что без фильтра. Возможно будет реализовано позднее, а может и никогда</span>
			<div v-for="(trainer, index) in trainers" :key="index">
				<md-card>
					<md-card-header>
						<md-card-header-text>
							<div class="md-title">{{ trainer.first_name}} {{ trainer.last_name }}</div>
							<div class="md-body-1">Стоимость {{ trainer.price ? trainer.price : 0 }}</div>
							<div v-if="trainer.description" class="md-body-1">{{ trainer.description }}</div>
							<div v-else class="md-body-1">Пользователь не оставил описания</div>
						</md-card-header-text>

						<md-card-media>
							<img src="http://vk.com/images/camera_b.gif" alt="Avatar">
						</md-card-media>
					</md-card-header>

					<md-card-actions>
						<md-button v-if="!trainer.request" @click="sendNotification(trainer.id, trainers.indexOf(trainer))">Отправить заявку</md-button>
						<span class="md-subheading" v-else>Вы уже отправляли зявку</span>
					</md-card-actions>
				</md-card>
			</div>
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
				trainers: []
			}
		},

		components: {
			Snackbar
		},

		methods: {
			fetchTrainers() {
				axios.get('/get_trainers')
					.then(response => {
						this.trainers = response.data.trainers
					})
			},

			sendNotification(id, index) {
				axios.post('/notifications/create_add_trainer_notification', {
					id: id
				})
					.then(response => {
						if (response.data.error) {
							this.$refs.snackbar.openSnackbar(response.data.error)
						} else {
							this.trainers[index].request = true
							this.$store.dispatch('userUpdate')

						}
					})
			}
		},

		created() {
			this.fetchTrainers()
		}
	}	
</script>