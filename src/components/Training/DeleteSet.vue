<template>
  <div>
    <!-- Dialog for delete exercise -->
    <md-dialog ref="dialog">
      <md-dialog-title>Удаление упражнения</md-dialog-title>

      <md-dialog-content>
        <p>Вы уверены что хотите удалить упражнение?</p>
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeDialog">Отмена</md-button>
        <md-button class="md-primary" @click="deleteExercise">Удалить</md-button>
      </md-dialog-actions>
    </md-dialog>

    <Snackbar ref="snackbar"></Snackbar>

  </div>
</template>

<script>
import axios from 'axios'
import Snackbar from '../Snackbar.vue'
import { dialogsControl } from '../mixins/dialogsControl'

export default {
  props: ['setId'],

  mixins: [dialogsControl],

  components: {
    Snackbar
  },

  methods: {
    deleteExercise(ref) {
      axios.post('/training/set/delete', {
        id: this.setId
      })
      .then(response => {
        if (response.data.error) {
            this.$refs.snackbar.openSnackbar(response.data.error)
        } else {
            this.$refs.snackbar.openSnackbar('Удалено')
            this.$emit('fetchSetsByDate')
        }
      })
      this.closeDialog()
    }
  }
}
</script>