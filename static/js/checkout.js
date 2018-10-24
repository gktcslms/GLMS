var app = angular.module("checkout", []);

app.config(function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	$httpProvider.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';
	$httpProvider.defaults.useXDomain = true;
	$httpProvider.defaults.headers.common['Accept'] = 'application/json, text/javascript';
});

app.controller('myCtrl', function($scope, $http, $q, $window) {
    console.log("Checkout.js Loaded");
    var cart = document.getElementById("cart").innerHTML;
    $scope.cart = JSON.parse(cart);
    $scope.courses_ids = [];
    for(i = 0; i < $scope.cart.length; i++){
        $scope.cart[i].time = 1;
        // $scope.cart[i].cost = 10;
        $scope.cart[i].cost = $scope.cart[i].fees;
        $scope.courses_ids.push($scope.cart[i].id);
    }
    console.log("courses_ids");
    console.log($scope.courses_ids);
    $scope.total_cost = 0;
    for(i = 0; i < $scope.cart.length; i++){
        $scope.total_cost = $scope.total_cost + $scope.cart[i].cost;        
    }
    $("#cart").hide();

    // Start Paypal Section
    paypal.Button.render({
        
        //env: 'sandbox', // sandbox | production
        env: 'production', // sandbox | production

        // PayPal Client IDs - replace with your own
        // Create a PayPal app: https://developer.paypal.com/developer/applications/create
        client: {
            // My Keys
            // sandbox:    'AZDxjDScFpQtjWTOUtWKbyN_bDt4OgqaF4eYXlewfBP4-8aqX3PiV8e1GWU6liB2CUXlkA59kJXE7M6R',
            // TEST APP
            // sandbox: 'AWLD_ucGZ0ICt-L-CJSUh2L1Hz5xsxfxscngWC-M0AMqfGWd_XO3tmw8y9Ke5gx1a9zZup6YwQ5H3GXC',
            // production: 'Afz2dSzSuchdJWgK39Qbli8AeeXbwuvLmdcStXN_cY4oXLhxKCI5vWP2YEkh8oRIXYqP9CYjPl1SdXrn'
            // Surendra Sir's Paypal Merchant Key
            production: 'Aduo5FUAsdfk3WOP2CpArJ8cMvhND5aT-6x4I0qOMVdJamZFUslsGv1tzScqejS8o9y-73SyG-IkrM9C'
        },

        // Show the buyer a 'Pay Now' button in the checkout flow
        commit: true,

        // payment() is called when the button is clicked
        payment: function(data, actions) {

            // Make a call to the REST api to create the payment
            return actions.payment.create({
                payment: {
                    transactions: [
                        {
                            amount: { total: $scope.total_cost, currency: 'INR' }
                        }
                    ]
                }
            });
        },

        // onAuthorize() is called when the buyer approves the payment
        onAuthorize: function(data, actions) {

            // Make a call to the REST api to execute the payment
            return actions.payment.execute().then(function(data) {
                // window.alert('Payment Complete!');
                console.log(data);
                $scope.paymentId = data.id;
                // $scope.provide_access();
                swal("Payment Done Successfully.", {
                    icon: "success",
                });
                $scope.access_provide();
            })
            .catch(function(error){
                console.log(error);
                $scope.show_payment_error();
            });
        }

    }, '#paypal-button');
    // End Paypal Section

    $scope.access_provide = function(){
        console.log("Access PROVISION");
        $scope.access = JSON.stringify("YES");
        // POST
		var url = "/provide_acess_on_payment/";
		var data= {
            "access": $scope.access,
            "courses_ids": $scope.courses_ids
		};
		$http.post(url, data).then(successCallback, errorCallback);			
		function successCallback(response){
            console.log(response);
            if(response.data === 'Access Provided 200 All Ok')
            {
                console.log("Redirect to the receipts section.");
                console.log($window.location);
                $window.location.href = '/my_receipts/';
            }
            else{
                console.log(response.data)
            }
		};
		function errorCallback(error){
			console.log(error);
			swal("Oops!", "Check your internet connection!", "error");			
		};
    };
    
    $scope.provide_access = function(){
        // var basicAuthString = btoa('CLIENTID:SECRET');
        // var basicAuthString = btoa('Afln2JlWLddwsD3r0vpqZbfe0J23yzIJ9u1uE2FkitbWz63NSdsOuYv5Le_G5BJS_kATV9U9wzWJwcqL:EAe2oCIowPMWVs3GJWcvLair8YBS4fyqmd0t5oDKmPZAzZqJbQ0ASUjDtq8bwKqeV69VqC51HNlOqbmL');
        var basicAuthString = btoa('AWLD_ucGZ0ICt-L-CJSUh2L1Hz5xsxfxscngWC-M0AMqfGWd_XO3tmw8y9Ke5gx1a9zZup6YwQ5H3GXC:EGmcgYVox0omtdNVTzkR67jNT8Rw2UOkixg7lsbooLPR7O_l2eT_pLmLRsFz6PBqF-NWXQJOGcC_l70r');
        $http({
            method: 'POST',
            url: 'https://api.sandbox.paypal.com/v1/oauth2/token',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + basicAuthString,
            },
            data: 'grant_type=client_credentials'
        }).then(successCallback, errorCallback);
        function successCallback(response){
            console.log(response.data);
            console.log(response.data.access_token);
            console.log(response.data.token_type);
            // swal("Payment Successful!", {
            //     icon: "success",
            // });
            $scope.access_token = response.data.access_token;
            $scope.token_type = response.data.token_type;

            $scope.validate_payment();
        };
        function errorCallback(error){
            console.log(error);
        };
    };

    $scope.validate_payment = function(){
        console.log("Validating Payment");
        console.log($scope.paymentId);
        console.log($scope.access_token);
        console.log($scope.token_type);
        $http({
            method: 'GET',
            url: 'https://api.sandbox.paypal.com/v1/payments/' + $scope.paymentId + '/',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': $scope.token_type + ' ' + $scope.access_token,
            }, 
        }).then(successCallback, errorCallback);
        function successCallback(response){
            swal(response, {
                icon: "success",
            });
        };
        function errorCallback(error){
            console.log(error);
        };
    }

    $scope.show_payment_error = function(){
        console.log("Something went wrong!");
        swal("Deleted Successfully.", {
            icon: "warning",
        });
    };
});