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

        <Snackbar ref="snackbar"/>

    </div>
</template>

<script>
    import axios from 'axios'
    import Snackbar from '../Snackbar.vue'
    import {dialogsControl} from '../mixins/dialogsControl'

    export default {
        props: ['programm', 'exercise'],

        mixins: [dialogsControl],

        components: {
            Snackbar
        },

        methods: {
            deleteExercise() {
                axios.post('/programms/delete_exercise', {
                    id: this.programm,
                    exercise_id: this.exercise
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$emit('fetchProgramms')
                            this.$refs.snackbar.openSnackbar('Удалено')
                        }
                    })
                this.closeDialog()
            }
        }
    }
</script>