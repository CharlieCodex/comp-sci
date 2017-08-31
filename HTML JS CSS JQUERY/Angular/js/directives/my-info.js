angular.module("CodexMessenger")
.directive("myInfo", function(){
	return {
		restrict:'E',
		templateUrl: 'templates/my-info-index.html'
	};
});