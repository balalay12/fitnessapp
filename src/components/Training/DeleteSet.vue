<template>
    <div>
        <!-- Dialog for delete exercise -->
        <md-dialog ref="deleteExercise">
            <md-dialog-title>Удаление упражнения</md-dialog-title>

            <md-dialog-content>
                <p>Вы уверены что хотите удалить упражнение?</p>
            </md-dialog-content>

            <md-dialog-actions>
                <md-button class="md-primary" @click="closeDialog">Отмена</md-button>
                <md-button class="md-primary" @click="deleteExercise">Удалить</md-button>
            </md-dialog-actions>
        </md-dialog>

        <Snackbar ref="snackbar"></Snackbar>

    </div>
</template>

<script>
    import axios from 'axios'
    import Snackbar from '../Snackbar.vue'

    export default {
        props: ['setId'],

        components: {
            Snackbar
        },

        methods: {
            openDialog() {
                this.$refs.deleteExercise.open()
            },
            deleteExercise(ref) {
                axios.post('/training/set/delete', {
                    id: this.setId
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$refs.snackbar.openSnackbar('Удалено')
                            this.$emit('fetchSetsByDate')
                        }
                    })
                this.closeDialog()
            },
            closeDialog() {
                this.$refs.deleteExercise.close()
            },
        }
    }
</script>