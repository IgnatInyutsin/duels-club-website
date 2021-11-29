class DataCollector extends ProjectObject { //для сборщиков информации
    constructor(options) {
        super(options);
        this.requestData = options.requestData
        this.extFunction = options.extFunction

        if (options.hasOwnProperty("async")) {
            this.async = options.async
        } else {
            this.async = false
        }

        this.responseData = []
        return this
    }

    takeBackendData(options = {
        errorFunction: function () {
        }
    }) {
        let caller = this
        $.ajax({ //делаем запрос
            url: caller.url + 'api/get_data',
            method: 'get',
            dataType: 'json',
            data: this.requestData,
            async: this.async,
            success: function (data) { //если удачный запрос выполняем асинхронную функцию
                caller.responseData = data //передаем в переменную
                return caller.extFunction(caller); //выполняем побочную функцию
            },
            error: options.errorFunction
        });
    }
}