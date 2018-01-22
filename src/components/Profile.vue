<template>
	<md-layout md-gutter md-align="center">
		<md-layout md-row md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">
			<md-list>
				<md-list-item>

					<md-avatar class="md-large">
					  	<img v-if="currentUser.data.photo" :src="currentUser.data.photo" alt="Avatar">
						<img v-else src="http://vk.com/images/camera_b.gif" alt="Avatar">
					</md-avatar>

					<span class="md-title">{{ currentUser.data.first_name }} {{ currentUser.data.last_name }}</span>

				</md-list-item>
			</md-list>
		</md-layout>

		<md-layout md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" md-gutter>
			<md-list>
				<md-list-item>
					<span v-if="currentUser.data.email">Email: {{ currentUser.data.email }}</span>
					<span v-else >Email: нет данных</span>
				</md-list-item>
				<md-list-item>
					<span v-if="currentUser.data.vk_id">VK: {{ currentUser.data.vk_id }}</span>
					<span v-else>VK: нет данных</span>
				</md-list-item>
			</md-list>
		</md-layout>

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