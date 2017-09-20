<template>

  <md-layout md-align="center" md-gutter>
    
    <md-layout md-flex="60" md-flex-medium="60" md-flex-small="90" md-flex-xsmall="90" md-gutter>
      <md-layout>
        <md-button @click="dateDecrement">
          <md-icon>keyboard_arrow_left</md-icon>
        </md-button>
      </md-layout>
      <md-layout md-align="center" md-vertical-align="center">
        <span class="md-subheading">{{ currentMonth(date) }} </span>
      </md-layout>
      <md-layout md-align="end">
        <span flex></span>
        <md-button @click="dateIncrement">
          <md-icon>keyboard_arrow_right</md-icon>
        </md-button>
      </md-layout>
    </md-layout>

    <md-layout md-flex="60" md-align="center" md-flex-medium="60" md-flex-small="90" md-flex-xsmall="90" v-if="Object.keys(sets).length === 0">
      <span class="md-subheading">Здесь пока что ничего нет.</span>
    </md-layout>

    <md-layout v-else md-column md-flex="60" md-flex-medium="60" md-flex-small="90" md-flex-xsmall="90" v-for="(date, key, index) in sets" :key="index">
      <h2 class="md-title date">{{ russianDate(key) }}</h2>
      <md-table-card v-for="(set, index) in date" :key="index">
        <md-toolbar>
          <h1 class="md-title">{{ set.exercise.name }}</h1>
          <md-button class="md-icon-button" id="editExerciseButton" @click="openExerciseDialog('editExercise',key, index)">
                <md-icon>edit</md-icon>
              </md-button>
              <md-button class="md-icon-button" id="deleteExerciseButton" @click="openDeleteExercise('deleteExerciseDialog',key, index)">
                <md-icon>delete_forever</md-icon>
              </md-button>
        </md-toolbar>

        <md-table>
          <md-table-header>
            <md-table-row>
              <md-table-head>#</md-table-head>
              <md-table-head>Вес</md-table-head>
              <md-table-head>Повторы</md-table-head>
              <md-table-head></md-table-head>
            </md-table-row>
          </md-table-header>

          <md-table-body>
            <md-table-row v-for="(rep, index) in set.repeats" :key="index">
              <md-table-cell>{{ index + 1}}</md-table-cell>
              <md-table-cell md-numeric>{{ rep.weight }}</md-table-cell>
              <md-table-cell md-numeric>{{ rep.count }}</md-table-cell>
              <md-table-cell md-numeric>
                <md-button class="md-icon-button" @click="test(rep)">
                  <md-icon>edit</md-icon>
                </md-button>
              </md-table-cell>
            </md-table-row>
          </md-table-body>
        </md-table>
      </md-table-card>
    </md-layout>

    <router-link tag="md-button" to="/training/add" id="addBtn" class="md-fab md-fab-bottom-right">
      <md-icon>add</md-icon>
    </router-link>

    <md-dialog md-open-from="#deleteExerciseButton" md-close-to="#deleteExerciseButton" ref="deleteExerciseDialog">
      <md-dialog-title>Удалить упражение</md-dialog-title>

      <md-dialog-content>
       <p>Вы уверены что хотите удалить упражнение?</p> 
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeExerciseDialog('deleteExerciseDialog')">Отмена</md-button>
        <md-button class="md-primary" @click="deleteExercise('deleteExerciseDialog')">Удалить</md-button>
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

  </md-layout>

</template>

<script>
import axios from 'axios'
import moment from 'moment'

moment.locale('ru')

export default {
  data() {
    return {
      date: '',
      sets: '',
      category: '',
      exercise: '',
      exercises: '',
      buffer: {}
    }
  },

  methods: {
    test(index) {
      console.log('test ', index);
    },
    getSetsByDate(month, year) {
      axios.get(`/api/set_by_date/${month+1}/${year}`)
      .then(response => {
        this.sets = response.data.sets
      })
    },
    russianDate(date) {
      return moment(date).format('D MMMM YYYY')
    },
    currentMonth(date) {
      return moment(date).format('MMMM YYYY')
    },
    dateIncrement() {
      this.date = moment(this.date).add(1, 'M')
      this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
    },
    dateDecrement() {
      this.date = moment(this.date).subtract(1, 'M')
      this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
    },
    // delete exercise modal window
    openDeleteExercise(ref, key, index) {
      this.$refs[ref].open()
      this.buffer.deleteKey = key
      this.buffer.deleteIndex = index
    },
    deleteExercise(ref) {
      // TODO удаление упражнения на сервере
      console.log(this.sets[this.buffer.deleteKey][this.buffer.deleteIndex].id, 'упражнение было удалено якобы')
      this.buffer = {}
      this.$refs[ref].close()
    },
    closeDeleteExerciseDialog(ref) {
      this.buffer = {}
      this.$refs[ref].close()
    },
    // edit exercise modal window
    openExerciseDialog(ref, key, index) {
      console.log(index)
      this.buffer.exerciseKey = key
      this.buffer.exerciseIndex = index
      this.$refs[ref].open()
    },
    saveExerciseDialog(ref) {
      // this.day[this.editData.exerciseIndex].exercise = this.exercise
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

  created() {
    this.date = new Date()
    axios.get('/api/sets')
    .then(response => {
      this.sets = response.data.sets
    })
  }
}
</script>

<style >
  #addBtn {
    position: fixed;
  }

  .date {
    /*text-align: center;*/
  }
</style>
