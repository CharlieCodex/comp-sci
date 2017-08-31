angular.module("CodexMessenger")
.directive("chatHole", function(){
	return {
		restrict:'E',
		templateUrl: 'templates/chat-hole-index.html'
	};
});