<template>
    <!-- Dialog for delete bodysize item -->
    <md-dialog ref="dialog">
        <md-dialog-title>Удаленние данных</md-dialog-title>

        <md-dialog-content>
            <p>Вы уверены что хотите удалить элемент?</p>
        </md-dialog-content>

        <md-dialog-actions>
            <md-button class="md-primary" @click="closeDialog">Отмена</md-button>
            <md-button class="md-primary" @click="deleteBodysize">Удалить</md-button>
        </md-dialog-actions>
    </md-dialog>
</template>

<script>
    import axios from 'axios'
    import {dialogsControl} from '../mixins/dialogsControl'

    export default {
        props: ['id', 'showDelete'],

        mixins: [dialogsControl],

        methods: {
            deleteBodysize() {
                axios.get(`/anthropometry/delete/${this.id}`)
                    .then(response => {
                        this.data = {}
                        this.$emit('fetchBodysize')
                        this.closeDialog()
                    })
            }
        }
    }
</script>