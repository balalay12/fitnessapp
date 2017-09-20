<template lang="html">
<md-stepper @completed="submit">

  <md-step  md-button-back="назад" md-button-continue="далее" :md-error="day.length === 0" :md-continue="day.length > 0">
    <md-layout md-align="center" >

      <md-layout md-tag="md-card" md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">
        
        <md-card-header>
          <div class="md-title">Новая тренировка</div>
        </md-card-header>

        <md-card-content>

          <md-input-container v-bind:class="{ 'md-input-invalid': $v.date.$error }">
            <label>Дата</label>
            <md-input name="date" v-model="date" type="date" @input="$v.date.$touch()" required></md-input>
            <span v-if="!$v.date.required" class="md-error">Поле обязательно</span>
          </md-input-container>

          <md-input-container>
            <label for="category">Категория</label>
            <md-select name="category" id="category" v-model="category">
              <md-option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</md-option>
            </md-select>
          </md-input-container>

          <md-input-container v-if="showExerciseField">
            <label for="exercise">Упражнение</label>
            <md-select name="exercise" id="exercise" v-model="exercise">
              <md-option v-for="ex in exercises" :key="ex.id" :value="ex">{{ ex.name }}</md-option>
            </md-select>
          </md-input-container>

          <md-input-container v-if="showExerciseField" v-bind:class="{ 'md-input-invalid': $v.weight.$error }">
            <label for="weight">Вес</label>
            <md-input name="weight" type="number" v-model="weight" @input="$v.weight.$touch()" required></md-input>
            <span v-if="!$v.weight.required" class="md-error">Поле обязательно</span>
            <span v-if="!$v.weight.numeric" class="md-error">
              Введите число.
            </span>
          </md-input-container>

          <md-input-container v-if="showExerciseField" v-bind:class="{ 'md-input-invalid': $v.reps.$error }">
            <label for="reps">Повторы</label>
            <md-input name="reps" type="number" v-model="reps" @input="$v.reps.$touch()" required></md-input>
            <span v-if="!$v.reps.required" class="md-error">Поле обязательно</span>
            <span v-if="!$v.reps.numeric" class="md-error">
              Введите число.
            </span>
          </md-input-container>

          <md-button :disabled="weight === '' || reps === ''" @click="addSet" v-if="showExerciseField">
            <md-icon>add_box</md-icon>
            подход
          </md-button>

          <md-table v-if="sets.length != 0">
            <md-table-header>
              <md-table-row>
                <md-table-head>Вес</md-table-head>
                <md-table-head>Повторы</md-table-head>
                <md-table-head></md-table-head>
              </md-table-row>
            </md-table-header>

            <md-table-body>
              <md-table-row v-for="(set, index) in sets" :key="index">
                <md-table-cell md-numeric>{{ set.weight }}</md-table-cell>
                <md-table-cell md-numeric>{{ set.count }}</md-table-cell>
                <md-table-cell md-numeric>
                  <md-button class="md-icon-button" @click="delRep(index)">
                    <md-icon>delete_forever</md-icon>
                  </md-button>
                </md-table-cell>
              </md-table-row>
            </md-table-body>
          </md-table>

          <md-layout v-if='errorsMsg.length != 0'>
            <md-list class="md-dense" v-for="msg in errorsMsg" :key="msg.id">
              <md-list-item><span class="md-error">{{ msg }}</span></md-list-item>
            </md-list>
          </md-layout>

        </md-card-content>

        <md-card-actions>
          <md-button :disabled="sets.length === 0" @click="add">Добавить</md-button>
        </md-card-actions>

        <!-- TODO пока что не использутеся -->
        <md-snackbar :md-position="vertical + ' ' + horizontal" ref="snackbar" :md-duration="duration">
          <span>{{ server_error }}</span>
          <md-button class="md-accent" @click="$refs.snackbar.close()">Закрыть</md-button>
        </md-snackbar>

      </md-layout>
    </md-layout>
  </md-step>

  <md-step :md-disabled="day.length === 0" :md-continue="day.length > 0" md-button-back="назад" md-button-continue="сохранить">
    <md-layout md-align="center" >
      <md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">

        <div v-for="training in day">
          <md-table-card>

            <md-toolbar>
              <h1 class="md-title">{{ training.exercise.name }}</h1>
              <md-button class="md-icon-button" id="editExerciseButton" @click="openExerciseDialog('editExercise', day.indexOf(training))">
                <md-icon>edit</md-icon>
              </md-button>
              <md-button class="md-icon-button" @click="deleteExercise(day.indexOf(training))">
                <md-icon>delete_forever</md-icon>
              </md-button>
            </md-toolbar>

            <md-table>
              <md-table-header>
                <md-table-row>
                  <md-table-head>Вес</md-table-head>
                  <md-table-head>Повторы</md-table-head>
                  <md-table-head></md-table-head>
                </md-table-row>
              </md-table-header>

              <md-table-body>
                <md-table-row v-for="(set, index) in training.sets" :key="index">
                  <md-table-cell md-numeric>{{ set.weight }}</md-table-cell>
                  <md-table-cell md-numeric>{{ set.count }}</md-table-cell>
                  <md-table-cell md-numeric>
                    <md-button class="md-icon-button" id="editRepButton" @click="openRepDialog('editRep', day.indexOf(training), index)">
                      <md-icon>edit</md-icon>
                    </md-button>
                  </md-table-cell>
                </md-table-row>
              </md-table-body>
            </md-table>

          </md-table-card>
        </div>

      </md-layout>
    </md-layout>
  </md-step>

  <!-- Edit repeat dialog in 2 step -->
  <md-dialog md-open-from="#editRepButton" md-close-to="#editRepButton" ref="editRep">
    <md-dialog-title>Редактировать подход</md-dialog-title>

    <md-dialog-content>
      <form>
        <md-input-container>
          <label>Вес</label>
          <md-input type="number" v-model="editData.weight"></md-input>
        </md-input-container>
        <md-input-container>
          <label>Повторения</label>
          <md-input type="number" v-model="editData.count"></md-input>
        </md-input-container>
      </form>
    </md-dialog-content>

    <md-dialog-actions>
      <md-button class="md-primary" @click="deleteRepDialog('editRep')">Удалить</md-button>
      <md-button class="md-primary" @click="saveRepDialog('editRep')">Изменить</md-button>
    </md-dialog-actions>
  </md-dialog>

  <!-- Edit exericse diaon on 2 step -->
  <md-dialog md-open-from="#editExerciseButton" md-close-to="#editExerciseButton" ref="editExercise">
    <md-dialog-title>Изменить упражение</md-dialog-title>

    <md-dialog-content>
      <form>
        <md-input-container>
          <label for="category">Категория</label>
          <md-select name="category" id="category" v-model="category">
            <md-option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</md-option>
          </md-select>
        </md-input-container>

        <md-input-container>
          <label for="exercise">Упражнение</label>
          <md-select name="exercise" id="exercise" v-model="exercise">
            <md-option v-for="ex in exercises" :key="ex.id" :value="ex">{{ ex.name }}</md-option>
          </md-select>
        </md-input-container>
      </form>
    </md-dialog-content>

    <md-dialog-actions>
      <md-button class="md-primary" @click="closeExerciseDialog('editExercise')">Отмена</md-button>
      <md-button class="md-primary" @click="saveExerciseDialog('editExercise')">Изменить</md-button>
    </md-dialog-actions>
  </md-dialog>

