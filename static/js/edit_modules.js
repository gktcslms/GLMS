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
	console.log("My Controller");

	$scope.form_info = {};
	
	var course_id = document.getElementById("course_id").innerHTML;
	var url = "/api/courses/";
	var query_string = url + course_id + "/";

	$scope.query_string = query_string;

	$http.get(query_string).then(successCallback, errorCallback);	
	function successCallback(response){
		$scope.course = response.data;
		$scope.modules = $scope.course.modules;
		$scope.sortableOptions = {
			stop: function(e, ui) {
				$scope.update_order(); 
			},
		};
	};
	function errorCallback(error){
		alert("Error Loading Page!");
	};

	$scope.update_order = function(){
		for(var i = 0; i < $scope.modules.length; i++){
			$scope.modules[i].order = i + 1;			
			var data = {
				"order": $scope.modules[i].order
			};
			var url = $scope.modules[i].url;
			$http.patch(url, data).then(successCallback, errorCallback);
			function successCallback(response){
			};
			function errorCallback(error){
			};		
		}		
	};

	$scope.delete_module = function(object, index){
		swal({
			title: "Are you sure?",
			text: "Once Deleted, you will not be able to recover!",
			icon: "warning",
			buttons: true,
			dangerMode: true,
		  })
		  .then((willDelete) => {
			if (willDelete) {
				$http.delete(object.url).then(successCallback, errorCallback);	
				function successCallback(response){
					$scope.modules.splice(index, 1);
					$scope.update_order();
					swal("Deleted Successfully.", {
						icon: "success",
					});
				};
				function errorCallback(error){
					swal("Deleting Cancelled!");					
				};
			} else {
			  swal("Deleting Cancelled!");
			}
		  });			
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
			$scope.selected.labsession_name = unescape($scope.selected.labsession.split('/').pop());
		}
		catch(err){
			$scope.selected.labsession_name = "No File!";
		};
		try{
			$scope.selected.reference1_name = unescape($scope.selected.reference1.split('/').pop());
		}
		catch(err){
			$scope.selected.reference1_name = "No File!";
		};
		try{
			$scope.selected.reference2_name = unescape($scope.selected.reference2.split('/').pop());
		}
		catch(err){
			$scope.selected.reference2_name = "No File!";
		};
		try{
			$scope.selected.reference3_name = unescape($scope.selected.reference3.split('/').pop());
		}
		catch(err){
			$scope.selected.reference3_name = "No File!";
		};
		try{
			$scope.selected.video_name = unescape($scope.selected.video.split('/').pop());
		}
		catch(err){
			$scope.selected.video_name = "No File!";
		};
	};

	$scope.edit_module = function(object, index){
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
			$scope.selected.labsession_name = unescape($scope.selected.labsession.split('/').pop());
		}
		catch(err){
			$scope.selected.labsession_name = "No File!";
		};
		try{
			$scope.selected.reference1_name = unescape($scope.selected.reference1.split('/').pop());
		}
		catch(err){
			$scope.selected.reference1_name = "No File!";
		};
		try{
			$scope.selected.reference2_name = unescape($scope.selected.reference2.split('/').pop());
		}
		catch(err){
			$scope.selected.reference2_name = "No File!";
		};
		try{
			$scope.selected.reference3_name = unescape($scope.selected.reference3.split('/').pop());
		}
		catch(err){
			$scope.selected.reference3_name = "No File!";
		};
		try{
			$scope.selected.video_name = unescape($scope.selected.video.split('/').pop());
		}
		catch(err){
			$scope.selected.video_name = "No File!";
		};
		// POPULATE FORM DATA
		$scope.form_info = $scope.selected;
	};


	//Change Module Name Part
	$scope.change_module_name = function(){
		var data = {
			"name":$scope.form_info.name
		};
		var url = $scope.selected.url;
		$http.patch(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			swal("Name Changed!", "Module Name Updated Successfully!", "success");
		};
		function errorCallback(error){
			swal("Oops!", "Something went wrong!", "error");
		};
	}


	//Change Topic Name Part	
	$scope.change_topic = function(){
		var data = {
			"topics":$scope.form_info.topics
		};
		var url = $scope.selected.url;
		$http.patch(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			swal("Topic Changed!", "Topics Updated Successfully!", "success");
		};
		function errorCallback(error){
			swal("Oops!", "Something went wrong!", "error");
		};
	};
	// Change Preview Option Part
	$scope.toggle_preview = function(){
		console.log($scope.selected.allow_preview);
		$scope.selected.allow_preview = !($scope.selected.allow_preview);
		console.log($scope.selected.allow_preview);
		console.log($scope.form_info.allow_preview);
		var data = {
			"allow_preview":$scope.form_info.allow_preview
		};
		var url = $scope.selected.url;
		$http.patch(url, data).then(successCallback, errorCallback);
		function successCallback(response){
			swal("Preview Option Changed!", "Preview Status Successfully Changed!", "success");
		};
		function errorCallback(error){
			console.log(error);
			swal("Oops!", "Something went wrong!", "error");
		};
	};
	//Video Upload Part	
	$scope.vdo_upload = function(){
		var file_selected = false;		
		var element = document.getElementById("vdo");
		if (element.files[0] === undefined){
			swal("No File Chosen!", "Please select a file to be uploaded!", "error");
		}
		else{
			file_selected = true;
		};
		if (file_selected === true){
		    $scope.show_vdo_progrsess_bar = true;			
			var url = $scope.selected.url;
			var fd = new FormData();
			var canceller = $q.defer();
			$scope.vdo_cancel = function(){
				swal({
					title: "Are you sure?",
					text: "Once aborted, you will not be able to resume!",
					icon: "warning",
					buttons: true,
					dangerMode: true,
				  })
				  .then((willDelete) => {
					if (willDelete) {
					  swal("Upload Cancelled!");
					  canceller.resolve();
					} else {
					  swal("Resuming file upload.", {
						icon: "success",
					});
					}
				  });			
			};
			fd.append('video', element.files[0]);
			$http.patch(url, fd, {
				transformRequest: angular.identity,
				headers: {'Content-Type': undefined},
				uploadEventHandlers: {
					progress: function (e) {
							  if (e.lengthComputable) {
								$scope.vdoprogressBar = Math.floor((e.loaded / e.total) * 95);
							  }
					}
				},
				timeout: canceller.promise
			}).then(successCallback, errorCallback);
			function successCallback(response){
				if (response.status === 200){
					$scope.selected.video = response.data.video;
					$scope.selected.video_name = $scope.selected.video.split('/').pop();
					$scope.selected.video_name = unescape($scope.selected.video_name);
					$scope.vdoprogressBar = $scope.vdoprogressBar + 5;
					$scope.show_vdo_progrsess_bar = false;
					swal("Good job!", "Your file is uploaded!", "success");
				}
			};
			function errorCallback(error){
				if (error.status === -1){
					swal("Aborted!", "File Uploaded Was Aborted!", "error");									
				}
				else{
                    console.log(error)
					swal("Oops!", "Something went wrong....!", "error");									
				}
				$scope.show_vdo_progrsess_bar = false;
			};
		};
	};

	//Assignment Upload Part
	$scope.assignment_upload = function(){
		var file_selected = false;		
		var element = document.getElementById("ass");
		if (element.files[0] === undefined){
			swal("No File Chosen!", "Please select a file to be uploaded!", "error");
		}
		else{
			file_selected = true;
		};
		if (file_selected === true){
		    $scope.show_ass_progrsess_bar = true;			
			var url = $scope.selected.url;
			var fd = new FormData();
			var canceller = $q.defer();
			$scope.ass_cancel = function(){
				swal({
					title: "Are you sure?",
					text: "Once aborted, you will not be able to resume!",
					icon: "warning",
					buttons: true,
					dangerMode: true,
				  })
				  .then((willDelete) => {
					if (willDelete) {
					  swal("Resuming file upload.", {
						icon: "success",
					  });
					} else {
					  swal("Upload Cancelled!");
					  canceller.resolve();
					}
				  });			
			};
			fd.append('Assignment', element.files[0]);
			$http.patch(url, fd, {
				transformRequest: angular.identity,
				headers: {'Content-Type': undefined},
				uploadEventHandlers: {
					progress: function (e) {
							  if (e.lengthComputable) {
								$scope.assprogressBar = Math.floor((e.loaded / e.total) * 95);
							  }
					}
				},
				timeout: canceller.promise
			}).then(successCallback, errorCallback);
			function successCallback(response){
				if (response.status === 200){
					$scope.selected.Assignment = response.data.Assignment;
					$scope.selected.assignment_name = $scope.selected.Assignment.split('/').pop();
					$scope.selected.assignment_name = unescape($scope.selected.assignment_name);
					$scope.assprogressBar = $scope.assprogressBar + 5;
					$scope.show_ass_progrsess_bar = false;
					swal("Good job!", "Your file is uploaded!", "success");
				}
			};
			function errorCallback(error){
				if (error.status === -1){
					swal("Aborted!", "File Uploaded Was Aborted!", "error");									
				}
				else{
					swal("Oops!", "Something went wrong....!", "error");									
				}
				$scope.show_ass_progrsess_bar = false;
			};
		};
	};


	//Presentation Upload Part
	$scope.presentation_upload = function(){
		var file_selected = false;		
		var element = document.getElementById("pres");
		console.log(element)
		if (element.files[0] === undefined){
			swal("No File Chosen!", "Please select a file to be uploaded!", "error");
		}
		else{
			file_selected = true;
		};
		if (file_selected === true){
		    $scope.show_pres_progrsess_bar = true;			
			var url = $scope.selected.url;
			var fd = new FormData();
			var canceller = $q.defer();
			$scope.pres_cancel = function(){
				swal({
					title: "Are you sure?",
					text: "Once aborted, you will not be able to resume!",
					icon: "warning",
					buttons: true,
					dangerMode: true,
				  })
				  .then((willDelete) => {
					if (willDelete) {
					  swal("Resuming file upload.", {
						icon: "success",
					  });
					} else {
					  swal("Upload Cancelled!");
					  canceller.resolve();
					}
				  });			
			};
			fd.append('Presentation', element.files[0]);
			$http.patch(url, fd, {
				transformRequest: angular.identity,
				headers: {'Content-Type': undefined},
				uploadEventHandlers: {
					progress: function (e) {
							  if (e.lengthComputable) {
								$scope.presprogressBar = Math.floor((e.loaded / e.total) * 95);
							  }
					}
				},
				timeout: canceller.promise
			}).then(successCallback, errorCallback);
			function successCallback(response){
				if (response.status === 200){
					$scope.selected.Presentation = response.data.Presentation;
					$scope.selected.presentation_name = $scope.selected.Presentation.split('/').pop();
					$scope.selected.presentation_name = unescape($scope.selected.presentation_name);
					$scope.presprogressBar = $scope.presprogressBar + 5;
					$scope.show_pres_progrsess_bar = false;
					swal("Good job!", "Your file is uploaded!", "success");
				}
			};
			function errorCallback(error){
				if (error.status === -1){
					swal("Aborted!", "File Uploaded Was Aborted!", "error");									
				}
				else{
					swal("Oops!", "Something went wrong....!", "error");									
				}
				$scope.show_pres_progrsess_bar = false;
			};
		};
	};

	//Lab Session Upload Part
	$scope.lab_upload = function(){
		var file_selected = false;		
		var element = document.getElementById("lab");
		if (element.files[0] === undefined){
			swal("No File Chosen!", "Please select a file to be uploaded!", "error");
		}
		else{
			file_selected = true;
		};
		if (file_selected === true){
		    $scope.show_lab_progrsess_bar = true;			
			var url = $scope.selected.url;
			var fd = new FormData();
			var canceller = $q.defer();
			$scope.lab_cancel = function(){
				swal({
					title: "Are you sure?",
					text: "Once aborted, you will not be able to resume!",
					icon: "warning",
					buttons: true,
					dangerMode: true,
				  })
				  .then((willDelete) => {
					if (willDelete) {
					  swal("Resuming file upload.", {
						icon: "success",
					  });
					} else {
					  swal("Upload Cancelled!");
					  canceller.resolve();
					}
				  });			
			};
			fd.append('labsession', element.files[0]);
			$http.patch(url, fd, {
				transformRequest: angular.identity,
				headers: {'Content-Type': undefined},
				uploadEventHandlers: {
					progress: function (e) {
							  if (e.lengthComputable) {
								$scope.labprogressBar = Math.floor((e.loaded / e.total) * 95);
							  }
					}
				},
				timeout: canceller.promise
			}).then(successCallback, errorCallback);
			function successCallback(response){
				if (response.status === 200){
					$scope.selected.labsession = response.data.labsession;
					console.log(response.data.labsession);
					$scope.selected.labsession_name = $scope.selected.labsession.split('/').pop();
					$scope.selected.labsession_name = unescape($scope.selected.labsession_name);
					$scope.labprogressBar = $scope.labprogressBar + 5;
					$scope.show_lab_progrsess_bar = false;
					swal("Good job!", "Your file is uploaded!", "success");
				}
			};
			function errorCallback(error){
				if (error.status === -1){
					swal("Aborted!", "File Uploaded Was Aborted!", "error");									
				}
				else{
					swal("Oops!", "Something went wrong....!", "error");									
				}
				$scope.show_lab_progrsess_bar = false;
			};
		};
	};

	//Reference1 Upload Part
	$scope.reference1_upload = function(){
		var file_selected = false;		
		var element = document.getElementById("reference1");
		if (element.files[0] === undefined){
			swal("No File Chosen!", "Please select a file to be uploaded!", "error");
		}
		else{
			file_selected = true;
		};
		if (file_selected === true){
		    $scope.show_reference1_progrsess_bar = true;			
			var url = $scope.selected.url;
			var fd = new FormData();
			var canceller = $q.defer();
			$scope.reference1_cancel = function(){
				swal({
					title: "Are you sure?",
					text: "Once aborted, you will not be able to resume!",
					icon: "warning",
					buttons: true,
					dangerMode: true,
				  })
				  .then((willDelete) => {
					if (willDelete) {
					  swal("Resuming file upload.", {
						icon: "success",
					  });
					} else {
					  swal("Upload Cancelled!");
					  canceller.resolve();
					}
				  });			
			};
			fd.append('reference1', element.files[0]);
			$http.patch(url, fd, {
				transformRequest: angular.identity,
				headers: {'Content-Type': undefined},
				uploadEventHandlers: {
					progress: function (e) {
							  if (e.lengthComputable) {
								$scope.reference1progressBar = Math.floor((e.loaded / e.total) * 95);
							  }
					}
				},
				timeout: canceller.promise
			}).then(successCallback, errorCallback);
			function successCallback(response){
				if (response.status === 200){
					$scope.selected.reference1 = response.data.reference1;
					$scope.selected.reference1_name = $scope.selected.reference1.split('/').pop();
					$scope.selected.reference1_name = unescape($scope.selected.reference1_name);
					$scope.reference1progressBar = $scope.reference1progressBar + 5;
					$scope.show_reference1_progrsess_bar = false;
					swal("Good job!", "Your file is uploaded!", "success");
				}
			};
			function errorCallback(error){
				if (error.status === -1){
					swal("Aborted!", "File Uploaded Was Aborted!", "error");									
				}
				else{
					swal("Oops!", "Something went wrong....!", "error");									
				}
				$scope.show_reference1_progrsess_bar = false;
			};
		};
	};

	//Reference2 Upload Part
	$scope.reference2_upload = function(){
		var file_selected = false;		
		var element = document.getElementById("reference2");
		if (element.files[0] === undefined){
			swal("No File Chosen!", "Please select a file to be uploaded!", "error");
		}
		else{
			file_selected = true;
		};
		if (file_selected === true){
		    $scope.show_reference2_progrsess_bar = true;			
			var url = $scope.selected.url;
			var fd = new FormData();
			var canceller = $q.defer();
			$scope.reference2_cancel = function(){
				swal({
					title: "Are you sure?",
					text: "Once aborted, you will not be able to resume!",
					icon: "warning",
					buttons: true,
					dangerMode: true,
				  })
				  .then((willDelete) => {
					if (willDelete) {
					  swal("Resuming file upload.", {
						icon: "success",
					  });
					} else {
					  swal("Upload Cancelled!");
					  canceller.resolve();
					}
				  });			
			};
			fd.append('reference2', element.files[0]);
			$http.patch(url, fd, {
				transformRequest: angular.identity,
				headers: {'Content-Type': undefined},
				uploadEventHandlers: {
					progress: function (e) {
							  if (e.lengthComputable) {
								$scope.reference2progressBar = Math.floor((e.loaded / e.total) * 95);
							  }
					}
				},
				timeout: canceller.promise
			}).then(successCallback, errorCallback);
			function successCallback(response){
				if (response.status === 200){
					$scope.selected.reference2 = response.data.reference2;
					$scope.selected.reference2_name = $scope.selected.reference2.split('/').pop();
					$scope.selected.reference2_name = unescape($scope.selected.reference2_name);
					$scope.reference2progressBar = $scope.reference2progressBar + 5;
					$scope.show_reference2_progrsess_bar = false;
					swal("Good job!", "Your file is uploaded!", "success");
				}
			};
			function errorCallback(error){
				if (error.status === -1){
					swal("Aborted!", "File Uploaded Was Aborted!", "error");									
				}
				else{
					swal("Oops!", "Something went wrong....!", "error");									
				}
				$scope.show_reference2_progrsess_bar = false;
			};
		};
	};
	
	//Reference3 Upload Part
	$scope.reference3_upload = function(){
		var file_selected = false;		
		var element = document.getElementById("reference3");
		if (element.files[0] === undefined){
			swal("No File Chosen!", "Please select a file to be uploaded!", "error");
		}
		else{
			file_selected = true;
		};
		if (file_selected === true){
		    $scope.show_reference3_progrsess_bar = true;			
			var url = $scope.selected.url;
			var fd = new FormData();
			var canceller = $q.defer();
			$scope.reference3_cancel = function(){
				swal({
					title: "Are you sure?",
					text: "Once aborted, you will not be able to resume!",
					icon: "warning",
					buttons: true,
					dangerMode: true,
				  })
				  .then((willDelete) => {
					if (willDelete) {
					  swal("Resuming file upload.", {
						icon: "success",
					  });
					} else {
					  swal("Upload Cancelled!");
					  canceller.resolve();
					}
				  });			
			};
			fd.append('reference3', element.files[0]);
			$http.patch(url, fd, {
				transformRequest: angular.identity,
				headers: {'Content-Type': undefined},
				uploadEventHandlers: {
					progress: function (e) {
							  if (e.lengthComputable) {
								$scope.reference3progressBar = Math.floor((e.loaded / e.total) * 95);
							  }
					}
				},
				timeout: canceller.promise
			}).then(successCallback, errorCallback);
			function successCallback(response){
				if (response.status === 200){
					$scope.selected.reference3 = response.data.reference3;
					$scope.selected.reference3_name = $scope.selected.reference3.split('/').pop();
					$scope.selected.reference3_name = unescape($scope.selected.reference3_name);
					$scope.reference3progressBar = $scope.reference3progressBar + 5;
					$scope.show_reference3_progrsess_bar = false;
					swal("Good job!", "Your file is uploaded!", "success");
				}
			};
			function errorCallback(error){
				if (error.status === -1){
					swal("Aborted!", "File Uploaded Was Aborted!", "error");									
				}
				else{
					swal("Oops!", "Something went wrong....!", "error");									
				}
				$scope.show_reference3_progrsess_bar = false;
			};
		};
	};	
	// Unpopulate form
	// Empty Form
	$scope.empty_form = function(){
		console.log("Empty Form");	
		$('#add_form')[0].reset();
	};


	// New Module Add
	$scope.add_module = function(){
		console.log("add colled");
		$scope.vdo_element = document.getElementById("new_vdo");
		$scope.pres_element = document.getElementById("new_pres");
		$scope.ass_element = document.getElementById("new_ass");
		$scope.lab_element = document.getElementById("new_lab");
		$scope.reference1_element = document.getElementById("new_reference1");
		$scope.reference2_element = document.getElementById("new_reference2");
		$scope.reference3_element = document.getElementById("new_reference3");

		$scope.fd = new FormData();	
		$scope.show_addmodule_progrsess_bar = true;
		var canceller = $q.defer();	

		if ($scope.vdo_element.files[0] === undefined){
		}
		else{
			$scope.fd.append('video', $scope.vdo_element.files[0]);	
		};

		if ($scope.ass_element.files[0] === undefined){
		}
		else{
			$scope.fd.append('Assignment', $scope.ass_element.files[0]);	
		};

		if ($scope.pres_element.files[0] === undefined){
		}
		else{
			$scope.fd.append('Presentation', $scope.pres_element.files[0]);	
		};
		if ($scope.lab_element.files[0] === undefined){
		}
		else{
			$scope.fd.append('labsession', $scope.lab_element.files[0]);	
		};
		if ($scope.reference1_element.files[0] === undefined){
		}
		else{
			$scope.fd.append('reference1', $scope.reference1_element.files[0]);	
		};
		if ($scope.reference2_element.files[0] === undefined){
		}
		else{
			$scope.fd.append('reference2', $scope.reference2_element.files[0]);	
		};
		if ($scope.reference3_element.files[0] === undefined){
		}
		else{
			$scope.fd.append('reference3', $scope.reference3_element.files[0]);	
		};
		$scope.fd.append('name', $scope.new_module_name);
		$scope.fd.append("topics", $scope.new_module_topics);
		$scope.fd.append("part_of", $scope.query_string);
		$scope.fd.append("order", $scope.modules.length + 1);

		var url = "/api/courses_modules/"

		$scope.add_cancel = function(){
			swal({
				title: "Are you sure?",
				text: "Once aborted, you will not be able to resume!",
				icon: "warning",
				buttons: true,
				dangerMode: true,
			  })
			  .then((willDelete) => {
				if (willDelete) {
				  swal("Upload Cancelled!");
				  canceller.resolve();
				} else {
				  swal("Resuming Module upload.", {
					icon: "success",
				});
				}
			  });			
		};

		$http.post(url, $scope.fd, {
			transformRequest: angular.identity,
			headers: {'Content-Type': undefined},
			uploadEventHandlers: {
				progress: function (e) {
						  if (e.lengthComputable) {
							$scope.show_add_progrsess_bar = true;
							$scope.addmodule_progressBar = Math.floor((e.loaded / e.total) * 95);
						  }
				}
			},
			timeout: canceller.promise
		}).then(successCallback, errorCallback);

		function successCallback(response){
			if (response.status === 201){
				swal("Good job!", "New module uploaded!", "success");
				$scope.new_module = response.data;				
				$scope.modules.push($scope.new_module);			
				$scope.addmodule_progressBar = $scope.addmodule_progressBar + 5;	
				$scope.show_add_progrsess_bar = false;
			};
		};
		function errorCallback(error){
			if (error.status === -1){
				swal("Aborted!", "Module Uploaded Was Aborted!", "error");									
			}
			else{
				swal("Oops!", "Something went wrong!", "error");
			};
			$scope.show_add_progrsess_bar = false;			
		};
	};


	// QUIZ PART
	$scope.quiz = function(object){
		if (object.quiz[0] !== undefined){
			console.log("Quiz Present");
			$scope.quiz_name = object.quiz[0].quiz_name;
			$scope.quiz_present = true;		
			$scope.questions = object.quiz[0].questions;
			if ($scope.questions.length !== 0){
				$scope.selected_question = $scope.questions[0];
				$scope.selected_question.correct = $scope.questions[0].correct;
				$scope.selected_question.option_1 = $scope.selected_question.possible_answers[0];
				$scope.selected_question.option_2 = $scope.selected_question.possible_answers[1];
				$scope.selected_question.option_3 = $scope.selected_question.possible_answers[2];
				$scope.selected_question.option_4 = $scope.selected_question.possible_answers[3];
			}
			else{
				console.log("Add first Question!");
				$scope.selected_question = null;
			};
		}
		else{
			console.log("Quiz Not Present");
			$scope.quiz_name = "";
			$scope.quiz_present = false;						
		};

		// Change the name of quiz if present or create new if not present
		$scope.change_quiz_name = function(){
			console.log("Change Quiz Name");
			console.log($scope.quiz_name);
			// IF QUIZ PRESENT
			if ($scope.quiz_present === true){
				$scope.quiz_url = object.quiz[0].url;
				console.log($scope.quiz_url);
				var url = $scope.quiz_url;
				console.log(url);
				var data = {
					"quiz_name": $scope.quiz_name
				}; 
				console.log(data);
				$http.patch(url, data).then(successCallback, errorCallback);
				function successCallback(response){
					if (response.status === 200){
						swal("Good job!", "Quiz Name Updated!", "success");
					}
				};
				function errorCallback(error){
					console.log(error);
					swal("Oops!", "Something went wrong!", "error");					
				};			
			};
			// END IF QUIZ PRESENT

			// IF QUIZ NOT PRESENT
			if ($scope.quiz_present === false){
				var url = object.url;
				var data = {"quiz": [{
					"quiz_name": $scope.quiz_name,
					// "questions": [{}]
				}]}; 
				console.log(data);
				$http.patch(url, data).then(successCallback, errorCallback);
				function successCallback(response){
					if (response.status === 200){
						$scope.quiz_present = true;
						object.quiz = response.data.quiz;
						console.log(object.quiz);
						swal("Good job!", "Quiz Name Updated!", "success");
					}
					console.log(response);
					$scope.selected_question = {};
					$scope.questions = [];
				};
				function errorCallback(error){
					console.log(error);
					swal("Oops!", "Something went wrong!", "error");					
				};			
			};
			// END IF QUIZ NOT PRESENT
		};

		$scope.select_question = function(quest){
			$scope.selected_question = quest;
			$scope.selected_question.option_1 = $scope.selected_question.possible_answers[0];
			$scope.selected_question.option_2 = $scope.selected_question.possible_answers[1];
			$scope.selected_question.option_3 = $scope.selected_question.possible_answers[2];
			$scope.selected_question.option_4 = $scope.selected_question.possible_answers[3];
		};
	
		$scope.select_new_question = function(){
			$scope.selected_question = null;
		}
	
		$scope.save_question = function(){
			if($scope.selected_question.url === undefined || $scope.selected_question.url === null){
				$scope.save_new_question();
			}
			else{
				$scope.save_old_question();
			};
		};
	
		$scope.save_new_question = function(){
			console.log("Save New Question");
			var url = "/api/quiz_questions/"
			var data = {
				"quiz": object.quiz[0].url,
				"q_type": "MCQ",
				"text": $scope.selected_question.text,
				"possible_answers": [
					{
						"text": $scope.selected_question.option_1.text
					},
					{
						"text": $scope.selected_question.option_2.text
					},
					{
						"text": $scope.selected_question.option_3.text
					},
					{
						"text": $scope.selected_question.option_4.text
					}
				],
				"selected": null,
				"correct": {"text": $scope.selected_question.correct.text}
			};
			$http.post(url, data).then(successCallback, errorCallback);
			function successCallback(response){
				console.log("Response");
				console.log(response.data);
				console.log($scope.selected_question);
				console.log($scope.selected_question.possible_answers);
				$scope.selected_question.possible_answers = [];
				$scope.selected_question.possible_answers.push({"text": $scope.selected_question.option_1.text});
				$scope.selected_question.possible_answers.push({"text": $scope.selected_question.option_2.text});
				$scope.selected_question.possible_answers.push({"text": $scope.selected_question.option_3.text});
				$scope.selected_question.possible_answers.push({"text": $scope.selected_question.option_4.text});
				console.log($scope.selected_question.possible_answers);
				$scope.selected_question.url = response.data.url;
				$scope.questions.push($scope.selected_question);
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
			console.log($scope.selected_question.possible_answers[0]);
			var data = {
				"quiz": $scope.selected_question.quiz,
				"q_type": "MCQ",
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

		$scope.delete_question = function(){
			console.log("DELETE THE SELECTED QUESTION:-");
			console.log($scope.selected_question.url);
			var url = $scope.selected_question.url;
			$http.delete(url).then(successCallback, errorCallback);	
			function successCallback(response){
				swal("Deleted Successfully.", {
					icon: "success",
				});
				var index = $scope.questions.indexOf($scope.selected_question);
				console.log(index);
				// $scope.questions.splice(index, 1);				
				$scope.questions.splice( $scope.questions.indexOf($scope.selected_question), 1 );
				console.log($scope.questions.length);
				$scope.selected_question = $scope.questions[index];
			};
			function errorCallback(error){
				swal("Deleting Cancelled!");					
			};
		};
	};
	// END QUIZ PART
	
	//EMPTY Form on modal close
	$('#quizModal').on('hidden.bs.modal', function () {
		// $(this).find('form').trigger('reset');
		// $scope.selected_question = null;
	});
});