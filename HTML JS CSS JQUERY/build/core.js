var canvas;
var ctx;
var loop;
var conn;
var peer = new Peer({key: 'ej52dou975pnwmi',
					debug: 3,
					config: {'iceServers': [
					{url: 'stun:stun.l.google.com:19302'},
					{url: 'stun:stun1.l.google.com:19302'}
					]}});
var debug;
$(document).ready(function($) {
	canvas = $('#gameView')[0];
	ctx = canvas.getContext('2d');
	peer.on('open',function(){
		$('#chatLog').html("Enter a peers id to connect</br>Your ID is "+peer.id);
		console.log($('#chatLog p')[0]);
	})
	peer.on('connection',function(connection) {
		conn = connection;
		initConn();
	});
	$('#chatSend').on('click',function(){
		if($('#chatInput').val()!=""){
			conn = peer.connect($('#chatInput').val());
			initConn();
		}
	});
	loop = window.setInterval(main,1000/60);
});
function main () {
	ctx.fillRect(0,0,100,100);
}
function initConn(){
	conn.on('open', function(){
			$('#chatLog').html("");
			conn.on('data',function(data){
				//get data tag
				var tag = data.substring(0,data.indexOf(':'));
				//handle data based on tag
				if(tag === 'msg'){
					appendMessage(data.substring(data.indexOf(':')+1),false);
				}
			});
		});
		$('#chatSend').unbind('click');
		$('#chatSend').on('click',function(){
			if($('#chatInput').val()!=""){
				appendMessage($('#chatInput').val(),true)
				conn.send('msg:'+$('#chatInput').val());
		$('#chatInput').val('');
			}
		});	
}
function htmlEncode(value){
  return $('<div/>').text(value).html();
}

function htmlDecode(value){
  return $('<div/>').html(value).text();
}
function appendMessage(msg, local){
	var log = $('#chatLog');
	var div = $('<div></div>');
	div.text(htmlDecode(htmlEncode(msg)));
	if(!local){
		div.attr('class', 'them');
	}
	$('#chatLog').append(div);
}