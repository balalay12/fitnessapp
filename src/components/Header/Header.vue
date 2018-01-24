<template>
    <div>

        <md-toolbar>
            <md-button class="md-icon-button" @click="openSidenav">
                <md-icon>menu</md-icon>
            </md-button>

            <router-link tag="h2" to="/" class="md-title" style="flex: 1">
                FitnessApp <span class="md-caption">PREalpha v.0.1.0</span>
            </router-link>

            <md-menu md-direction="bottom left" md-size="6">
                <md-button class="md-icon-button" md-menu-trigger>
                    <md-icon class="md-accent">notifications_active</md-icon>
                </md-button>

                <md-menu-content>
                    <md-list class="md-dense">
                        <md-list-item>
                            <span>Пользователь test хочет стать вашим клиентом</span>
                            <md-button class="md-icon-button md-list-action" @click="fetchNotificatins(1)">
                                <md-icon class="md-accent">delete</md-icon>
                            </md-button>
                        </md-list-item>
                        <md-divider></md-divider>
                        <md-list-item>
                            <span>Notification</span>
                            <md-button class="md-icon-button md-list-action" @click="fetchNotificatins(2)">
                                <md-icon class="md-accent">delete</md-icon>
                            </md-button>
                        </md-list-item>
                    </md-list>
                </md-menu-content>
            </md-menu>

        </md-toolbar>

        <Sidenav ref="sidenav"/>

    </div>
</template>

<script>
    import Sidenav from './Sidenav.vue'

    export default {
        components: {
            Sidenav
        },

        methods: {
            openSidenav() {
                this.$refs.sidenav.toggleLeftSidenav()
            },

            fetchNotificatins(n) {
                console.log('get notifications', n)
            }
        },

        mounted() {
            // this.fetchNotificatins()

            // setInterval(function() {
            //     this.fetchNotificatins()
            // }.bind(this), 1000)
        }
    }
</script>
