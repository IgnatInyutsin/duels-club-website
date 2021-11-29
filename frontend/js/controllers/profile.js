main.controller('profile', function ($scope, $http, $location, $cookies) {
    //контроллер страницы index
    $scope.$parent.pageName = 'profile';

    let loginOrUnlogin = new Checkup({
        $cookies: $cookies,
        $scope: $scope,
        condition: function ($scope) { //условие при проверке
            if ($scope.loginBool) {
                return true;
            } else if ($scope.loginBool == undefined) {
                if (setTimeout(loginOrUnlogin.condition, 30, $scope)) {
                    return true;
                } else if (!loginOrUnlogin($scope)) {
                    return false
                }
            } else {
                return false;
            }
        },
        ifTrue: function () {
            document.location.href = "#!/members/" + String($scope.userID)
        },
        ifFalse: function () {

        }
    });

    loginOrUnlogin.check();
});