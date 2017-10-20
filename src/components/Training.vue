<template>

  <md-layout md-align="center" md-gutter>
    
    <md-layout md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" md-gutter>
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

    <md-layout md-flex="60" md-align="center" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" v-if="Object.keys(sets).length === 0">
      <span class="md-subheading">Здесь пока что ничего нет.</span>
    </md-layout>

    <md-layout v-else md-column md-flex="60" md-flex-medium="60" md-flex-small="90" md-flex-xsmall="90" v-for="(date, key, index) in sets" :key="index">
      <h2 class="md-title date">{{ russianDate(key) }}</h2>
      <md-table-card class="card-margin"  v-for="(set, index) in date" :key="index">
        <md-toolbar>
          <h1 class="md-title">{{ set.exercise.name }}</h1>
          <md-button class="md-icon-button" id="addRepButton" @click="openAddRepeatDialog('addRep', set.id)">
            <md-icon>add</md-icon>
          </md-button>
          <md-button class="md-icon-button" id="editExerciseButton" @click="openExerciseDialog('editExercise', key, index)">
            <md-icon>edit</md-icon>
          </md-button>
          <md-button class="md-icon-button" id="deleteExerciseButton" @click="openDeleteExercise('deleteExerciseDialog', key, index)">
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
                <md-button class="md-icon-button" @click="openRepDialog('editRep', rep.id, rep.weight, rep.count)">
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

    <!-- Edit repeat dialog -->
    <md-dialog md-open-from="#editRepButton" md-close-to="#editRepButton" ref="editRep">
      <md-dialog-title>Редактировать подход</md-dialog-title>

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
        <md-button class="md-primary" @click="closeRepDialog('editRep')">Закрыть</md-button>
        <md-button class="md-warn" @click="deleteRepDialog('editRep')">Удалить</md-button>
        <md-button class="md-accent" @click="saveRepDialog('editRep')">Изменить</md-button>
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

    <md-snackbar :md-position="vertical + ' ' + horizontal" ref="snackbar" :md-duration="duration">
      <span>{{ server_error }}</span>
      <md-button class="md-accent" @click="$refs.snackbar.close()">Закрыть</md-button>
    </md-snackbar>

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
      weight: '',
      count: '',
      buffer: {},
      server_error: '',
      vertical: 'top',
      horizontal: 'right',
      duration: 4000
    }
  },

  methods: {
    getAllSets() {
      axios.get('/training/sets')
      .then(response => {
        this.sets = response.data.sets
      })
    },
    getSetsByDate(month, year) {
      axios.get(`/training/set_by_date/${month+1}/${year}`)
      .then(response => {
        this.sets = response.data.sets
      })
    },
    russianDate(date) {
      return moment(date).format('D MMMM')
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
      axios.post('/training/set/delete', {
        id: this.sets[this.buffer.deleteKey][this.buffer.deleteIndex].id
      })
      .then(response => {
        if (response.data.error) {
          this.server_error = response.data.error
          this.closeDeleteExerciseDialog(ref)
          this.$refs.snackbar.open()
        } else {
          this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
        }
      })
      this.closeDeleteExerciseDialog(ref)
    },
    closeDeleteExerciseDialog(ref) {
      this.buffer = {}
      this.$refs[ref].close()
    },

    // edit exercise modal window
    openExerciseDialog(ref, key, index) {
      this.buffer.exerciseKey = key
      this.buffer.exerciseIndex = index
      this.$refs[ref].open()
    },
    saveExerciseDialog(ref) {
      axios.post('/training/set/edit', {
        id: this.sets[this.buffer.exerciseKey][this.buffer.exerciseIndex].id,
        exercise_id: this.exercise.id
      })
      .then(response => {
        if (response.data.error) {
          this.server_error = response.data.error
          this.closeExerciseDialog(ref)
          this.$refs.snackbar.open()
        } else {
          this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
        }
      })
      this.closeExerciseDialog(ref)
    },
    closeExerciseDialog(ref) {
      this.buffer = {}
      this.exercise = ''
      this.category = ''
      this.$refs[ref].close()
    },

    // edit or delete repeat modal window
    openRepDialog(ref, id, weight, count) {
      this.buffer.repeatId = id
      this.count = count
      this.weight = weight
      this.$refs[ref].open()
    },
    closeRepDialog(ref) {
      this.buffer = {}
      this.count = ''
      this.weight = ''
      this.$refs[ref].close()
    },
    deleteRepDialog(ref) {
      axios.post('/training/repeat/delete', {
        id: this.buffer.repeatId
      })
      .then(response => {
        if (response.data.error) {
          this.server_error = response.data.error
          this.closeRepDialog(ref)
          this.$refs.snackbar.open()
        } else {
          this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
        }
      })
      this.closeRepDialog(ref)
    },
    saveRepDialog(ref) {
      axios.post('/training/repeat/edit', {
        id: this.buffer.repeatId,
        weight: this.weight,
        count: this.count
      })
      .then(response => {
        if (response.data.error) {
          this.server_error = response.data.error
          this.closeRepDialog(ref)
          this.$refs.snackbar.open()
        } else {
          this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
        }
      })
      this.weight = ''
      this.count = ''
      this.closeRepDialog(ref)
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
      axios.post('/training/repeat/add', {
        id: this.buffer.setId,
        weight: this.weight,
        count: this.count
      })
      .then(response => {
        if (response.data.error) {
          this.server_error = response.data.error
          this.closeAddRepeatDialog(ref)
          this.$refs.snackbar.open()
        } else {
          this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
        }
      })
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
      this.showExerciseField = true
    }
  },

  created() {
    this.date = new Date()
    this.getAllSets()
  }
}
</script>

<style >
  #addBtn {
    position: fixed;
  }

  .card-margin {
    margin: 8px;
  }
</style>
