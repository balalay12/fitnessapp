<template>
	<md-layout md-gutter md-align="center" md-column md-flex="60" md-flex-medium="60" md-flex-small="60" md-flex-xsmall="90">
		
		<md-layout md-row md-align="center" md-flex="100" md-flex-medium="100" md-flex-small="100" md-flex-xsmall="100">
			<h1 class="md-title">Размеры тела</h1>
		</md-layout>

		<md-layout md-align="center" md-flex="60" md-flex-medium="60" md-flex-small="100" md-flex-xsmall="100">
			<h1 class="md-subheading" v-if="Object.keys(anthropometry).length === 0">Вы пока что ничего не добавили</h1>
			<md-layout class="card-margin" v-else v-for="item in anthropometry" :key="item.id" md-column md-tag="md-table-card" md-align="center" md-flex="30" md-flex-medium="50" md-flex-small="100" md-flex-xsmall="100">

					<md-toolbar>
						<h1 class="md-title">{{ humanDate(item.date) }}</h1>
						<md-button class="md-icon-button" @click="openBodySizeDialogForUpdate('bodysizeDialog', anthropometry.indexOf(item))">
	            <md-icon>edit</md-icon>
	          </md-button>
	          <md-button class="md-icon-button" id="deleteBodysizeButton" @click="openDialog('deleteDialog', item.id)">
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

		<!-- Dialog for delete bodysize item -->
		<md-dialog md-open-from="#deleteBodysizeButton" md-close-to="#deleteBodysizeButton" ref="deleteDialog">
      <md-dialog-title>Удаленние данных</md-dialog-title>

      <md-dialog-content>
       <p>Вы уверены что хотите удалить элемент?</p> 
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeDialog('deleteDialog')">Отмена</md-button>
        <md-button class="md-primary" @click="deleteBodysize('deleteDialog')">Удалить</md-button>
      </md-dialog-actions>
    </md-dialog>

    <!-- Dialog for add and edit bodysize item -->
    <md-dialog md-open-from="#addBtn" md-close-to="#addBtn" ref="bodysizeDialog">
      <md-dialog-title>
				Размеры тела
      </md-dialog-title>

      <md-dialog-content>
       <form novalidate @submit.stop.prevent="submit">

					<md-input-container>
						<label>Шея</label>
						<md-input type="number" v-model="data.neck"></md-input>
					</md-input-container>

					<md-input-container>
						<label>Грудь</label>
						<md-input type="number" v-model="data.chest"></md-input>
					</md-input-container>

					<md-input-container>
						<label>Бицепс</label>
						<md-input type="number" v-model="data.arm"></md-input>
					</md-input-container>

					<md-input-container>
						<label>Предплечье</label>
						<md-input type="number" v-model="data.forearm"></md-input>
					</md-input-container>

					<md-input-container>
						<label>Талия</label>
						<md-input type="number" v-model="data.waist"></md-input>
					</md-input-container>

					<md-input-container>
						<label>Бедро</label>
						<md-input type="number" v-model="data.hip"></md-input>
					</md-input-container>

					<md-input-container>
						<label>Голень</label>
						<md-input type="number" v-model="data.shin"></md-input>
					</md-input-container>

				</form>
      </md-dialog-content>

      <md-dialog-actions>
        <md-button class="md-primary" @click="closeBodysizeDialog('bodysizeDialog')">Отмена</md-button>
        <md-button v-if="!update" class="md-primary" @click="saveBodysize('bodysizeDialog')">Сохранить</md-button>
        <md-button v-if="update" class="md-primary" @click="updateBodysize('bodysizeDialog')">Обновить</md-button>
      </md-dialog-actions>
    </md-dialog>

		<md-button id="addBtn" class="md-fab md-fab-bottom-right" @click="openBodySizeDialog('bodysizeDialog')">
      <md-icon>add</md-icon>
    </md-button>
	</md-layout>
</template>

<script>
	import axios from 'axios'
	import moment from 'moment'

	export default {
		data() {
			return {
				anthropometry: [],
				data: {},
				update: false,
				delete: ''
			}
		},

		methods: {
			fetchData() {
				axios.get('/anthropometry')
				.then(response => {
					this.anthropometry = response.data.anthropometry
				})
			},
			humanDate(date) {
				let raw_date = new Date(date)
				return moment(raw_date).format('D MMMM YYYY')
			},

			// delete dialog
			openDialog(ref, id) {
				this.delete = id
    		this.$refs[ref].open();
	    },
	    closeDialog(ref) {
	    	this.delete = ''
	      this.$refs[ref].close();
	    },
	    deleteBodysize(ref) {
	    	axios.get(`/anthropometry/delete/${this.delete}`)
	    	.then(response => {
	    		this.data = {}
	    		this.fetchData()
	    		this.closeDialog(ref)
	    	})
	    },

	    // bodysize dialog
	    openBodySizeDialog(ref) {
	    	this.$refs[ref].open()
	    },
	    openBodySizeDialogForUpdate(ref, index) {
	    	this.update = true;
	    	this.data = this.anthropometry[index]
	    	this.$refs[ref].open()
	    },
	    saveBodysize(ref) {
	    	axios.post('/anthropometry/add',
					this.data
				)
				.then(response => {
					this.data = {}
					this.fetchData()
					this.closeBodysizeDialog(ref)
				})
	    },
	    updateBodysize(ref) {
	    	let send_data = {}
	    	// check null in value
				for (let item in this.data) {
					if (this.data[item]) {
						send_data[item] = this.data[item]
					}
				}
				axios.post('/anthropometry/edit', send_data)
				.then(response => {
					this.data = {}
					this.fetchData()
					this.closeBodysizeDialog(ref)
				})
	    },
	    closeBodysizeDialog(ref) {
	    	this.update = false
	    	for (let item in this.data) {
					this.data[item] = ''
				}
	    	this.$refs[ref].close()
	    }
		},

		created() {
			this.fetchData()
		}
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
