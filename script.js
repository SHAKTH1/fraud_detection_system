var app = angular.module('fraudDetectionApp', []);

app.controller('fraudDetectionController', function($scope, $http, $rootScope) {
    $scope.formData = {};
    $scope.predictionResult = null;

    function convertToBoolean(value) {
        return value === 'true';
    }

    $scope.detectFraud = function() {
        console.log('Form data:', $scope.formData); // Log form data for inspection
        // Convert string values to boolean values
        $scope.formData.cashout = convertToBoolean($scope.formData.cashout);
        $scope.formData.debit = convertToBoolean($scope.formData.debit);
        $scope.formData.payment = convertToBoolean($scope.formData.payment);
        $scope.formData.transfer = convertToBoolean($scope.formData.transfer);

        // Send the data to the server for prediction
        $http.post('/predict', $scope.formData)
            .then(function(response) {
                console.log('Prediction result:', response.data.prediction);
                $rootScope.$broadcast('predictionReceived', response.data.prediction);
            }, function(error) {
                console.log('Prediction error:', error);
            });
    };

    // Listen for the predictionReceived event
    $scope.$on('predictionReceived', function(event, prediction) {
        $scope.predictionResult = prediction;
    });
});
