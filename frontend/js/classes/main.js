class ProjectObject {
	constructor(options) {
		this.$scope = options.$scope //передаем $scope
		this.$cookies = options.$cookies
		this.$timeout = options.$timeout
	}

	joinWithBackend(options) { //функкция для отправки запросов
		var responseData = []
		let caller = this

		$.ajax({ //делаем запрос 
			url: options.url,
			method: 'get',
			dataType: 'json',
			data: options.requestData,
			success: function(data){ //если удачный запрос выполняем асинхронную функцию
				responseData = data //передаем в переменную
				options.additionalFunc(responseData, caller.$cookies, caller.$scope); //выполняем побочную функцию
			},
			error: options.errorFunction
		});
	}
}