</md-stepper>

</template>

<script>
import axios from 'axios'
import { required, numeric } from 'vuelidate/lib/validators'

export default {

  data() {
    return {
      date: '',
      category: '',
      exercise: '',
      exercises: '',
      weight: '',
      reps: '',
      sets: [],
      showExerciseField: false,
      day: [],
      editData: {},

			errorsMsg: [],
			server_error: '',
      vertical: 'top',
      horizontal: 'right',
      duration: 4000
		}
	},

	methods: {
    submit() {
      console.log('submit -> ', this.day);
      axios.post('/api/set/add', {
        train: this.day
      })
      .then(response => {
        console.log(response);
      })
    },

		add() {
      this.day.push({
        date: this.date,
        exercise: this.exercise,
        sets: this.sets
      })
      this.exercise = ''
      this.sets = []
    },

    addSet() {
      this.sets.push({weight: this.weight, count: this.reps})
      this.weight = ''
      this.reps = ''
    },

    delRep(index) {
      this.sets.splice(index, 1)
    },

    openRepDialog(ref, dayIndex, repIndex) {
      this.editData = this.day[dayIndex].sets[repIndex]
      this.editData.dayIndex = dayIndex
      this.editData.repIndex = repIndex
      this.$refs[ref].open()
    },
    saveRepDialog(ref) {
      this.day[this.editData.dayIndex].sets[this.editData.repIndex].weight = this.editData.weight
      this.day[this.editData.dayIndex].sets[this.editData.repIndex].count = this.editData.count
      this.editData = ''
      this.$refs[ref].close()
    },
    deleteRepDialog(ref) {
      this.day[this.editData.dayIndex].sets.splice(this.editData.repIndex, 1)
      this.editData = ''
      this.$refs[ref].close()
    },
    deleteExercise(index) {
      this.day.splice(index, 1)
    },
    openExerciseDialog(ref, index) {
      console.log(index)
      this.editData.exerciseIndex = index
      this.$refs[ref].open()
    },
    saveExerciseDialog(ref) {
      this.day[this.editData.exerciseIndex].exercise = this.exercise
      this.editData = {}
      this.exercise = ''
      this.category = ''
      this.$refs[ref].close()
    },
    closeExerciseDialog(ref) {
      this.editData = {}
      this.exercise = ''
      this.category = ''
      this.$refs[ref].close()
    }
	},

  computed: {
    categories() {
      return this.$store.getters.categories
    },
    exercisesByCategoryId() {
      return this.$store.getters.exercisesByCategoryId
    }
  },

  watch: {
    category(val) {
      this.exercise = ''
      this.exercises = this.exercisesByCategoryId(val);
      this.showExerciseField = true
    }
  },

	validations: {
		date: {
      required
    },
    weight: {
      required,
      numeric
    },
    reps: {
      required,
      numeric
    }
	}
}
</script>

<style lang="css">
</style>
