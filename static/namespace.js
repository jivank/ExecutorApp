var app = angular.module('myApp', [])
app.controller('myCtrl', function($scope,$http) {
    $http.get("/listing").success(function(response) {
        $scope.files = response.scripts;
    });
    $http.get("/running").success(function(response) {
        $scope.history = response;
    });
});
