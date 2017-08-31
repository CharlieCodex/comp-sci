angular.module("CodexMessenger")
.directive('linkz', function(){
	return {
		restrict: 'A', // E = Element, A = Attribute, C = Class, M = Comment
		link: function(scope, elm, attrs){
			
			scope.peer = peer;

			peer.on('open',function(){

			});

			peer.on('connection',function(connection) {
				connections[connections.length] = connection;
				connection.index = connections.length-1;
				initConn(connection);
			});

			$('#addContactOverlay input').on('keypress',function(event){
				if(event.keyCode == 13){
					if($('#addContactOverlay input').val()!=""){
						var conn = peer.connect($('#addContactOverlay input').val());
						connections[connections.length] = conn;
						conn.index = connections.length-1;
						$('.overlay#addContactOverlay').show();
						initConn(conn);
					}
				}
			});
			
			$('#myInfoOverlay .closeOverlay').on('click', function() {
				if($('#myName').val()!==name){
					name = $('#myName').val();
					connections.send('name:'+name);
				}
			})
			$('.chatInput').on('keypress',function(event){
				var input = $(this);
				var connIn = Number(input.parent().parent().attr('id').substring(4));
				if(event.keyCode == 13){
					if(input.val()!=""){
						appendMessage(connIn,input.val(),true)
						connections[connIn].send('msg:'+input.val());
						input.val('');
					}
				}
			});
			$('#useStaticID').on('change', function(e) {
				if($(this).prop('checked')){
					$("#useCookies").prop("checked",true);
				}
			});

			$('#useCookies').on('change', function(e) {
				if(!$(this).prop('checked')){
					$("#useStaticID").prop("checked",false);
				}
			});
		}
	};
});