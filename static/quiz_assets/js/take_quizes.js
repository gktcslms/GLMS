var app = angular.module("take_quiz", []);

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
    var quiz_id = document.getElementById("quiz_id").innerHTML;
    var user_id = document.getElementById("user_id").innerHTML;
    document.getElementById("quiz_id").style.display = "none";
    document.getElementById("user_id").style.display = "none";
    $scope.score = 0;

    // Get the quiz questions

    $scope.get_quiz_questions = function(){
        var get_qq_url = "/api/quiz_all_quizes/" + quiz_id;
        $http.get(get_qq_url).then(successCallback, errorCallback);
        function successCallback(response){
            $scope.quiz_questions = response.data.questions;
            $scope.quiz_time = response.data.time_limit;
            $scope.selected_question = $scope.quiz_questions[0];
            console.log($scope.selected_question);
            $scope.seconds = $scope.quiz_time * 60;
        };
        function errorCallback(error){
            alert("Error Loading Page!");
        };
    };
    
    $scope.get_quiz_questions();

    // Timer Countdown Function
    timer = function(){
        var minutes = Math.round(($scope.seconds - 30)/60);
        var remainingSeconds = $scope.seconds % 60;
        if (remainingSeconds < 10) {
            remainingSeconds = "0" + remainingSeconds; 
        }
        console.log(minutes + ":" + remainingSeconds);
        document.getElementById('countdown').innerHTML = minutes + ":" + remainingSeconds;
        if ($scope.seconds == 0) {
            clearInterval($scope.countdownTimer);
            console.log("Your Quiz is Stopped...!");
            document.getElementById('countdown').innerHTML = "Your Quiz Time is up...!";
            $scope.submit_quiz();
        } else {
            $scope.seconds--;
        }
    };

    start_timer = function(){
        $scope.countdownTimer = setInterval('timer()', 1000);
    };

    // End Timer Countdown Function

    $scope.select_question = function(question){
        $scope.selected_question = question;
        console.log($scope.selected_question);
    };

    var submit_quiz = true;

    $scope.submit_quiz = function(){
        if(submit_quiz == true)
        {
            var post_questions_array = [];
            for(var i=0; i < $scope.quiz_questions.length; i++){
                // If option selected
                if ($scope.quiz_questions[i].selected != undefined){
                    var url = "/submit_quiz";
                    var data= {
                        "quiz_question_id": $scope.quiz_questions[i].id,
                        "user_id": user_id,
                        "chosen_answer_id": $scope.quiz_questions[i].selected.id,
                        "correct_answer_id": $scope.quiz_questions[i].correct.id,
                        "quiz_id": quiz_id 
                    };
                    post_questions_array.push($http.post(url, data));    
                    if($scope.quiz_questions[i].selected.id == $scope.quiz_questions[i].correct.id){
                        $scope.score += 1;
                        console.log($scope.score);
                    }
                }
                // If option not selected pass the dummy id of invalid answer in our case 135
                else{
                    var url = "/submit_quiz";
                    var data= {
                        "quiz_question_id": $scope.quiz_questions[i].id,
                        "user_id": user_id,
                        "chosen_answer_id": 135,
                        "correct_answer_id": $scope.quiz_questions[i].correct.id,
                        "quiz_id": quiz_id 
                    }
                    post_questions_array.push($http.post(url, data));
                };
            };
            console.log(post_questions_array);
            $q.all(post_questions_array).then(function(response) {
                console.log(response);

                // Submit score after successfuly storing answers
                var url = "/submit_score";
                var data = {
                    "user_id": user_id,
                    "score": $scope.score,
                    "quiz_id": quiz_id
                };
                $http.post(url, data).then(successCallback, errorCallback);
                function successCallback(response){
                    console.log(response);
                    Swal.fire({
                        type: 'success',
                        title: 'Quiz Submitted Successfully',
                        text: 'You can now check your score!',
                        onClose: () => {
                            location.reload();
                        }
                    });
                };
                function errorCallback(error){
                    console.log(error);
                    Swal.fire({
                        type: 'error',
                        title: 'Error Submitting Quiz',
                        text: 'Quiz could not be submitted',
                    });
                };		

                // End Submit score part

            }).catch(function(error){
                console.log(error);
                Swal.fire({
                    type: 'error',
                    title: 'Error Submitting Quiz',
                    text: 'Quiz could not be submitted',
                });
            });
        };
        submit_quiz = false;
    };
});