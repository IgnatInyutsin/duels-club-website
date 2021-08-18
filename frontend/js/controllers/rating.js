main.controller('rating',function($scope,$http,$location,$cookies){
	//контроллер страницы index
	$scope.$parent.pageName = 'rating';
	//делаем запрос /get_data
	$.ajax({
		url: 'http://localhost:82/get_data',
		method: 'get',
		dataType: 'json',
		data: {sql: 'rating'},
		success: function(data){ //если удачный выполняем асинхронную функцию
			//меняем рейтинг на данные с запроса
			$scope.rating = data
			//добавляем в каждый массив номер в топе и процент побед
			for (i=0; i<$scope.rating.length; i++) {
				$scope.rating[i][7] = i+1
				$scope.rating[i][8] = parseInt($scope.rating[i][2]/($scope.rating[i][2]+$scope.rating[i][3]+$scope.rating[i][4])*100)
			}
			//отправляем все изменения в $scope
			$scope.$apply();
		}
	});
});