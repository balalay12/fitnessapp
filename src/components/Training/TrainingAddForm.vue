<template lang="html">
<md-stepper @completed="submit">

  <md-step  md-button-back="назад" md-button-continue="далее" :md-error="day.length === 0" :md-continue="day.length > 0">
    <md-layout md-align="center" >

      <md-layout md-tag="md-card" md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">
        
        <md-card-header>
          <div class="md-title">Новая тренировка</div>
        </md-card-header>

        <md-card-content>

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

          <ExerciseChoose v-model="exercise" :category="category" ref="chooseExercise"></ExerciseChoose>

          <md-input-container v-bind:class="{ 'md-input-invalid': $v.weight.$error }">
            <label for="weight">Вес</label>
            <md-input name="weight" id="weight" type="number" v-model="weight" @input="$v.weight.$touch()" required></md-input>
            <span v-if="!$v.weight.numeric" class="md-error">
              Введите число больше нуля.
            </span>
          </md-input-container>

          <md-input-container v-bind:class="{ 'md-input-invalid': $v.count.$error }">
            <label for="count">Повторы</label>
            <md-input name="count" type="number" id="count" v-model="count" @input="$v.count.$touch()" required></md-input>
            <span v-if="!$v.count.numeric" class="md-error">
              Введите число больше нуля.
            </span>
          </md-input-container>

          <md-button :disabled="$v.weight.$invalid || $v.count.$invalid" @click="addSet">
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
          <md-button :disabled="sets.length === 0 || date === '' " @click="add">Добавить</md-button>
        </md-card-actions>

      </md-layout>
    </md-layout>
  </md-step>

  <md-step :md-disabled="day.length === 0" :md-continue="day.length > 0" md-button-back="назад" md-button-continue="сохранить">
    <md-layout md-align="center" >
      <md-layout md-column md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">

        <div v-for="training in day">
          <md-table-card>

            <md-toolbar>
              <h1 class="md-title">{{ russianDate(training.date) }} {{ training.exercise.name }}</h1>
              <md-button class="md-icon-button" id="addRepButton" @click="openAddRepeatDialog('addRep', day.indexOf(training))">
                <md-icon>add</md-icon>
              </md-button>
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
          <md-input type="number" v-model="buffer.weight"></md-input>
        </md-input-container>
        <md-input-container>
          <label>Повторения</label>
          <md-input type="number" v-model="buffer.count"></md-input>
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

  <!-- Add repeat dialog -->
  <md-dialog md-open-from="#addRepButton" md-close-to="#addRepButton" ref="addRep">
    <md-dialog-title>Добавить подход</md-dialog-title>

    <md-dialog-content>
      <form>
        <md-input-container>
          <label>Вес</label>
          <md-input type="number" v-model="weight"></md-input>
        </md-input-container>
        <md-input-container>
          <label>Повторения</label>
          <md-input type="number" v-model="count"></md-input>
        </md-input-container>
      </form>
    </md-dialog-content>

    <md-dialog-actions>
      <md-button class="md-primary" @click="closeAddRepeatDialog('addRep')">Закрыть</md-button>
      <md-button class="md-accent" @click="submitNewRepeat('addRep')">Сохранить</md-button>
    </md-dialog-actions>
  </md-dialog>

  <Snackbar ref="snackbar"></Snackbar>

</md-stepper>

</template>

<script>
import axios from 'axios'
import { required, numeric } from 'vuelidate/lib/validators'
import ExerciseChoose from '../ExerciseChoose.vue'
import Snackbar from '../Snackbar.vue'
// datepicker
import moment from 'moment'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import {Russian} from 'flatpickr/dist/l10n/ru'

moment.locale('ru')

export default {

  data() {
    return {
      date: null,
      category: '',
      exercise: '',
      exercises: '',
      weight: '',
      count: '',
      sets: [],
      day: [],
      buffer: {},
      errorsMsg: [],
      clientId: '',

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
    ExerciseChoose,
      Snackbar
  },

	methods: {
    russianDate(date) {
      return moment(date).format('D MMMM')
    },
    submit() {
        let sendData = []
        for (let index in this.day) {
            sendData.push({
                date: this.day[index].date,
                sets: this.day[index].sets,
                exercise: this.day[index].exercise.id
            })
        }
      axios.post('/training/set/add', {
        training: sendData,
        id: this.clientId
      })
      .then(response => {
        if (response.data.error) {
            this.$refs.snackbar.openSnackbar(response.data.error)
        } else {
          if (this.clientId) {
            this.$router.push({ path: '/training', query: { id: this.clientId}})
          } else {
            this.$router.push('/training')
          }
        }
      })
    },

	  add() {
      this.day.push({
        date: this.date,
        exercise: this.exercise,
        sets: this.sets
      })
      this.$refs.chooseExercise.resetExercise()
      this.exercise = ''
      this.sets = []
    },

    addSet() {
      this.sets.push({weight: this.weight, count: this.count})
      this.weight = ''
      this.count = ''
    },

    delRep(index) {
      this.sets.splice(index, 1)
    },

    openRepDialog(ref, dayIndex, repIndex) {
      this.buffer = this.day[dayIndex].sets[repIndex]
      this.buffer.dayIndex = dayIndex
      this.buffer.repIndex = repIndex
      this.$refs[ref].open()
    },
    saveRepDialog(ref) {
      this.day[this.buffer.dayIndex].sets[this.buffer.repIndex].weight = this.buffer.weight
      this.day[this.buffer.dayIndex].sets[this.buffer.repIndex].count = this.buffer.count
      this.buffer = ''
      this.$refs[ref].close()
    },
    deleteRepDialog(ref) {
      this.day[this.buffer.dayIndex].sets.splice(this.buffer.repIndex, 1)
      this.buffer = ''
      this.$refs[ref].close()
    },
    deleteExercise(index) {
      this.day.splice(index, 1)
    },
    openExerciseDialog(ref, index) {
      console.log(index)
      this.buffer.exerciseIndex = index
      this.$refs[ref].open()
    },
    saveExerciseDialog(ref) {
      this.day[this.buffer.exerciseIndex].exercise = this.exercise
      this.buffer = {}
      this.exercise = ''
      this.category = ''
      this.$refs[ref].close()
    },
    closeExerciseDialog(ref) {
      this.buffer = {}
      this.exercise = ''
      this.category = ''
      this.$refs[ref].close()
    },

    // add new repeat
    openAddRepeatDialog(ref, setId) {
        this.buffer.setId = setId
        this.$refs[ref].open()
    },
    closeAddRepeatDialog(ref) {
        this.weight = ''
        this.count = ''
        this.$refs[ref].close()
    },
    submitNewRepeat(ref) {
        this.day[this.buffer.setId].sets.push({weight: this.weight, count: this.count})
        this.weight = ''
        this.count = ''
        this.closeAddRepeatDialog(ref)
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
    }
  },

  created() {
    if (this.$route.query.id) {
      this.clientId = this.$route.query.id
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
    count: {
        required,
        numeric
    }
	}
}
</script>

<style lang="css">
</style>
