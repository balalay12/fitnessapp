<template>
	<md-layout md-gutter md-align="center"md-column>

		<md-layout md-gutter md-column >
			<md-layout md-align="center" md-flex-large="90" md-flex-medium="90" md-flex-small="90" md-flex-xsmall="90">
				<h1 class="md-title">Программы тренировок</h1>
			</md-layout>
			<md-layout md-align="center">
				<p>Программы тренировок позволяют создать шаблоны ваших тренировочных дней. И позволят добавлять упражнения нажатием 2 кнопок.</p>
			</md-layout>	
		</md-layout>

		<md-layout md-align="center" md-flex-large="60" md-flex-medium="50" md-flex-small="100" md-flex-xsmall="100">
			<h1 class="md-subheading" v-if="programms.length === 0">Вы пока что ничего не добавили</h1>
			<md-layout class="card-margin" v-else v-for="(item, index) in programms" :key="index" md-column md-tag="md-table-card" md-align="center" md-flex-large="33" md-flex-medium="45" md-flex-small="100" md-flex-xsmall="100">

					<md-toolbar>
						<h1 class="md-title">{{ item.name }}</h1>
						<md-button class="md-icon-button">
	            <md-icon>assignment</md-icon>
	          </md-button>
						<md-button class="md-icon-button" @click="openNewExerciseDialog('editExercise', item.id)">
	            <md-icon>add</md-icon>
	          </md-button>
						<md-button class="md-icon-button" id="changeNameBtn" @click="openChangeNameDialog('changeName', item)">
	            <md-icon>edit</md-icon>
	          </md-button>
	          <md-button class="md-icon-button" id="deleteProgrammButton" @click="openDeleteProgrammDialog('deleteProgrammDialog', item.id)">
	            <md-icon>delete_forever</md-icon>
	          </md-button>
					</md-toolbar>

					<md-table>
						<md-table-header>
							<md-table-head>#</md-table-head>
							<md-table-head>Упражнение</md-table-head>
							<md-table-head></md-table-head>
						</md-table-header>

						<md-table-body>

							<md-table-row v-for="(exercise, exIndex) in item.exercises" :key="exIndex">
								<md-table-cell>{{ exIndex + 1}}</md-table-cell>
								<md-table-cell>{{ exercise.name }}</md-table-cell>
								<md-table-cell>
									<md-button class="md-icon-button" id="editExerciseButton" @click="openExerciseDialog('editExercise', item.id, exercise)">
				            <md-icon>edit</md-icon>
				          </md-button>
				          <md-button class="md-icon-button" id="deleteExerciseButton" @click="openDeleteExerciseDialog('deleteExercise', item.id, exercise.id)">
				            <md-icon>delete_forever</md-icon>
				          </md-button>
								</md-table-cell>
							</md-table-row>

						</md-table-body>
					</md-table>

			</md-layout>
		</md-layout>

		<!-- Add new programm dialog -->
		<md-dialog md-open-from="#addBtn" md-close-to="#addBtn" ref="newProgramm">
			<md-dialog-title>
				Новая программа тренировок
			</md-dialog-title>

			<md-dialog-content>
				<form novalidate @submit.stop.prevent="submit">

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.name.$error }">
						<label>Название</label>
						<md-input type="text" v-model="name" @input="$v.name.$touch()" required></md-input>
						<span v-if="!$v.name.required" class="md-error">Поле обязательно</span>
					</md-input-container>

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

          <md-button class="md-accent" @click="addExercise">Добавить</md-button>

				</form>

				<md-table v-if="data.length != 0">
					<md-table-header>
						<md-table-row>
							<md-table-head>#</md-table-head>
							<md-table-head>Упражение</md-table-head>
						</md-table-row>
					</md-table-header>

					<md-table-body>
						<md-table-row v-for="(item, index) in data" :key="index">
							<md-table-cell>{{ index + 1}}</md-table-cell>
							<md-table-cell>{{ item.name }}</md-table-cell>
						</md-table-row>
					</md-table-body>
				</md-table>

			</md-dialog-content>

			<md-dialog-actions>
				<md-button class="md-primary" @click="closeNewProgramm('newProgramm')">Отмена</md-button>
				<md-button class="md-primary" @click="saveNewProgramm('newProgramm')">Сохранить</md-button>
			</md-dialog-actions>
		</md-dialog>

		<!-- Change programm's name -->
		<md-dialog md-open-from="#changeNameBtn" md-close-to="#changeNameBtn" ref="changeName">
			<md-dialog-title>
				Изменить название
			</md-dialog-title>

			<md-dialog-content>
				<form novalidate @submit.stop.prevent="submit">

					<md-input-container v-bind:class="{ 'md-input-invalid': $v.name.$error }">
						<label>Название</label>
						<md-input type="text" v-model="name" @input="$v.name.$touch()" required></md-input>
						<span v-if="!$v.name.required" class="md-error">Поле обязательно</span>
					</md-input-container>

				</form>

			</md-dialog-content>

			<md-dialog-actions>
				<md-button class="md-primary" @click="closeChangeNameDialog('changeName')">Отмена</md-button>
				<md-button class="md-primary" @click="saveName('changeName')">Сохранить</md-button>
			</md-dialog-actions>
		</md-dialog>

		<!-- Dialog for delete programm -->
		<md-dialog md-open-from="#deleteProgrammButton" md-close-to="#deleteProgrammButton" ref="deleteProgrammDialog">
      <md-dialog-title>Удаление программы</md-dialog-title>

      <md-dialog-content>
       <p>Вы уверены что хотите удалить программу?</p> 
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeDeleteProgrammDialog('deleteProgrammDialog')">Отмена</md-button>
        <md-button class="md-primary" @click="deleteProgramm('deleteProgrammDialog')">Удалить</md-button>
      </md-dialog-actions>
    </md-dialog>

    <!-- Dialog for delete exercise -->
    <md-dialog md-open-from="#deleteExerciseButton" md-close-to="#deleteExerciseButton" ref="deleteExercise">
      <md-dialog-title>Удаление упражнения</md-dialog-title>

      <md-dialog-content>
       <p>Вы уверены что хотите удалить упражнение?</p> 
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeDeleteExerciseDialog('deleteExercise')">Отмена</md-button>
        <md-button class="md-primary" @click="deleteExercise('deleteExercise')">Удалить</md-button>
      </md-dialog-actions>
    </md-dialog>

    <!-- Edit exericse diaon -->
    <md-dialog md-open-from="#editExerciseButton" md-close-to="#editExerciseButton" ref="editExercise">
      <md-dialog-title>
      	<span v-if="new_exercise">Добавить упражение</span>
      	<span v-else>Изменить упражение</span>
      </md-dialog-title>

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
        <md-button v-if="new_exercise" class="md-primary" @click="createExercise('editExercise')">Создать</md-button>
        <md-button v-else class="md-primary" @click="saveExerciseDialog('editExercise')">Изменить</md-button>
      </md-dialog-actions>
    </md-dialog>

		<md-button id="addBtn" class="md-fab md-fab-bottom-right" @click="openNewProgramm('newProgramm')">
      <md-icon>add</md-icon>
    </md-button>

    <!-- Show messages (errors) -->
    <md-snackbar :md-position="vertical + ' ' + horizontal" ref="snackbar" :md-duration="duration">
	    <span>{{ message }}</span>
	    <md-button class="md-accent" @click="$refs.snackbar.close()">Закрыть</md-button>
	  </md-snackbar>

	</md-layout>
