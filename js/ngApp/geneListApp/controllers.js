var phonecatApp = angular.module('phonecatApp', []);
 
phonecatApp.controller('PhoneListCtrl', ['$scope', '$http',
  function ($scope, $http) {
    $http.get('/1.0/genes/json').success(function(data) {
      $scope.genes = data;
    });
    $scope.numLimit = 100;
  }]);
