<template>
    <md-snackbar :md-position="vertical + ' ' + horizontal" ref="snackbar" :md-duration="duration">
        <span>{{ message }}</span>
        <md-button class="md-accent" @click="$refs.snackbar.close()">Закрыть</md-button>
    </md-snackbar>
</template>

<script>
    export default {
        data() {
            return {
                message: '',
                vertical: 'top',
                horizontal: 'right',
                duration: 4000,
            }
        },

        methods: {
            openSnackbar(msg) {
                this.message = msg
                this.$refs.snackbar.open()
            }
        }
    }
</script>