main.controller('get_result',function($scope,$http,$location,$cookies){
	//контроллер страницы index
	$scope.$parent.pageName = 'get_result';

	//собиратель всех игроков для автоподмены
	let allMembers = new DataCollector ({
		$scope: $scope,
		requestData: {sql: 'allMember'},
		extFunction: function (caller) { //если запрос удачный
			let opponentNicks = []
			for(i=0; i<caller.responseData.length; i++){//собираем все в одномерный массив
				if (caller.responseData[i][0] != caller.$scope.userNick) { //если это не ник игрока то добавляем в массив
					opponentNicks[i] = caller.responseData[i][0]
				}
				else {
					opponentNicks[i] = ''
				}
			}

			$('#opponentNick').autocomplete({ //создаем варианты поиска
				source: opponentNicks
			})
		}
	});

	//объект проверки на пустоту полей
	let emptyValGame = new Checkup({
		$cookies: $cookies,
		$scope: $scope,
		condition: function($scope) { //условие при проверке
			if ($('#resultOfGame').val() != "none" && $('#opponentNick').val() != "") {
				return true;
			}
			else {
				return false;
			}
		},
		ifTrue: function() {
			sendGameButton.enabled();
		},
		ifFalse: function() {
			sendGameButton.disabled();
		}
	});

	//объект проверки на логин
	let errorOrView = new Checkup({
		$cookies: $cookies,
		$scope: $scope,
		condition: function($scope) { //условие при проверке
			if ($scope.loginBool) {
				return true;
			}

			else if ($scope.loginBool == undefined) {
				if (setTimeout(errorOrView.condition, 30, $scope)) {
					return true;
				}
				else if (!loginOrUnlogin($scope)) {
					return false
				}
			}

			else {
				return false;
			}
		},
		ifTrue: function() {
			let errorBlock = new Block({
				$scope: $scope,
				$cookies: $cookies,
				id: "error_block"
			})
			.hidden();
		},
		ifFalse: function() {
			let resultBlock = new Block({
				$scope: $scope,
				$cookies: $cookies,
				id: "ResultBlock"
			})
			.hidden();
		}
	});

	//объект "кнопка отправки"
	let sendGameButton = new Button({
		$scope: $scope,
		$cookies: $cookies,
		id: "gameSendBut",
		clickFunction: function () { //функция при клике на кнопку
			//собираем данные с полей
			opponentNick = $('input#opponentNick').val();
			gameResult = $('select#resultOfGame').val();
			gameComment = $('input#gameComment').val();
			//делаем запрос на бэкэнд
			sendGameButton.joinWithBackend({
				url: 'get_result',
				requestData: {myID: $scope.userID, opponentNick: opponentNick, gameResult: gameResult, gameComment: gameComment},
				additionalFunc: function (data, $cookies, $scope) {
					//обнуляем поля
					$('input#opponentNick').val('');
					$('select#resultOfGame').val('none');
					$('input#gameComment').val('');

					$('input#gameComment').val('Успешная отправка.');
				},
				errorFunction: function () {
					$('input#opponentNick').val('');
					$('select#resultOfGame').val('none');
					$('input#gameComment').val('');

					$('input#gameComment').val('Произошла ошибка.');
				}
			});
		}
	});
	$scope.sendGameButton = sendGameButton

	//запуск собирателей
	allMembers.takeBackendData();
	//запуск проверок
	errorOrView.check();
	emptyValGame.infinityCheck(emptyValGame);
});