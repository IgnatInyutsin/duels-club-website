main.controller('members',function($scope,$http,$location,$cookies, $routeParams){
	//контроллер страницы index
	$scope.$parent.pageName = 'members';

	//объявление переменных
	viewSearch = false
	$scope.dataOfMember = []

	//объявление функций
	getProfileData = function(memberID) {
			$.ajax({ //запрос для собирания данных об пользователе
				url: 'http://localhost:82/get_data',
				method: 'get',
				dataType: 'json',
				data: {sql: 'OneMember' + String(memberID)},
				success: function(data){ //если удачный выполняем асинхронную функцию
					$scope.dataOfMember = data
					$scope.$apply(); //отправляем все изменения в $scope
				}
			});
	}

	//проверка memberID, если число, то делаем вывод профиля, если нет, то даем значение true на показывание поиска
	if (parseInt($routeParams.memberID) != NaN) {
		try {
			getProfileData(parseInt($routeParams.memberID));
		}
		catch {
			viewSearch = true
		}
	}
	else {
		viewSearch = true
	}

});