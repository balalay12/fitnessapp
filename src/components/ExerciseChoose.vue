<template>
	<div>
		<md-input-container>
      <label for="category">Категория</label>
      <md-select name="category" id="category" v-model="category">
        <md-option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</md-option>
      </md-select>
    </md-input-container>

    <md-input-container>
      <label for="exercise">Упражнение</label>
      <md-select name="exercise" id="exercise" v-model="exercise" @change="selectedExercise">
        <md-option v-for="ex in exercises" :key="ex.id" :value="ex">{{ ex.name }}</md-option>
      </md-select>
    </md-input-container>
	</div>
</template>

<script>
	export default {

		data() {
			return {
				exercises: '',
				exercise: '',
				category: ''
			}
		},

		methods: {
			selectedExercise(val) {
				this.$emit('input', val)
			},
			resetData() {
				this.exercise = ''
				this.exercises = ''
				this.category = ''
			},
			resetExercise() {
				this.exercise = ''
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
		}
	}
</script>