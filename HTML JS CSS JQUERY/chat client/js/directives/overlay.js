angular.module("CodexMessenger")
.directive('overlay', function(){
	// Runs during compile
	return {
		restrict: 'A', // E = Element, A = Attribute, C = Class, M = Comment
		link: function($scope, element, attrs, controller) {
			$scope.$watch('overlay.overlay',function(val){
				if(val==attrs.overlay){
					element.removeClass('ng-hide');
					element.find('input').first().focus();;
				}else{
					element.addClass('ng-hide');
				}
			});
			element.addClass('overlay');
		}
	};
});