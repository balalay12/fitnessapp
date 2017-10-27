<template>

    <md-layout md-align="center" md-gutter>

        <md-layout md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100" md-gutter>
            <md-layout>
                <md-button @click="dateDecrement">
                    <md-icon>keyboard_arrow_left</md-icon>
                </md-button>
            </md-layout>
            <md-layout md-align="center" md-vertical-align="center">
                <span class="md-subheading">{{ currentMonth(date) }} </span>
            </md-layout>
            <md-layout md-align="end">
                <span flex></span>
                <md-button @click="dateIncrement">
                    <md-icon>keyboard_arrow_right</md-icon>
                </md-button>
            </md-layout>
        </md-layout>

        <md-layout md-flex="60" md-align="center" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100"
                   v-if="Object.keys(sets).length === 0">
            <span class="md-subheading">Здесь пока что ничего нет.</span>
        </md-layout>

        <md-layout v-else md-column md-flex="60" md-flex-medium="60" md-flex-small="90" md-flex-xsmall="90"
                   v-for="(date, key, index) in sets" :key="index">
            <h2 class="md-title date">{{ russianDate(key) }}</h2>
            <md-table-card class="card-margin" v-for="(set, index) in date" :key="index">
                <md-toolbar>
                    <h1 class="md-title">{{ set.exercise.name }}</h1>
                    <md-button class="md-icon-button" @click="createRepeat(set.id)">
                        <md-icon>add</md-icon>
                    </md-button>
                    <md-button class="md-icon-button" @click="changeExercise(set.id)">
                        <md-icon>edit</md-icon>
                    </md-button>
                    <md-button class="md-icon-button" @click="deleteSet(set.id)">
                        <md-icon>delete_forever</md-icon>
                    </md-button>
                </md-toolbar>

                <md-table v-if="set.repeats.length > 0">
                    <md-table-header>
                        <md-table-row>
                            <md-table-head>#</md-table-head>
                            <md-table-head>Вес</md-table-head>
                            <md-table-head>Повторы</md-table-head>
                            <md-table-head></md-table-head>
                        </md-table-row>
                    </md-table-header>

                    <md-table-body>
                        <md-table-row v-for="(rep, index) in set.repeats" :key="index">
                            <md-table-cell>{{ index + 1}}</md-table-cell>
                            <md-table-cell>{{ rep.weight }}</md-table-cell>
                            <md-table-cell>{{ rep.count }}</md-table-cell>
                            <md-table-cell>
                                <md-button class="md-icon-button" @click="updateRepeat(rep.id, rep.weight, rep.count)">
                                    <md-icon>edit</md-icon>
                                </md-button>
                            </md-table-cell>
                        </md-table-row>
                    </md-table-body>
                </md-table>

                <md-card-content v-else>
                    Вы еще не добавили ни одного подхода
                </md-card-content>

            </md-table-card>
        </md-layout>

        <router-link tag="md-button" to="/training/add" id="addBtn" class="md-fab md-fab-bottom-right">
            <md-icon>add</md-icon>
        </router-link>

        <DeleteSet
                :setId="setId"
                ref="deleteSet"
                @fetchSetsByDate="fetchSets"></DeleteSet>

        <ChangeExercise
                :setId="setId"
                ref="changeExercise"
                @fetchSetsByDate="fetchSets"></ChangeExercise>

        <RepeatDialog
                :setId="setId"
                :repeatId="repeatId"
                :weightOld="weight"
                :countOld="count"
                :action="action"
                ref="repeatDialog"
                @fetchSetsByDate="fetchSets"></RepeatDialog>

    </md-layout>

</template>

<script>
    import axios from 'axios'
    import moment from 'moment'
    import RepeatDialog from './RepeatDialog.vue';
    import ChangeExercise from './ChangeExercise.vue'
    import DeleteSet from './DeleteSet.vue'

    moment.locale('ru')

    export default {
        data() {
            return {
                date: '',
                sets: '',
                setId: '',
                repeatId: '',
                action: '',
                weight: '',
                count: '',
            }
        },

        components: {
            RepeatDialog,
            ChangeExercise,
            DeleteSet
        },

        methods: {

            createRepeat(setId) {
                this.setId = setId
                this.action = 'create'
                this.count = ''
                this.weight = ''
                this.$refs.repeatDialog.openDialog()
            },

            updateRepeat(repeatId, weight, count) {
                this.repeatId = repeatId
                this.weight = weight
                this.count = count
                this.action = 'update'
                this.$refs.repeatDialog.openDialog()
            },

            changeExercise(setId) {
                this.setId = setId
                this.$refs.changeExercise.openDialog()
            },

            deleteSet(setId) {
                this.setId = setId;
                this.$refs.deleteSet.openDialog()
            },

            getAllSets() {
                axios.get('/training/sets')
                    .then(response => {
                        this.sets = response.data.sets
                    })
            },
            fetchSets() {
                this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
            },
            getSetsByDate(month, year) {
                axios.get(`/training/set_by_date/${month + 1}/${year}`)
                    .then(response => {
                        this.sets = response.data.sets
                    })
            },
            russianDate(date) {
                return moment(date).format('D MMMM')
            },
            currentMonth(date) {
                return moment(date).format('MMMM YYYY')
            },
            dateIncrement() {
                this.date = moment(this.date).add(1, 'M')
                this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
            },
            dateDecrement() {
                this.date = moment(this.date).subtract(1, 'M')
                this.getSetsByDate(moment(this.date).month(), moment(this.date).year())
            }
        },

        created() {
            this.date = new Date()
            this.getAllSets()
        }
    }
</script>

<style>
    #addBtn {
        position: fixed;
    }

    .card-margin {
        margin: 8px;
    }
</style>
