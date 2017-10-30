<template>
  <div>
    <!-- Edit exericse dialog -->
    <md-dialog ref="editExercise">
      <md-dialog-title>Изменить упражение</md-dialog-title>

      <md-dialog-content>
        <form>

          <ExerciseChoose v-model="new_exercise" ref="chooseExercise"></ExerciseChoose>

        </form>
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeDialog">Отмена</md-button>
        <md-button class="md-primary" @click="changeExercise">Изменить</md-button>
      </md-dialog-actions>
    </md-dialog>

    <Snackbar ref="snackbar"></Snackbar>
  </div>
</template>

<script>
import axios from 'axios'
import ExerciseChoose from '../ExerciseChoose.vue'
import Snackbar from '../Snackbar.vue'

export default {
  props: ['setId'],

  data() {
    return {
      new_exercise: ''
    }
  },

  components: {
      ExerciseChoose,
      Snackbar
  },

  methods: {
    openDialog() {
      this.$refs.editExercise.open()
    },
    closeDialog() {
      this.$refs.editExercise.close()
      this.$refs.chooseExercise.resetData()
      this.new_exercise = ''
    },
    changeExercise() {
      axios.post('/training/set/edit', {
        id: this.setId,
        exercise_id: this.new_exercise.id
      })
      .then(response => {
        if (response.data.error) {
          this.$refs.snackbar.openSnackbar(response.data.error)
        } else {
          this.$emit('fetchSetsByDate')
        }
      })
      this.closeDialog()
    },
  }
}
</script>