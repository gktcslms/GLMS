var app = angular.module("create_quiz", []);

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
	console.log("Inside My Controller");
	var get_quizes_url = "/api/quiz_all_quizes/";
	$http.get(get_quizes_url).then(successCallback, errorCallback);
	function successCallback(response){
		$scope.quizes = response.data;
	};
	function errorCallback(error){
		alert("Error Loading Page!");
	};

	$scope.edit_quiz = function(object, index){
		console.log("Edit Quiz");
		console.log(object);
		$scope.selected = object;
		$scope.q_name = $scope.selected.quiz_name; 
		$scope.q_time = $scope.selected.time_limit; 
		$scope.questions = $scope.selected.questions;
		if($scope.questions.length !== 0 || $scope.questions.length !== undefined){
			$scope.selected_question = $scope.questions[0];
		}
	};

	$scope.change_quiz_name = function(){
		var url = $scope.selected.url;
		console.log(url);
		var data = {
			"quiz_name": $scope.q_name
		};
		console.log(data);
		$http.patch(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			if (response.status === 200){
				console.log("Success");
				console.log(response);
				$scope.selected.quiz_name = $scope.q_name;
				swal("Good job!", "Quiz Name Updated!", "success");
			}
		};
		function errorCallback(error){
			console.log(error);
			swal("Oops!", "Something went wrong!", "error");					
		};			
	};

	$scope.change_quiz_time = function(){
		var url = $scope.selected.url;
		console.log(url);
		var data = {
			"time_limit": $scope.q_time
		};
		console.log(data);
		$http.patch(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			if (response.status === 200){
				console.log("Success");
				console.log(response);
				$scope.selected.time_limit = $scope.q_time; 
				swal("Good job!", "Quiz Time Updated!", "success");
			}
		};
		function errorCallback(error){
			console.log(error);
			swal("Oops!", "Something went wrong!", "error");					
		};			
	};

	$scope.select_question = function(question){
		$scope.selected_question = question;
		console.log($scope.selected_question);
	};

	$scope.save_question = function(){
		console.log("Save Question");
		if($scope.selected_question.url === null || $scope.selected_question.url === undefined){
			$scope.save_new_question();
		}
		else{
			$scope.save_old_question();
		};
	};

	$scope.save_new_question = function(){
		console.log("Save New Question");
		console.log($scope.selected);
		var url = "/api/quiz_all_questions/"
		var data = {
			"quiz": $scope.selected.url,
			"text": $scope.selected_question.text,
			"possible_answers": [
				{
					"text": $scope.selected_question.possible_answers[0].text
				},
				{
					"text": $scope.selected_question.possible_answers[1].text
				},
				{
					"text": $scope.selected_question.possible_answers[2].text
				},
				{
					"text": $scope.selected_question.possible_answers[3].text
				}
			],
			"selected": null,
			"correct": {"text": $scope.selected_question.correct.text}
		};
		$http.post(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			$scope.selected_question.url = response.data.url;
			console.log($scope.selected_question);				
			// $scope.questions.push($scope.selected_question);
			// console.log($scope.questions);
			$scope.selected.questions.push($scope.selected_question);
			swal("Good job!", "Question Saved!", "success");
		};
		function errorCallback(error){
			console.log(error);
			swal("Oops!", "Something went wrong!", "error");					
		};				
	};

	$scope.save_old_question = function(){
		console.log("Save Old Question");
		console.log($scope.selected_question);
		var data = {
			"quiz": $scope.selected_question.quiz,
			"text": $scope.selected_question.text,
			"possible_answers": [
				{
					"text": $scope.selected_question.possible_answers[0].text
				},
				{
					"text": $scope.selected_question.possible_answers[1].text
				},
				{
					"text": $scope.selected_question.possible_answers[2].text
				},
				{
					"text": $scope.selected_question.possible_answers[3].text
				}
			],
			"selected": null,
			"correct": {"text": $scope.selected_question.correct.text}
		};
		var url = $scope.selected_question.url;
		$http.patch(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			swal("Good job!", "Question Updated!", "success");
		};
		function errorCallback(error){
			console.log(error);
			swal("Oops!", "Something went wrong!", "error");					
		};				
	};


	$scope.clear_form = function(){
		console.log("Clear Form");
		$('#quiz_form')[0].reset();
		$scope.selected_question = undefined;
		console.log($scope.selected_question);
	}

	$scope.delete_question = function(){
		$http.delete($scope.selected_question.url).then(successCallback, errorCallback);	
		function successCallback(response){
			swal("Deleted Question Successfully.", {
				icon: "success",
			});
			var index = $scope.questions.indexOf($scope.selected_question);
			$scope.questions.splice( $scope.questions.indexOf($scope.selected_question), 1 );
			$scope.selected_question = $scope.questions[index-1];
		};
		function errorCallback(error){
			swal("Question could not be deleted!");					
		};
	};

	$scope.create_new_quiz = function(){
		console.log("Creating new quiz.");
		console.log($scope.new_quiz_name);
		var url = "/api/quiz_all_quizes/";
		var data = {
			"quiz_name": $scope.new_quiz_name
		};
		$http.post(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			swal("Created Quiz Successfully.", {
				icon: "success",
			});
			console.log(response);
			$scope.quizes.push(response.data);
			console.log($scope.quizes);
		};
		function errorCallback(error){
			console.log(error);
			swal("Quiz could not be created!");					
		};
	};

	$scope.delete_quiz = function(object, index){
		console.log(object.url);
		console.log(index);

		$http.delete(object.url).then(successCallback, errorCallback);
		function successCallback(response){
			swal("Deleted Quiz Successfully.", {
				icon: "success",
			});
			console.log(response);
			$scope.quizes.splice( $scope.quizes.indexOf(object), 1 );
		};
		function errorCallback(error){
			swal("Oops Quiz not deleted!", {
				icon: "error",
			});
			console.log(error);
		}
	}
});