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

		<md-layout md-collumn md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" md-gutter>
			<md-list>
				<md-list-item>
					<p v-if="currentUser.data.goal">Цель: {{ currentUser.data.goal }}</p>
					<span v-else>Цель будет напоминать вам о том, чего вы хотите добиться (а так же будет видна тренерам)</span>
					<md-button class="md-icon-button md-raised" @click="showGoalHandle">
						<md-icon>add</md-icon>
					</md-button>
				</md-list-item>
				<md-layout md-collumn v-if="showGoalForm">
					<md-input-container>
						<label>Цель</label>
						<md-textarea v-model="goal"></md-textarea>
					</md-input-container>
					<md-button class="md-raised" @click="showGoalHandle">Отменить</md-button>
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
			goal: ''
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
		showGoalHandle() {
			this.goal = this.currentUser.data.goal	
			this.showGoalForm = !this.showGoalForm
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
            		this.showGoalHandle()
            	}
			})
		}
	}
}
</script>