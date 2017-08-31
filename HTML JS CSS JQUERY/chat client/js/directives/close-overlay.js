angular.module("CodexMessenger")
.directive('closeOverlay', function(){
	// Runs during compile
	return {
		restrict: 'E', // E = Element, A = Attribute, C = Class, M = Comment
		templateUrl: 'templates/close-overlay-index.html',
		link: function(scope, element, attrs) {
			element.children('button').attr('data-target','#'+element.parents('.modal').attr('id'));
		}
	};
});