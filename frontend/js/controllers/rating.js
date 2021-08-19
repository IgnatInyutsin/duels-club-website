main.controller('rating',function($scope,$http,$location,$cookies){
	//контроллер страницы index
	$scope.$parent.pageName = 'rating';

	$.ajax({ //делаем запрос на получение текущего рейтинга
		url: 'http://localhost:82/get_data',
		method: 'get',
		dataType: 'json',
		data: {sql: 'rating'},
		success: function(data){ //если удачный выполняем асинхронную функцию
			$scope.rating = data //передаем в $scope

			for (i=0; i<$scope.rating.length; i++) { 
				$scope.rating[i][7] = i+1 //добавляем в каждый массив номер в топе
				$scope.rating[i][8] = parseInt($scope.rating[i][2]/($scope.rating[i][2]+$scope.rating[i][3]+$scope.rating[i][4])*100); //процент побед
			}

			$scope.$apply(); //отправляем все изменения в $scope
		}
	});
});