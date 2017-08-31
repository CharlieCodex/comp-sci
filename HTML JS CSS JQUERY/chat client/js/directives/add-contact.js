angular.module("CodexMessenger")
.directive('addContact', function(){
	return {
		restrict: 'E', // E = Element, A = Attribute, C = Class, M = Comment
		templateUrl: 'templates/overlays/add-contact-index.html'
	};
});