var app = angular.module("edit_modules", ['ui.sortable']);

app.config(function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	$httpProvider.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';
	$httpProvider.defaults.useXDomain = true;
	$httpProvider.defaults.headers.common['Accept'] = 'application/json, text/javascript';
});

app.controller('myCtrl', function($scope, $http, $q) {

	$scope.form_info = {};
	
	var course_id = document.getElementById("course_id").innerHTML;
	$scope.learner_id = document.getElementById("learner_id").innerHTML;
	var url = "/api/courses/";
	var query_string = url + course_id + "/";

	$scope.query_string = query_string;

	$http.get(query_string).then(successCallback, errorCallback);	
	function successCallback(response){
		$scope.course = response.data;
		$scope.modules = $scope.course.modules;
		$scope.get_qna_if_exists();
	};
	function errorCallback(error){
		swal("Oops!", "Error Loading Page!", "error");
	};

	$scope.all_modules_quiz = {};
	$scope.all_modules_quiz.quiz_data = [];

	$scope.get_qna_if_exists = function(){
		var req_array = [];
		console.log("Get QnA if exists!");
		console.log($scope.modules);
		console.log($scope.modules[0]);
		for(var i = 0; i < $scope.modules.length; i++){
			if($scope.modules[i].quiz.length !== 0){
				var url = "/api/learner_qa/" + $scope.modules[i].quiz[0].id;
				console.log(url);
				req_array.push($http.get(url));
			};	
		};
		console.log("Req Array");
		console.log(req_array);
		$q.all(req_array).then(function(response) {
			$scope.learner_attempted_quizes = response;
			console.log("Learner Attempted Quizes:-");
			console.log(response);
			$scope.map_attempted_quizes();
	    }).catch(function(error){
		    console.log(error);
	    });
	};

	$scope.map_attempted_quizes = function(){
		console.log("Map Function Called");
		$scope.laq = [];
		for(var i = 0; i < $scope.learner_attempted_quizes.length; i++){
			if($scope.learner_attempted_quizes[i].data.length !== 0){
				$scope.laq.push($scope.learner_attempted_quizes[i].data);
			};
		};
		console.log($scope.laq);

		for(var i = 0; i < $scope.modules.length; i++){
			for(var j = 0; j < $scope.laq.length; j++){
				if($scope.modules[i].quiz[0] !== undefined){
					if($scope.modules[i].quiz[0].questions.length === $scope.laq[j].length){
						var array_size = $scope.laq[j].length;
						var lq_array = [];
						var mq_array = [];
						for(var k = 0; k < array_size; k++){
							mq_array.push($scope.modules[i].quiz[0].questions[k].text); 
							lq_array.push($scope.laq[j][k].quiz_question.text);
						};
						mq_array.sort();
						lq_array.sort();
						console.log(mq_array);
						console.log(lq_array);
						console.log(JSON.stringify(mq_array) === JSON.stringify(lq_array));
						if(JSON.stringify(mq_array) === JSON.stringify(lq_array)){
							$scope.modules[i].lq_exists = true;
							$scope.modules[i].learner_quiz = $scope.laq[j];
						};
					};
				};
			};
		};
		
		$scope.module_wise_calculate_score();			
	};

	$scope.module_wise_calculate_score = function(){
		console.log("Calculate Score");
		for(var i = 0; i < $scope.modules.length; i++){
			var score = 0			
			if($scope.modules[i].lq_exists){
				for(var j = 0; j < $scope.modules[i].learner_quiz.length; j++){
					if($scope.modules[i].learner_quiz[j].quiz_question.correct.text === $scope.modules[i].learner_quiz[j].chosen_option.text){
						score = score + 1;						
					};
				};
				$scope.modules[i].score = score;
				$scope.modules[i].percentage = (score / $scope.modules[i].learner_quiz.length) * 100;
			};
			console.log($scope.modules[i]);
			console.log($scope.modules[i].score);
			console.log($scope.modules[i].percentage);
		};
	};

	$scope.view_module = function(object, index){
		$scope.selected = object;
		if($scope.selected.topics === "undefined"){
			$scope.selected.topics = "No Topics Added."
		};
		try{
			$scope.selected.assignment_name = unescape($scope.selected.Assignment.split('/').pop());
		}
		catch(err){
			$scope.selected.assignment_name = "No File!";
		};
		try{
			$scope.selected.presentation_name = unescape($scope.selected.Presentation.split('/').pop());
		}
		catch(err){
			$scope.selected.presentation_name = "No File!";
		};
		try{
			$scope.selected.video_name = unescape($scope.selected.video.split('/').pop());
		}
		catch(err){
			$scope.selected.video_name = "No File!";
		};
		try{
			$scope.selected.reference_name = unescape($scope.selected.Refernce.split('/').pop());
		}
		catch(err){
			$scope.selected.reference_name = "No File!";
		};
	};

	$scope.take_quiz = function(object){
		$scope.module = object;
		$scope.quiz_name = object.quiz[0].quiz_name;
		$scope.questions = object.quiz[0].questions;
		$scope.selected_question = object.quiz[0].questions[0];
	};

	$scope.show_taken_quiz = function(object){
		console.log(object);
		$scope.quiz_name = object.quiz[0].quiz_name;
		$scope.learner_quiz_questions = object.learner_quiz;
		$scope.selected_answered_question = object.learner_quiz[0];		
	};

	$scope.select_question = function(question){
		$scope.selected_question = question;
	};

	$scope.select_answered_question = function(question){
		$scope.selected_answered_question = question;	
	};

	$scope.submit_quiz = function(){
		$scope.module.learner_quiz = [];
		for(var i=0; i < $scope.questions.length; i++){
			// If the user has selected an option
			if($scope.questions[i].selected !== null){
				var url = "/api/learner_qa/";
				var data= {
					"quiz_question": $scope.questions[i].url,
					"learner": "/api/learners/" + $scope.learner_id + "/",
					"chosen_option": $scope.questions[i].selected.url
				};
				$http.post(url, data).then(successCallback, errorCallback);			
				function successCallback(response){
					console.log(response);
					if(response.status === 201){
						$scope.module.lq_exists = true;
						$scope.module.learner_quiz.push(response.data);
						console.log($scope.module.learner_quiz);
						swal("Good job!", "Answers uploaded!", "success");
						console.log("Successfully Posted");
						console.log(i);
						if(i === ($scope.questions.length)){
							console.log(i);
							console.log(($scope.questions.length - 1));
							console.log("Now Calculate the score");
							$scope.module_wise_calculate_score();
							$('#quizModal').modal('hide');									
						};
					};
				};
				function errorCallback(error){
					console.log(error);
					swal("Oops!", "Something went wrong!", "error");			
				};	
			};
			// If the user has not selected an option then pass in the dummy answer with text "No Option Selected". Make sure to create one and pass it's id
			if($scope.questions[i].selected === null){
				var url = "/api/learner_qa/";
				var data= {
					"quiz_question": $scope.questions[i].url,
					"learner": "/api/learners/" + $scope.learner_id + "/",
					"chosen_option": "/api/answer_options/45/"
				};
				$http.post(url, data).then(successCallback, errorCallback);			
				function successCallback(response){
					$scope.module.lq_exists = true;
					$scope.module.learner_quiz.push(response.data);
					if(i === ($scope.questions.length)){
						console.log(i);
						console.log(($scope.questions.length - 1));
						console.log("Now Calculate the score");
						$scope.module_wise_calculate_score();									
					};
					swal("Good job!", "Answer uploaded!", "success");
				};
				function errorCallback(error){
					console.log(error);
					swal("Oops!", "Something went wrong!", "error");			
				};	
			};
		};
	};
});