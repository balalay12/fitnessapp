<template>
	<md-layout md-gutter md-align="center">
		<md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">
			<h1 class="md-title text-content">Уведомления</h1>
			<div v-for="(notification, index) in notifications" :key="index">
				<md-card>
					<md-card-header>
						<md-card-header-text>
							<div class="md-boyd-1" v-if="notification.need_confirm">От: {{ notification.from.first_name }} {{ notification.from.last_name }}</div>
							<div class="md-body-1">{{ notification.message }}</div>
							<div class="md-body-1" v-if="notification.need_confirm">Here needed client's info</div>
						</md-card-header-text>

						<md-card-media>
							<img src="http://vk.com/images/camera_b.gif" alt="Avatar">
						</md-card-media>
					</md-card-header>

					<md-card-actions v-if="notification.need_confirm">
						<md-button >Отклонить</md-button>
						<md-button >Принять</md-button>
					</md-card-actions>
				</md-card>
			</div>

		</md-layout>
	</md-layout>
</template>

<script>
	import axios from 'axios'

	export default {
		data() {
			return {
			}
		},

		computed: {
			notifications() {
				return this.$store.getters.getNotifications
			}
		}
	}	
</script>