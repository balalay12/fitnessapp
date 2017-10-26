<template>
	<md-dialog ref="bodysizeDialog">
      <md-dialog-title>
				Размеры тела
      </md-dialog-title>

      <md-dialog-content>
       <form novalidate @submit.stop.prevent="submit">

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.data.neck.$error }">
						<label>Шея</label>
						<md-input type="number" v-model="data.neck" @input="$v.data.neck.$touch()"></md-input>
						<span v-if="!$v.data.neck.numeric" class="md-error">
              Введите число больше нуля.
            </span>
					</md-input-container>

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.data.chest.$error }">
						<label>Грудь</label>
						<md-input type="number" v-model="data.chest" @input="$v.data.chest.$touch()"></md-input>
						<span v-if="!$v.data.chest.numeric" class="md-error">
              Введите число больше нуля.
            </span>
					</md-input-container>

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.data.arm.$error }">
						<label>Бицепс</label>
						<md-input type="number" v-model="data.arm" @input="$v.data.arm.$touch()"></md-input>
						<span v-if="!$v.data.arm.numeric" class="md-error">
              Введите число больше нуля.
            </span>
					</md-input-container>

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.data.forearm.$error }">
						<label>Предплечье</label>
						<md-input type="number" v-model="data.forearm" @input="$v.data.forearm.$touch()"></md-input>
						<span v-if="!$v.data.forearm.numeric" class="md-error">
              Введите число больше нуля.
            </span>
					</md-input-container>

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.data.waist.$error }">
						<label>Талия</label>
						<md-input type="number" v-model="data.waist" @input="$v.data.waist.$touch()"></md-input>
						<span v-if="!$v.data.waist.numeric" class="md-error">
              Введите число больше нуля.
            </span>
					</md-input-container>

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.data.hip.$error }">
						<label>Бедро</label>
						<md-input type="number" v-model="data.hip" @input="$v.data.hip.$touch()"></md-input>
						<span v-if="!$v.data.hip.numeric" class="md-error">
              Введите число больше нуля.
            </span>
					</md-input-container>

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.data.shin.$error }">
						<label>Голень</label>
						<md-input type="number" v-model="data.shin" @input="$v.data.shin.$touch()"></md-input>
						<span v-if="!$v.data.shin.numeric" class="md-error">
              Введите число больше нуля.
            </span>
					</md-input-container>

				</form>
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeBodysizeDialog('bodysizeDialog')">Отмена</md-button>
        <md-button v-if="method === 'create'" class="md-primary" @click="saveBodysize('bodysizeDialog')">Сохранить</md-button>
        <md-button v-if="method === 'update'" class="md-primary" @click="updateBodysize('bodysizeDialog')">Обновить</md-button>
      </md-dialog-actions>
    </md-dialog>
</template>

<script>
	import axios from 'axios'
	import { numeric } from 'vuelidate/lib/validators'

	export default {
		props: ['method', 'data'],

		methods: {
			openDialog() {
	    	this.$refs.bodysizeDialog.open()
	    },
	    saveBodysize() {
	    	let send_data = {}
	    	// check null in value
				for (let item in this.data) {
					if (this.data[item]) {
						send_data[item] = this.data[item]
					}
				}
	    	axios.post('/anthropometry/add',
					send_data
				)
				.then(response => {
					this.$emit('fetchBodysize')
				})
				this.closeBodysizeDialog()
	    },
	    updateBodysize() {
	    	let send_data = {}
	    	// check null in value
				for (let item in this.data) {
					if (this.data[item]) {
						send_data[item] = this.data[item]
					}
				}
				axios.post('/anthropometry/edit', send_data)
				.then(response => {
					this.$emit('fetchBodysize')
				})
				this.closeBodysizeDialog()
	    },
	    closeBodysizeDialog() {
	    	this.$refs.bodysizeDialog.close()
	    }
		},

		validations: {
			data: {
				neck: {
					numeric
				},
				chest: {
					numeric
				},
				arm: {
					numeric
				},
				forearm: {
					numeric
				},
				waist: {
					numeric
				},
				hip: {
					numeric
				},
				shin: {
					numeric
				}
			}
		},
	}
</script>