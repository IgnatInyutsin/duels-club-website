main.controller('matches',function($scope,$http,$location,$cookies, $routeParams){
	//контроллер страницы index
	$scope.$parent.pageName = 'matches';

	//коллекторы данных

	//объект для сбора инфы о матче
	let allMatch = new DataCollector ({
		$scope: $scope,
		$cookies: $cookies,
		requestData: {sql: 'allMatch'},
		extFunction: function (caller) {
			//добавляем данные в $scope
			console.log(caller.responseData);
			caller.$scope.dataOfMatchs = caller.responseData
			caller.$scope.$apply();
			//скрываем блок с поиском
		}
	});

	//объект для сбора инфы о матче
	let oneMatch = new DataCollector ({
		$scope: $scope,
		$cookies: $cookies,
		requestData: {sql: 'OneMatch' + $routeParams.matchID},
		extFunction: function (caller) {
			//добавляем данные в $scope
			console.log(caller.responseData);
			caller.$scope.dataOfMatch = caller.responseData
			caller.$scope.$apply();
			//скрываем блок с поиском
			let memberSearch = new Block({
				$scope: $scope,
				$cookies: $cookies,
				id: "search_matches_block"
			})
			.hidden();
		}
	});

	//проверка на строку в браузере
	let matchIdCheckup = new Checkup({
		$cookies: $cookies,
		$scope: $routeParams,
		condition: function($routeParams) { //условие при проверке
			if (parseInt($routeParams.matchID) != NaN && $routeParams.matchID != undefined) { //если не пустая возвращаем true
				return true;
			}
			else {
				return false;
			}
		},
		ifTrue: function() {
			//запускаем коллектор данных
			oneMatch.takeBackendData({
				errorFunction: function () { //если ошибка то убираем блок с игроком
					let matchData = new Block({
						$scope: $scope,
						$cookies: $cookies,
						id: "match_container"
					})
					.hidden();
				}
			});
		},
		ifFalse: function() {
			let matchData = new Block({//убираем блок с игроком
				$scope: $scope,
				$cookies: $cookies,
				id: "match_container"
			})
			.hidden();
			allMatch.takeBackendData();
		}
	});

	//запускаем проверку
	matchIdCheckup.check();
});