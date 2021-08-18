main.controller('rating',function($scope,$http,$location,$cookies){
	//контроллер страницы index
	$scope.$parent.pageName = 'rating';
	$scope.mydata = []
	$.ajax({
		url: 'http://localhost:82/get_data',
		method: 'get',
		dataType: 'json',
		data: {sql: 'rating'},
		success: function(data){ 
			$scope.rating = data
			for (i=0; i<$scope.rating.length; i++) {
				$scope.rating[i][7] = i+1
				$scope.rating[i][8] = parseInt($scope.rating[i][2]/($scope.rating[i][2]+$scope.rating[i][3]+$scope.rating[i][4])*100)
			}
			$scope.$apply();
		}
	});
});