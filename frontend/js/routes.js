//создаем модуль main (подключается в index.html)
var main = angular.module("main", ['ngRoute', 'ngCookies']);

main.config(function ($routeProvider) {
    $routeProvider.when("/index/", {
        controller: "index",
        templateUrl: "views/controllers/index.html"
    });

    $routeProvider.when("/get_result/", {
        controller: "get_result",
        templateUrl: "views/controllers/get_result.html"
    });

    $routeProvider.when("/rating/", {
        controller: "rating",
        templateUrl: "views/controllers/rating.html"
    });

    $routeProvider.when("/members/:memberID?", {
        controller: "members",
        templateUrl: "views/controllers/members.html"
    });

    $routeProvider.when("/matches/:matchID?", {
        controller: "matches",
        templateUrl: "views/controllers/matches.html"
    });

    $routeProvider.when("/invite/:inviteID", {
        controller: "invite",
        templateUrl: "views/controllers/invite.html"
    })

    $routeProvider.when("/teams/", {
        controller: "teams",
        templateUrl: "views/controllers/teams.html"
    });

    $routeProvider.when("/profile/", {
        controller: "profile",
        templateUrl: "views/controllers/profile.html"
    });

    $routeProvider.when("/faq/", {
        controller: "matches",
        templateUrl: "views/controllers/faq.html"
    });
});