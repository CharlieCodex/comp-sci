var debug;
angular.module("CodexMessenger")
.controller('UtilController', ['$scope','$element', function($scope, $element){
	$scope.connections = [
		{
			name:"Al Gore",
			lastMsg:"Sounds good!",
			unread:5
		},

		{
			name:"Dank Master Dunk",
			lastMsg:"Ghadda go fast",
			unread:undefined
		},

		{
			name:"Bill Nye",
			lastMsg:"Better reply thoughtfully to this one",
			unread:2
		},

		{
			name:"Neil D. Tyson",
			lastMsg:"People say the universe don't be how it is but it do",
			unread:50
		}
	];
	$scope.myId = peer.id;
	$scope.tryConnection = function(id){
		var newConn = peer.connect(id);
		newConn.on('open', function(){
			connections.push(this);
			this.name = this.id;
		})
	}
	console.log($scope.connections)
}])