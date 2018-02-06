<template>
    <md-sidenav class="md-left md-fixed" ref="leftSidenav" md-swipeable>
        <md-toolbar v-if="currentUser.is_auth" class="md-account-header">
            <md-list class="md-transparent">
                <md-list-item class="md-avatar-list" @click="linkToProfile">
                    <md-avatar class="md-large">
                        <img v-if="currentUser.data.photo" :src="currentUser.data.photo" alt="Avatar">
                        <img v-else src="http://vk.com/images/camera_b.gif" alt="Avatar">
                    </md-avatar>
                </md-list-item>
                <md-list-item>
                    <div class="md-list-text-container">
                        <span>{{ currentUser.data.first_name }} {{ currentUser.data.last_name }}</span>
                        <span v-if="currentUser.data.role == 'user'">   Пользователь
                        </span>
                    </div>
                </md-list-item>
            </md-list>
        </md-toolbar>

        <md-toolbar v-else>
            <h3 class="md-title">Вы не авторизованы</h3>
        </md-toolbar>

        <md-list v-if="currentUser.is_auth">
            <router-link v-if="!currentUser.data.trainer" tag="md-list-item" to="/trainers">
                Поиск тренера 
            </router-link>
            <router-link tag="md-list-item" to="/notifications">
                Уведомления
            </router-link>
            <router-link tag="md-list-item" to="/training">
                Тренировки
            </router-link>
            <router-link tag="md-list-item" to="/programms">
                Программы тренировок
            </router-link>
            <router-link tag="md-list-item" to="/bodysize">
                Размеры тела
                <md-divider></md-divider>
            </router-link>
            <md-list-item @click="logout">
                <span>Выход</span>
            </md-list-item>
        </md-list>
    </md-sidenav>
</template>

<script>
    import axios from 'axios'

    export default {

        methods: {
            toggleLeftSidenav() {
                this.$refs.leftSidenav.toggle();
            },
            linkToProfile() {
                this.$router.push('/profile')
            },
            logout() {
                axios.get('/logout')
                    .then(response => {
                        this.$store.dispatch('userLogout')
                    })
            }
        },

        computed: {
            currentUser() {
                return this.$store.getters.currentUser
            }
        }
    }
</script>