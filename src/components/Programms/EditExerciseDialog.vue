<template>
    <div>
        <!-- Edit exericse dialog -->
        <md-dialog ref="editExercise">
            <md-dialog-title>
                <span v-if="!exerciseId">Добавить упражение</span>
                <span v-else>Изменить упражение</span>
            </md-dialog-title>

            <md-dialog-content>
                <form>

                    <ExerciseChoose v-model="new_exercise" ref="chooseExercise"/>

                </form>
            </md-dialog-content>

            <md-dialog-actions>
                <md-button class="md-primary" @click="closeDialog">Отмена</md-button>
                <md-button v-if="!exerciseId" class="md-primary" @click="createExercise('editExercise')">Создать
                </md-button>
                <md-button v-else class="md-primary" @click="saveExerciseDialog">Изменить</md-button>
            </md-dialog-actions>
        </md-dialog>

        <Snackbar ref="snackbar"/>
    </div>
</template>

<script>
    import axios from 'axios'
    import ExerciseChoose from '../ExerciseChoose.vue'
    import Snackbar from '../Snackbar.vue'

    export default {
        props: ['programmId', 'exerciseId', 'category'],

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
            createExercise(ref) {
                axios.post('/programms/add_exercise', {
                    id: this.programmId,
                    new_exercise: this.new_exercise.id
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$emit('fetchProgramms')
                            this.$refs.snackbar.openSnackbar('Успешно')
                        }
                    })
                this.closeDialog()
            },
            saveExerciseDialog() {
                axios.post('/programms/edit_exercise', {
                    id: this.programmId,
                    old_exercise: this.exerciseId,
                    new_exercise: this.new_exercise.id
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$emit('fetchProgramms')
                            this.$refs.snackbar.openSnackbar('Успешно')
                        }
                    })
                this.closeDialog()
            },
        }
    }
</script>