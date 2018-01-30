<template>
    <div>

        <md-toolbar>
            <md-button class="md-icon-button" @click="openSidenav">
                <md-icon>menu</md-icon>
            </md-button>

            <router-link tag="h2" to="/" class="md-title" style="flex: 1">
                FitnessApp <span class="md-caption">PREalpha v.0.1.0</span>
            </router-link>
            <md-button v-if="!newNotifications" class="md-icon-button" md-menu-trigger>
                <md-icon>notifications_active</md-icon>
            </md-button>

            <md-menu v-else md-direction="bottom left" md-size="6">
                <md-button class="md-icon-button" md-menu-trigger>
                    <md-icon class="md-accent">notifications_active</md-icon>
                </md-button>

                <md-menu-content>
                    <md-list class="md-dense">
                        <md-list-item @click="hideNotify">
                            <span>У вас есть новые уведомления</span>
                        </md-list-item>
                    </md-list>
                </md-menu-content>
            </md-menu>

        </md-toolbar>

        <Snackbar ref="snackbar"></Snackbar>

        <Sidenav ref="sidenav"/>

    </div>
</template>

<script>
    import axios from 'axios'
    import Sidenav from './Sidenav.vue'
    import Snackbar from '../Snackbar.vue'

    export default {
        data() {
            return {
                newNotifications: false     
            }
        },

        components: {
            Sidenav,
            Snackbar
        },

        methods: {
            openSidenav() {
                this.$refs.sidenav.toggleLeftSidenav()
            },

            hideNotify() {
                this.newNotifications = false
            },

            fetchNewNotificatins() {
                axios.get('/notifications/new')
                    .then(response => {
                        if (response.data.notifications.length > 0) {
                            this.newNotifications = true
                            this.$refs.snackbar.openSnackbar("У вас новые уведомления")
                            this.$store.dispatch('notificationsUpdate', response.data.notifications)
                        }
                    })
            }
        },

        mounted() {
            this.fetchNewNotificatins()

            setInterval(function() {
                this.fetchNewNotificatins()
            }.bind(this), 10000)
        }
    }
</script>
