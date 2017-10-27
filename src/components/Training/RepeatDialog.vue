<template>
    <div>
        <md-dialog ref="repeatDialog">
            <md-dialog-title v-if="action === 'update'">Редактировать подход</md-dialog-title>
            <md-dialog-title v-else>Создать подход</md-dialog-title>

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
                <md-button class="md-primary" @click="closeDialog">Закрыть</md-button>
                <md-button v-if="action === 'update'" class="md-warn" @click="deleteRepeat">Удалить</md-button>
                <md-button v-if="action === 'update'" class="md-accent" @click="updateRepeat">Изменить</md-button>
                <md-button v-if="action === 'create'" class="md-accent" @click="createRepeat">Сохранить</md-button>
            </md-dialog-actions>
        </md-dialog>

        <Snackbar ref="snackbar"></Snackbar>
    </div>
</template>

<script>
    import axios from 'axios'
    import Snackbar from '../Snackbar.vue'

    export default {
        props: ['setId', 'repeatId', 'weightOld', 'countOld', 'action'],

        data() {
            return {
                sendCount: '',
                sendWeight: ''
            }
        },

        components: {
            Snackbar
        },

        computed: {
            count: {
                get() {
                    this.sendCount = this.countOld
                    return this.countOld
                },
                set(val) {
                    this.sendCount = val
                }
            },
            weight: {
                get() {
                    this.sendWeight = this.weightOld
                    return this.weightOld
                },
                set(val) {
                    this.sendWeight = val
                }
            }
        },

        methods: {
            openDialog() {
                this.$refs.repeatDialog.open()
            },
            closeDialog() {
                this.$refs.repeatDialog.close()
            },
            createRepeat() {
                axios.post('/training/repeat/add', {
                    id: this.setId,
                    weight: this.sendWeight,
                    count: this.sendCount
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$emit('fetchSetsByDate')
                        }
                    })
                this.closeDialog()
            },
            updateRepeat() {
                axios.post('/training/repeat/edit', {
                    id: this.repeatId,
                    weight: this.sendWeight,
                    count: this.sendCount
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$emit('fetchSetsByDate')
                        }
                    })
                this.closeDialog()
            },
            deleteRepeat() {
                axios.post('/training/repeat/delete', {
                    id: this.repeatId
                })
                    .then(response => {
                        if (response.data.error) {
                            this.$refs.snackbar.openSnackbar(response.data.error)
                        } else {
                            this.$emit('fetchSetsByDate')
                        }
                    })
                this.closeDialog()
            }
        }
    }
</script>