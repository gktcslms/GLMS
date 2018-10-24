var app = angular.module("browse_courses", ['ngRateIt', 'ngFitText', 'infinite-scroll']);

app.config(function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.headers.common["X-CSRFToken"] = window.csrf_token;
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	$httpProvider.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';
	$httpProvider.defaults.useXDomain = true;
	$httpProvider.defaults.headers.common['Accept'] = 'application/json, text/javascript';
});

app.controller('myCtrl', function($scope, $http, $q) {

	$scope.cart = [];
	
	$scope.courses = {};
	var url = "/api/paginated_courses/";
	
	// FIRST GET
	$http.get(url).then(successCallback, errorCallback);	
	function successCallback(response){
		$scope.courses = response.data;
		$scope.next = response.data.next;
	};
	function errorCallback(error){
		swal("Oops!", "Something went wrong!", "error");
	};
	// END FIRST GET

	// INFINITE SCROLL
/* 	$scope.load_more = function(){
		if($scope.next !== null){
			console.log("Load More");
			$http.get($scope.next).then(successCallback, errorCallback);	
			function successCallback(response){
				$scope.courses.results = $scope.courses.results.concat(response.data.results);	
				$scope.next = response.data.next;								
				console.log($scope.next);					
			};
			function errorCallback(error){
				swal("Oops!", "Something went wrong!", "error");
			};
		}
		else{
			swal("Courses Finished!", "No more courses to show!", "warning");
		};
	};

	$(window).scroll(function(){
		if ($(this).scrollTop() + 1 >= $('body').height() - $(window).height()){
			$scope.load_more();
		};
	}); */
	// END INFINITE SCROLL	

	// SELECT COURSE TO BE SHOWN IN MODAL
	$scope.select_course = function(course){
		$scope.selected_course = course;
		console.log($scope.selected_course);
	};
	// END SELECT COURSE TO BE SHOWN IN MODAL
	
	// SHOW SELECTED MODULES
	$scope.show_modules = function(){
		$scope.modules_visible = true;
	}
	// END SHOW SELECTED MODULES

	// HIDE MODULES ON MODAL CLOSE
	$('#myModal').on('hidden.bs.modal', function () {
		$scope.modules_visible = false;
	})
	// END HIDE MODULES ON MODAL CLOSE

	$scope.add_to_cart = function(){
		$scope.selected_course.added_to_cart = true;
		$scope.cart.push($scope.selected_course);
		$scope.json_cart = JSON.stringify($scope.cart);
		console.log(typeof($scope.json_cart));
		// POST
		var url = "/update_cart_session/";
		var data= {
			"cart": $scope.json_cart
		};
		$http.post(url, data).then(successCallback, errorCallback);			
		function successCallback(response){
			console.log(response);
		};
		function errorCallback(error){
			console.log(error);
			swal("Oops!", "Check your internet connection!", "error");			
		};
	};
});
