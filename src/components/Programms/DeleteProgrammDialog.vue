<template>
	<div>
		<!-- Dialog for delete exercise -->
    <md-dialog ref="dialog">
      <md-dialog-title>Удаление программы</md-dialog-title>

      <md-dialog-content>
       <p>Вы уверены что хотите удалить программу?</p> 
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeDialog">Отмена</md-button>
        <md-button class="md-primary" @click="deleteProgramm">Удалить</md-button>
      </md-dialog-actions>
    </md-dialog>

    <Snackbar ref="snackbar" />

	</div>
</template>

<script>
import axios from 'axios'
import Snackbar from '../Snackbar.vue'
import { dialogsControl } from '../mixins/dialogsControl'

export default {
	props: ['programm'],

  mixins: [dialogsControl],

	components: {
		Snackbar
	},

	methods: {
    deleteProgramm() {
      axios.post('/programms/delete', {
        id: this.programm
      })
      .then(response => {
        if (response.data.error) {
        this.$refs.snackbar.openSnackbar(response.data.error)
        } else {
          this.$emit('fetchProgramms')
          this.$refs.snackbar.openSnackbar('Удалено')
        }
      })
      this.closeDialog()
    }
	}
}
</script>