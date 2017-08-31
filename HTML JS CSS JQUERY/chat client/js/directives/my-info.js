angular.module("CodexMessenger")
.directive("myInfo", function(){
	return {
		restrict:'E',
		templateUrl: 'templates/overlays/my-info-index.html'
	};
});