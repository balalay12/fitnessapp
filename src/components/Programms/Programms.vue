<template>
    <md-layout md-gutter md-align="center" md-column md-flex-xlarge="60" md-flex-large="60" md-flex-medium="60"
               md-flex-small="100" md-flex-xsmall="100">

        <md-layout md-gutter md-column>
            <md-layout md-align="center" md-flex-large="90" md-flex-medium="90" md-flex-small="90" md-flex-xsmall="90">
                <h1 class="md-title">Программы тренировок</h1>
            </md-layout>
            <md-layout md-align="center" class="text-content">
                <p>Программы тренировок позволяют создать шаблоны ваших тренировочных дней. И позволят добавлять упражнения нажатием 2 кнопок.</p>
            </md-layout>
        </md-layout>

        <md-layout md-align="center" md-flex-large="60" md-flex-medium="50" md-flex-small="100" md-flex-xsmall="100">
            <h1 class="md-subheading" v-if="programms.length === 0">Вы пока что ничего не добавили</h1>
            <md-layout class="card-margin card-align-top" v-else v-for="(item, index) in programms" :key="index"
                       md-column md-tag="md-table-card" md-flex-xlarge="33" md-flex-large="33" md-flex-medium="45"
                       md-flex-small="100" md-flex-xsmall="100">

                <md-toolbar>
                    <h1 class="md-title">{{ item.name }}</h1>
                    <md-button class="md-icon-button" @click="planningOn(item.id)">
                        <md-icon>assignment</md-icon>
                    </md-button>
                    <md-button class="md-icon-button" @click="createExerciseOn(item.id)">
                        <md-icon>add</md-icon>
                    </md-button>
                    <md-button class="md-icon-button" id="changeNameBtn" @click="changeNameOn(item.id, item.name)">
                        <md-icon>edit</md-icon>
                    </md-button>
                    <md-button class="md-icon-button" id="deleteProgrammButton" @click="deleteProgrammOn(item.id)">
                        <md-icon>delete_forever</md-icon>
                    </md-button>
                </md-toolbar>

                <md-table>
                    <md-table-header>
                        <md-table-head>#</md-table-head>
                        <md-table-head>Упражнение</md-table-head>
                        <md-table-head></md-table-head>
                    </md-table-header>

                    <md-table-body>

                        <md-table-row v-for="(exercise, exIndex) in item.exercises" :key="exIndex">
                            <md-table-cell>{{ exIndex + 1}}</md-table-cell>
                            <md-table-cell>{{ exercise.name }}</md-table-cell>
                            <md-table-cell>
                                <md-button class="md-icon-button" id="editExerciseButton"
                                           @click="editExerciseOn(item.id, exercise)">
                                    <md-icon>edit</md-icon>
                                </md-button>
                                <md-button class="md-icon-button" id="deleteExerciseButton"
                                           @click="deleteExerciseOn(item.id, exercise.id)">
                                    <md-icon>delete_forever</md-icon>
                                </md-button>
                            </md-table-cell>
                        </md-table-row>

                    </md-table-body>
                </md-table>

            </md-layout>
        </md-layout>

        <!-- Add new programm dialog -->
        <NewProgrammDialog
                ref="newProgramm"
                @fetchProgramms="fetchData"/>

        <!-- Change programm's name -->
        <ChangeProgrammNameDialog
                :programmId="current_programm_id"
                :programmName="name"
                ref="changeName"
                @fetchProgramms="fetchData"/>

        <!-- Dialog for delete programm -->
        <DeleteProgrammDialog
                :programm="current_programm_id"
                ref="deleteProgramm"
                @fetchProgramms="fetchData"/>

        <!-- Dialog for delete exercise -->
        <DeleteExerciseDialog
                ref="deleteExercise"
                :programm="current_programm_id"
                :exercise="current_exercise_id"
                @fetchProgramms="fetchData"/>

        <!-- Edit exericse dialog -->
        <EditExerciseDialog
                ref="editExercise"
                :programmId="current_programm_id"
                :exerciseId="current_exercise_id"
                :category="category"
                @fetchProgramms="fetchData"/>

        <PlanningDialog
                ref="PlanningDialog"
                :id="current_programm_id"/>

        <md-button id="addBtn" class="md-fab md-fab-bottom-right" @click="openDialog('newProgramm')">
            <md-icon>add</md-icon>
        </md-button>

    </md-layout>
</template>

<script>
    import axios from 'axios'
    import {required, alphaNum} from 'vuelidate/lib/validators'
    import PlanningDialog from './PlanningDialog.vue'
    import EditExerciseDialog from './EditExerciseDialog.vue'
    import DeleteExerciseDialog from './DeleteExerciseDialog.vue'
    import DeleteProgrammDialog from './DeleteProgrammDialog.vue'
    import ChangeProgrammNameDialog from './ChangeProgrammNameDialog.vue'
    import NewProgrammDialog from './NewProgrammDialog.vue'

    export default {
        data() {
            return {
                name: '',
                category: '',
                programms: [],
                current_programm_id: '',
                new_exercise_id: '',
                current_exercise_id: '',
                new_exercise: false,
            }
        },

        components: {
            PlanningDialog,
            EditExerciseDialog,
            DeleteExerciseDialog,
            DeleteProgrammDialog,
            ChangeProgrammNameDialog,
            NewProgrammDialog
        },

        methods: {
            openDialog(ref) {
                this.$refs[ref].openDialog()
            },

            planningOn(id) {
                this.current_programm_id = id;
                this.openDialog('PlanningDialog')
            },

            createExerciseOn(programm_id) {
                this.current_programm_id = programm_id
                this.current_exercise_id = ''
                this.openDialog('editExercise')
            },

            editExerciseOn(programm_id, exercise) {
                this.current_programm_id = programm_id
                this.current_exercise_id = exercise.id
                this.openDialog('editExercise')
            },

            deleteExerciseOn(programm_id, exercise_id) {
                this.current_programm_id = programm_id
                this.current_exercise_id = exercise_id
                this.openDialog('deleteExercise')
            },

            deleteProgrammOn(programm_id) {
                this.current_programm_id = programm_id
                this.openDialog('deleteProgramm')
            },

            changeNameOn(programm_id, name) {
                this.current_programm_id = programm_id
                this.name = name
                this.openDialog('changeName')
            },

            fetchData() {
                axios.get('/programms/')
                    .then(response => {
                        this.programms = response.data.programms
                    })
            }
        },

        created() {
            this.fetchData()
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

    .card-align-top {
        align-self: flex-start;
    }
</style>
