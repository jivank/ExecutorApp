var app = angular.module('myApp', ['ngAnimate'])
app.controller('myCtrl', function($scope, $http) {
    $scope.alerts = [];
    $scope.getListing = function() {
        $http.get("/listing").success(function(response) {
           // for (f in response.scripts.slice($scope.files.length)){
           //     $scope.files.unshift(f);
           //     console.log(f);
           // }
            angular.merge($scope.files,response.scripts);
        });
    }
    $scope.getRunning = function() {
        $http.get("/running").success(function(response) {
        //    for (l in response.slice($scope.history.length)){
        //        $scope.history.unshift(l);
        //        console.log(l);
        //    }
            angular.merge($scope.history,response);
        });
    }
    $scope.addAlert = function(script) {
        $http.get("/execute/" + script).success(function(response) {
            $scope.pid = response.pid
            $scope.alerts.push({
                type: 'success',
                msg: 'Ran with PID:' + $scope.pid
            });
        })
    };

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };



});
