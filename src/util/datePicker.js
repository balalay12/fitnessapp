var optionDatePicker= {
	type: 'day',
	week: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
	month: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
	format: 'DD-MM-YYYY',
	placeholder: '',
	inputStyle: {
		'display': 'inline-block',
		'padding': '6px',
		'font-size': '16px',
		'border': 'none',
		'border-radius': '2px',
		'color': '#5F5F5F',
		'width': '100%',
		'height': '32px',
		'-ms-flex': '1',
		'flex': '1',
		'background': 'none',
		'transition': 'all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1)',
		'transition-property': 'font-size',
		'font-family': 'inherit',
		'line-height': '32px',
		'-webkit-appearance': 'textfield'
	},
	buttons: {
		ok: 'Ok',
		cancel: 'Закрыть'
	},
	overlayOpacity: 0.5, // 0.5 as default
	dismissible: true // as true as default
}

export default optionDatePicker;