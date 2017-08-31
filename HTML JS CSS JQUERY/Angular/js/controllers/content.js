angular.module("Playground")
.controller("ContentController", function(){
	this.conversations = [];
	this.conversation = 0;
	this.switchConversation = function(conv){
		this.conversation = conv==null?0:conv;
	};
	this.isConversation = function(conv){
		return this.conversation === conv;
	};
});