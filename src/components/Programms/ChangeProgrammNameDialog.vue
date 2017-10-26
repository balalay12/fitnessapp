<template>
	<div>
		<md-dialog ref="changeName">
			<md-dialog-title>
				Изменить название
			</md-dialog-title>

			<md-dialog-content>
				<form novalidate @submit.stop.prevent="submit">

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.sendName.$error }">
						<label>Название</label>
						<md-input type="text" v-model="name" @input="$v.sendName.$touch()" required></md-input>
						<span v-if="!$v.sendName.required" class="md-error">Поле обязательно</span>
					</md-input-container>

				</form>

			</md-dialog-content>

			<md-dialog-actions>
				<md-button class="md-primary" @click="closeDialog">Отмена</md-button>
				<md-button class="md-primary" @click="saveName">Сохранить</md-button>
			</md-dialog-actions>
		</md-dialog>

		<Snackbar ref="snackbar" />
	</div>
</template>

<script>
import axios from 'axios'
import { required } from 'vuelidate/lib/validators'
import Snackbar from '../Snackbar.vue'

export default {
	props: ['programmId', 'programmName'],

	data() {
		return {
			sendName: ''
		}
	},

	components: {
		Snackbar
	},

	computed: {
		name: {
			get() { 
				this.sendName = this.programmName
				return this.programmName 
			},
			set(val) {
				this.sendName = val
			}
		}
	},

	methods: {
		openDialog() {
			this.$refs.changeName.open()
		},
		saveName() {
			axios.post('/programms/edit', {
				id: this.programmId,
				name: this.sendName
			})
			.then(response => {
				if (response.data.error) {
        this.$refs.snackbar.openSnackbar(response.data.error)
      	} else {
					this.$emit('fetchProgramms')
					this.$refs.snackbar.openSnackbar('Сохранено')
				}
			})
			this.closeDialog()
		},
		closeDialog() {
			this.sendName = ''
			this.$refs.changeName.close()
		}
	},

	validations: {
			sendName: {
				required
			}
		},
}
</script>