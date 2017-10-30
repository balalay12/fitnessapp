export const dialogsControl = {
	methods: {
		openDialog() {
			this.$refs.dialog.open()
		},
		closeDialog() {
			this.$refs.dialog.close()
		}
	}
}