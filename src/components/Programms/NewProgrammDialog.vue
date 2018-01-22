<template>
    <div>
        <!-- Add new programm dialog -->
        <md-dialog ref="newProgramm">
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

                    <ExerciseChoose v-model="exercise" ref="chooseExercise"/>

                    <md-button class="md-accent" :disabled="!exercise" @click="addExercise">Добавить</md-button>

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
                <md-button class="md-primary" @click="closeDialog">Отмена</md-button>
                <md-button class="md-primary" @click="saveNewProgramm">Сохранить</md-button>
            </md-dialog-actions>
        </md-dialog>

        <Snackbar ref="snackbar"/>

    </div>
</template>

<script>
    import axios from 'axios'
    import ExerciseChoose from '../ExerciseChoose.vue'
    import Snackbar from '../Snackbar.vue'
    import {required} from 'vuelidate/lib/validators'

    export default {
        data() {
            return {
                name: '',
                data: [],
                exercise: ''
            }
        },

        components: {
            ExerciseChoose,
            Snackbar
        },

        methods: {
            saveData(name, ids) {
                axios.post('/programms/add', {
                    name: name,
                    exercises: ids
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$emit('fetchProgramms')
                            this.$refs.snackbar.openSnackbar('Создано')
                            this.closeDialog()
                        }
                    })
            },

            openDialog() {
                this.$refs.newProgramm.open()
            },

            addExercise() {
                this.data.push(this.exercise)
                this.exercise = ''
                this.$refs.chooseExercise.resetExercise()
            },

            saveNewProgramm() {
                let exercises_ids = []
                this.data.forEach((item) => {
                    exercises_ids.push(item.id)
                })
                this.saveData(this.name, exercises_ids)
            },

            closeDialog() {
                this.data = []
                this.name = ''
                this.category = ''
                this.$refs.newProgramm.close()
            }
        },

        validations: {
            name: {
                required
            }
        },
    }
</script>