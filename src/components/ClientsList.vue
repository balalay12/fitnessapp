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
					<md-card-actions>
						<md-button class="md-warn" @click="openDialog(client.id)">Отказаться</md-button>
						<md-button @click="clientTrainings(client.id)">Тренировки</md-button>
						<md-button @click="cleintAnthropometry(client.id)">Размеры</md-button>
					</md-card-actions>
				</md-card>
			</div>
		</md-layout>

		<md-dialog-confirm
			md-title="Удаление клинета"
			md-content="Вы уверены, что хотите отказаться от клиента?"
			md-ok-text="Да"
			md-cancel-text="Отмента"
			@close="onClose"
			ref="dialog">
		</md-dialog-confirm>

		<Snackbar ref="snackbar"></Snackbar>

	</md-layout>
</template>

<script>
	import axios from 'axios'
	import Snackbar from './Snackbar.vue'

	export default {
		data() {
			return {
				clients: [],
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
			},

			clientTrainings(id) {
				this.$router.push({ path: '/training', query: { id: id}})
			},

			cleintAnthropometry(id) {
				this.$router.push({ path: '/bodysize', query: { id: id}})
			},

			openDialog(id) {
				this.clientId = id
				this.$refs.dialog.open()
			},

			closeDialog() {
				this.clientId = ''
				this.$refs.dialog.close()
			},

			onClose(type) {
				if (type == 'ok') {
					axios.get(`/delete_client/${this.clientId}`)
					.then(response => {
						if (response.data.error) {
		            		this.$refs.snackbar.openSnackbar(response.data.error)
		            	} else {
		            		this.fetchClients()
            			}
					})
				}
			}
		},

		created() {
			this.fetchClients()
		}
	}
</script>