</template>

<script>
	import axios from 'axios'
	import { required, alphaNum } from 'vuelidate/lib/validators'

	export default {
		data() {
			return {
				name: '',
				exercises: '',
				exercise: '',
				category: '',
				data: [],
				programms: [],
				current_programm_id: '',
				new_exercise_id: '',
				current_exercise_id: '',
				new_exercise: false,

				// snackbar variables
				message: '',
	      vertical: 'top',
	      horizontal: 'right',
	      duration: 4000
			}
		},

		methods: {
			fetchData() {
				axios.get('/programms/')
				.then(response => {
					this.programms = response.data.programms
				})
			},
			saveData(ref, name, ids) {
				axios.post('/programms/add', {
					name: name,
					exercises: ids
				})
				.then(response => {
					if (response.data.error) {
          	this.message = response.data.error
          	this.$refs.snackbar.open()
        	} else {
						this.fetchData()
						this.message = 'Создано'
						this.$refs.snackbar.open()
						this.closeNewProgramm(ref)
					}
				})
			},

			// open newProgramm dialog
			openNewProgramm(ref) {
				this.$refs[ref].open()
			},
			addExercise() {
				this.data.push(this.exercise)
				this.exercise = ''
			},
			saveNewProgramm(ref) {
				let exercises_ids = []
				this.data.forEach((item) => {
					exercises_ids.push(item.id)
				})
				this.saveData(ref, this.name, exercises_ids)
			},
			closeNewProgramm(ref) {
				this.data = []
				this.name = ''
				this.category = ''
				this.$refs[ref].close()
			},

			// changeName dialog
			openChangeNameDialog(ref, item) {
				this.current_programm_id = item.id;
				this.name = item.name
				this.$refs[ref].open()
			},
			saveName(ref) {
				axios.post('/programms/edit', {
					id: this.current_programm_id,
					name: this.name
				})
				.then(response => {
					if (response.data.error) {
          this.message = response.data.error
          this.$refs.snackbar.open()
        	} else {
						this.fetchData()
						this.message = 'Сохранено'
						this.$refs.snackbar.open()
					}
				})
				this.closeChangeNameDialog(ref)
			},
			closeChangeNameDialog(ref) {
				this.current_programm_id = ''
				this.name = ''
				this.$refs[ref].close()
			},

			// delete programm dialog
			openDeleteProgrammDialog(ref, id) {
				this.current_programm_id = id;
				this.$refs[ref].open()
			},
			deleteProgramm(ref) {
				axios.post('/programms/delete', {
					id: this.current_programm_id
				})
				.then(response => {
					if (response.data.error) {
          this.message = response.data.error
          this.$refs.snackbar.open()
        	} else {
						this.fetchData()
						this.message = 'Удалено'
						this.$refs.snackbar.open()
					}
				})
				this.closeDeleteProgrammDialog(ref)
			},
			closeDeleteProgrammDialog(ref) {
				this.current_programm_id = ''
				this.$refs[ref].close()
			},

			// edit exercise modal window
	    openExerciseDialog(ref, programm_id, exercise) {
	    	this.current_programm_id = programm_id
    		this.current_exercise_id = exercise.id
    		this.category = exercise.category.id
	      this.$refs[ref].open()
	    },
	    // open exercise dialog for add new exercise to programm
	    // we need only programm id for that
	    openNewExerciseDialog(ref, programm_id) {
	    	this.current_programm_id = programm_id
	    	this.new_exercise = true
	    	this.$refs[ref].open()
	    },
	    createExercise(ref) {
	    	axios.post('/programms/add_exercise', {
	    		id: this.current_programm_id,
	    		new_exercise: this.exercise.id
	    	})
	    	.then(response => {
	    		if (response.data.error) {
          this.message = response.data.error
          this.$refs.snackbar.open()
        	} else {
	    			this.fetchData()
	    			this.message = 'Успешно'
						this.$refs.snackbar.open()
	    		}
	    	})
	      this.closeExerciseDialog(ref)
	    },
	    saveExerciseDialog(ref) {
	    	axios.post('/programms/edit_exercise', {
	    		id: this.current_programm_id,
	    		old_exercise: this.current_exercise_id,
	    		new_exercise: this.exercise.id
	    	})
	    	.then(response => {
	    		if (response.data.error) {
          this.message = response.data.error
          this.$refs.snackbar.open()
        	} else {
	    			this.fetchData()
	    			this.message = 'Успешно'
						this.$refs.snackbar.open()
	    		}
	    	})
	      this.closeExerciseDialog(ref)
	    },
	    closeExerciseDialog(ref) {
	    	this.current_programm_id = ''
	    	this.category = ''
	    	this.exercise = ''
	    	this.current_exercise_id = ''
	    	this.new_exercise = false
	      this.$refs[ref].close()
	    },

	    // delete exercise dialog
	    openDeleteExerciseDialog(ref, programm_id, exercise_id) {
	    	this.current_programm_id = programm_id
	    	this.current_exercise_id = exercise_id
	    	this.$refs[ref].open()
	    },
	    deleteExercise(ref) {
	    	axios.post('/programms/delete_exercise', {
	    		id: this.current_programm_id,
	    		exercise_id: this.current_exercise_id
	    	})
	    	.then(response => {
	    		if (response.data.error) {
          this.message = response.data.error
          this.$refs.snackbar.open()
        	} else {
	    			this.fetchData()
	    			this.message = 'Удалено'
						this.$refs.snackbar.open()
	    		}
	    	})
	    	this.closeDeleteExerciseDialog(ref)
	    },
	    closeDeleteExerciseDialog(ref) {
	    	this.current_programm_id = ''
	    	this.current_exercise_id = ''
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
				this.exercises = this.exercisesByCategoryId(val)
			}
		},

		validations: {
			name: {
				required
			}
		},

		created() {
			this.fetchData()
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
