main.controller('members',function($scope,$http,$location,$cookies, $routeParams){
	//контроллер страницы index
	$scope.$parent.pageName = 'members';
	
	//собиратели информации информации
	//объект для сбора последних матчей
	let oneMember = new DataCollector ({
		$scope: $scope,
		$cookies: $cookies,
		requestData: {sql: 'OneMember' + $routeParams.memberID},
		extFunction: function (caller) {
			caller.responseData[8] = parseInt(caller.responseData[2]/(caller.responseData[2] + caller.responseData[3] + caller.responseData[4])*100)
			caller.$scope.dataOfMember = caller.responseData //добавляем данные в $scope
			caller.$scope.$apply();
			//скрываем блок с поиском
			let memberData = new Block({
				$scope: $scope,
				$cookies: $cookies,
				id: "search__member__block"
			})
			.hidden();
		}
	});

	//объект для получения матчей
	let oneMemberMatchs = new DataCollector ({
		$scope: $scope,
		$cookies: $cookies,
		requestData: {sql: 'matchsOfMember' + $routeParams.memberID},
		extFunction: function (caller) {
			caller.$scope.dataOfMemberMatchs = caller.responseData
			caller.$scope.$apply();
		}
	});

	//проверки
	//проверка на строку в браузере
	let memberIdCheckup = new Checkup({
		$cookies: $cookies,
		$scope: $routeParams,
		condition: function($routeParams) { //условие при проверке
			if (parseInt($routeParams.memberID) != NaN && $routeParams.memberID != undefined) { //если не пустая возвращаем true
				return true;
			}
			else {
				return false;
			}
		},
		ifTrue: function() {
			//запускаем коллектор данных
			oneMember.takeBackendData({
				errorFunction: function () { //если ошибка то убираем блок с игроком
					let memberData = new Block({
						$scope: $scope,
						$cookies: $cookies,
						id: "member_container"
					})
					.hidden();
				}
			});
			oneMemberMatchs.takeBackendData();
		},
		ifFalse: function() {
			let memberData = new Block({//убираем блок с игроком
				$scope: $scope,
				$cookies: $cookies,
				id: "member_container"
			})
			.hidden();
		}
	});

	//запускаем проверку
	memberIdCheckup.check();
});