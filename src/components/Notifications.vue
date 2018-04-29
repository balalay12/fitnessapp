<template>
	<md-layout md-gutter md-align="center">
		<md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">
			<h1 class="md-title text-content">Уведомления</h1>
			<div v-for="(notification, index) in notifications" :key="index">
				<md-card>
					<md-card-header>
						<md-card-header-text>
							<div class="md-body-1"> {{ notification.date }}</div>
							<div class="md-boyd-1" v-if="notification.need_confirm">От: {{ notification.from.first_name }} {{ notification.from.last_name }}</div>
							<div class="md-body-1">{{ notification.message }}</div>
							<div class="md-body-1" v-if="notification.need_confirm">Here needed client's info</div>
						</md-card-header-text>

						<md-card-media>
							<img src="http://vk.com/images/camera_b.gif" alt="Avatar">
						</md-card-media>
					</md-card-header>

					<md-card-actions v-if="notification.need_confirm || notification.status">
						<md-button v-if="notification.need_confirm" @click="decline(notification.id)">Отклонить</md-button>
						<md-button v-if="notification.need_confirm" @click="accept(notification.id)">Принять</md-button>
						<span v-if="notification.status" class="md-body-1">{{ notification.status }}</span>	
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
			}
		},

		components: {
			Snackbar
		},

		computed: {
			notifications() {
				return this.$store.getters.getNotifications
			}
		},

		methods: {
			accept(id) {
				axios.get(`/notifications/accept/${id}`)
					.then(response => {
						if (response.data.error) {
							this.$refs.snackbar.openSnackbar(response.data.error)
						} else {
							this.$store.dispatch('notificationsFetch')
						}
					})
			},
			decline(id) {
				axios.get(`/notifications/decline/${id}`)
					.then(response => {
						if (response.data.error) {
							this.$refs.snackbar.openSnackbar(response.data.error)
						} else {
							this.$store.dispatch('notificationsFetch')
						}
					})
			}	
		}
	}	
</script>