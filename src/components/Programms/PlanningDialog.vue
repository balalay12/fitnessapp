<template>
	<div>
		<!-- Dialog for planing traing from programm -->
	  <md-dialog ref="planningDialog">
	  	<md-dialog-title>
	  		<span class="md-title">Запланировать тренировку</span>
	  	</md-dialog-title>
	  		
	  	<md-dialog-content>
	  		<p>Выберите дату на которую хотите запланировать тренировку.</p>
	  		<md-input-container :class="date ? 'md-has-value' : ''">
	        <label>Дата</label>
	        <flat-pickr
	          v-model="date"
	          :config="config"
	          :required="true" 
	          :inputClass="'md-input'"                         
	          name="date">
	        </flat-pickr>
	      </md-input-container>		
	  	</md-dialog-content>

	  	<md-dialog-actions>
	  		<md-button class="md-primary" @click="closeDialog">Отмена</md-button>
	  		<md-button class="md-primary" @click="planningSave()">Запланировать</md-button>
	  	</md-dialog-actions>
	  </md-dialog>

	  <Snackbar ref="snackbar" />
  </div>
</template>

<script>
	import axios from 'axios'
	import Snackbar from '../Snackbar.vue'
	import flatPickr from 'vue-flatpickr-component'
	import 'flatpickr/dist/flatpickr.css'
	import {Russian} from 'flatpickr/dist/l10n/ru'

	export default {
		props: ['id'],

		data() {
			return {
				date: null,
				config: {
	        altFormat: 'd.m.Y',
	        altInput: true,
	        dateFormat: 'Y-m-d',
	        locale: Russian,
	        disableMobile: true
	      }
			}
		},

		components: {
	    flatPickr,
	    Snackbar
	  },

		methods: {
			openDialog() {
				console.log(this.id)
				this.$refs.planningDialog.open()
			},
			closeDialog() {
				this.$refs.planningDialog.close()
			},
			planningSave() {
	    	axios.post('/training/planning', {
	    		'programm_id': this.id,
	    		'date': this.date
	    	})
	    	.then(response => {
	    		if (response.data.error) {
          this.$refs.snackbar.openSnackbar(response.data.error)
        	} else {
						this.$refs.snackbar.openSnackbar('Тренировка успешно запланирована.')
	    		}
	    		this.closeDialog()
	    	})
	    },
		}
	}
</script>