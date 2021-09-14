main.controller('header',function($scope,$http,$location,$cookies){
	//объект бургер
	let burger = new Button ({
		$scope: $scope,
		$cookies: $cookies,
		id: "burger",
		clickFunction: function () { //при нажатии
			if ( $('.header__menu').hasClass("deactive") ) { //если неактивное делаем активным
				$('.header__menu').removeClass("deactive");
				$('.header__menu').addClass('active');
			}
			else { //если активное делаем деактивным
				$('.header__menu').removeClass('active');
				$('.header__menu').addClass('deactive');
			}

			//переключаем стили у бургера и body, у body для блокировки скролла
			$('.header__burger').toggleClass('active');
			$('body').toggleClass('active');
		}
	});

	$scope.burger = burger
});