/**
    Контроллер, выполняющийся при формировании каждой страницы
*/
main.controller('common',function($scope,$http,$location,$cookies, $timeout){

    $scope.showUpButton = false; // Кнопка перемотки вверх

    $scope.pageTop = function(){ // Функция перемотки вверх
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    }

    //объект "проверка на логин"
    let haveLogin = new Checkup ({ 
        $scope: $scope,
        $cookies: $cookies,
        $timeout: $timeout,
        condition: function ($scope, $cookies) { //условие проверки
            if (!$cookies.get('session')) {
                return true;
            }
            else {
                return false;
            }
        },
        ifTrue: function ($scope, $cookies, $timeout) { //если отсутствует логин то выставляем такие переменные
            $timeout(function() {
                $scope.userID = 0;
                $scope.loginBool = false
            }, 0);
        },
        ifFalse: function ($scope, $cookies, $timeout) {//если присутствует то проверяем
            haveLogin.joinWithBackend({ //отправляем запрос на бэкэнд
                url: 'http://localhost:82/get_data',
                requestData: {sql: 'session' + $cookies.get('session')},
                additionalFunc: function (responseData, $cookies, $scope) {
                    if (responseData.status != "not_ended") { //если не действительна
                        $timeout(function() {
                            $scope.userID = 0;
                            $scope.loginBool = false
                        }, 0);
                    }
                    else { //если действительна
                        $timeout(function() {
                            $scope.userID = responseData.id[0]
                            $scope.loginBool = true
                            $scope.userNick = responseData.id[1]
                        }, 0);
                    }

                }
            });
        }
    });

    if(document.location.hash=="")document.location.hash='!/index/'; //если переходят по пустому хэшу то редирект на главную страницу

    //запускаем проверки
    haveLogin.check();
});