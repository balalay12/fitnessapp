<template>
	<md-layout md-gutter md-align="center" md-column md-flex="60" md-flex-medium="60" md-flex-small="60" md-flex-xsmall="90">
		
		<md-layout md-row md-align="center" md-flex="100" md-flex-medium="100" md-flex-small="100" md-flex-xsmall="100">
			<h1 class="md-title">Размеры тела</h1>
		</md-layout>

		<md-layout md-align="center" md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">
			<h1 class="md-subheading" v-if="Object.keys(anthropometry).length === 0">Вы пока что ничего не добавили</h1>
			<md-layout class="card-margin" v-else v-for="item in anthropometry" :key="item.id"  md-column md-tag="md-table-card" md-align="center" md-flex="30" md-flex-medium="50" md-flex-small="100" md-flex-xsmall="100">

					<md-toolbar>
						<h1 class="md-title">{{ humanDate(item.date) }}</h1>
	          <md-button class="md-icon-button" @click="updateOn('bodysizeDialog', item.id, anthropometry.indexOf(item))">
	            <md-icon>edit</md-icon>
	          </md-button>
          	<md-button class="md-icon-button" id="deleteBodysizeButton" @click="deleteOn('deleteDialog', item.id)">
	            <md-icon>delete_forever</md-icon>
	          </md-button>
					</md-toolbar>

					<md-table>
						<md-table-header>
							<md-table-head>#</md-table-head>
							<md-table-head>См</md-table-head>
						</md-table-header>

						<md-table-body>

							<md-table-row>
								<md-table-cell>Шея</md-table-cell>
								<md-table-cell>{{ item.neck ? item.neck : '-' }}</md-table-cell>
							</md-table-row>
							<md-table-row>
								<md-table-cell>Грудь</md-table-cell>
								<md-table-cell>{{ item.chest ? item.chest : '-' }}</md-table-cell>
							</md-table-row>
							<md-table-row>
								<md-table-cell>Бицепс</md-table-cell>
								<md-table-cell>{{ item.arm ? item.arm : '-' }}</md-table-cell>
							</md-table-row>
							<md-table-row>
								<md-table-cell>Предплечье</md-table-cell>
								<md-table-cell>{{ item.forearm ? item.forearm : '-' }}</md-table-cell>
							</md-table-row>
							<md-table-row>
								<md-table-cell>Талия</md-table-cell>
								<md-table-cell>{{ item.waist ? item.waist : '-' }}</md-table-cell>
							</md-table-row>
							<md-table-row>
								<md-table-cell>Бедро</md-table-cell>
								<md-table-cell>{{ item.hip ? item.hip : '-' }}</md-table-cell>
							</md-table-row>
							<md-table-row>
								<md-table-cell>Голень</md-table-cell>
								<md-table-cell>{{ item.shin ? item.shin : '-' }}</md-table-cell>
							</md-table-row>

						</md-table-body>
					</md-table>

			</md-layout>
		</md-layout>

		<DeleteDialog ref="deleteDialog" v-on:fetchBodysize="fetchData" :id="bodysizeId" />

		<BodysizeForm ref="bodysizeDialog" v-on:fetchBodysize="fetchData" :method="method" :data="data" />

    <md-button id="addBtn" class="md-fab md-fab-bottom-right" @click="createOn('bodysizeDialog')">
      <md-icon>add</md-icon>
    </md-button>
	</md-layout>
</template>

<script>
	import axios from 'axios'
	import moment from 'moment'
	import { numeric } from 'vuelidate/lib/validators'
	import DeleteDialog from './DeleteDialog.vue'
	import BodysizeForm from './BodysizeForm.vue'

	moment.locale('ru')

	export default {
		data() {
			return {
				anthropometry: [],
				data: {
					neck: '',
					chest: '',
					arm: '',
					forearm: '',
					waist: '',
					hip: '',
					shin: ''
				},
				method: '',
				bodysizeId: '',
			}
		},

		components: {
			DeleteDialog,
			BodysizeForm
		},

		methods: {
			openDialog(ref) {
				this.$refs[ref].openDialog()
			},

			fetchData() {
				axios.get('/anthropometry')
				.then(response => {
					this.anthropometry = response.data.anthropometry
					this.showDelete = false
				})
			},

			humanDate(date) {
				let raw_date = new Date(date)
				return moment(raw_date).format('D MMMM YYYY')
			},

			deleteOn(ref, id) {
				this.bodysizeId = id
				this.openDialog(ref)
			},

			createOn(ref) {
				this.method = 'create'
				this.data = {}
				this.openDialog(ref)
			},

			updateOn(ref, id, index) {
				this.method = 'update'
				this.data = JSON.parse(JSON.stringify(this.anthropometry[index]))
				this.openDialog(ref)
			}
		},

		created() {
			this.fetchData()
		},
	}
</script>

<style >
  #addBtn {
    position: fixed;
  }

  .card-margin {
  	margin: 8px;
  }
</style>
