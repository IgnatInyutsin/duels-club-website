/**
    Контроллер, выполняющийся при формировании каждой страницы
*/
main.controller('common',function($scope,$http,$location,$cookies){

    $scope.showUpButton = false; // Кнопка перемотки вверх

    $scope.pageTop = function(){ // Функция перемотки вверх
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    }

    if(document.location.hash=="")document.location.hash='!/index/'; //если переходят по пустому хэшу то редирект на главную страницу

    if (!$cookies.get('session')) { //проверка сессии
        //если нет
        $scope.userID = 0
        $scope.loginBool = false
    }
    else { //если есть
        $.ajax({ //сравниваем сессию с базой данных с помощью запроса
            url: 'http://localhost:82/get_data',
            method: 'get',
            dataType: 'json',
            data: {sql: 'session' + $cookies.get('session')},
            success: function(data){ //если удачный выполняем асинхронную функцию
                $scope.userID = data.id
                if (data.status != "not_ended") { //если действительна
                    $scope.loginBool = false
                    $scope.userID = 0
                }
                else { //если не действительна
                    $scope.loginBool = true
                }
            }
        });
    }
});
