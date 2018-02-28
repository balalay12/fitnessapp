<template>
	<md-layout md-gutter md-align="center">
		<md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" >
			<h1 class="md-title text-content">Список клиентов</h1>
			<div v-for="(client, index) in clients" :key="index">
				<md-card>
					<md-card-header>
						<md-card-header-text>
							<div class="md-title">{{ client.first_name}} {{ client.last_name }}</div>
							<div v-if="client.description" class="md-body-1">{{ client.description }}</div>
							<div v-else class="md-body-1">Пользователь не оставил описания</div>
						</md-card-header-text>

						<md-card-media>
							<img src="http://vk.com/images/camera_b.gif" alt="Avatar">
						</md-card-media>
					</md-card-header>
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
				clients: []
			}
		},

		components: {
			Snackbar
		},

		methods: {
			fetchClients() {
				axios.get('/get_clients')
					.then(response => {
						this.clients = response.data.clients
					})
			}
		},

		created() {
			this.fetchClients()
		}
	}
</script>