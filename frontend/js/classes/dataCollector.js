class DataCollector extends ProjectObject { //для сборщиков информации
	constructor(options) {
		super(options);
		this.requestData = options.requestData
		this.extFunction = options.extFunction
		this.responseData = []
	}

	takeBackendData(options = {errorFunction: function() {}}) {
		let caller = this
		$.ajax({ //делаем запрос 
			url: caller.url + 'get_data',
			method: 'get',
			dataType: 'json',
			data: this.requestData,
			success: function(data){ //если удачный запрос выполняем асинхронную функцию
				caller.responseData = data //передаем в переменную
				caller.extFunction(caller); //выполняем побочную функцию
			},
			error: options.errorFunction
		});
	}
}