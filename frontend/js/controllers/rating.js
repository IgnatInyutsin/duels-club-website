main.controller('rating', function ($scope, $http, $location, $cookies) {
    //контроллер страницы index
    $scope.$parent.pageName = 'rating';

    let rating = new DataCollector({ //объект "рейтинг"
        $scope: $scope,
        requestData: {sql: 'rating'},
        extFunction: function (caller) {
            for (i = 0; i < caller.responseData.length; i++) {
                caller.responseData[i][8] = i + 1 //добавляем в каждый массив номер в топе
                caller.responseData[i][9] = parseInt(caller.responseData[i][2] / (caller.responseData[i][2] + caller.responseData[i][3] + caller.responseData[i][4]) * 100); //процент побед
            }

            caller.$scope.rating = caller.responseData //добавляем данные в $scope
            caller.$scope.$apply();
        }
    });

    rating.takeBackendData(); //забираем данные из бэкэнда
});