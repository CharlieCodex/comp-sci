var connections = [];
var activeConn = 0;
var peer = new Peer({key: 'ej52dou975pnwmi',
					debug: 3,
					config: {'iceServers': [
					{url: 'stun:stun.l.google.com:19302'},
					{url: 'stun:stun1.l.google.com:19302'}
					]}});
var debug;
var name;

connections.send = function(msg){
	this.forEach(function(conn){
		conn.send(msg);
	});
}

$(document).ready(function($) {
	
});
function switchConn(index){
	var conn = connections[index];
	$('#cont'+activeConn).removeClass('selected');
	$('#conn'+activeConn).hide();
	$('#conn'+index).show();
	$('#cont'+index).addClass('selected');
	activeConn = index;
}
function initConn(conn){
	conn.div = $('#connP').clone(true,true).appendTo('#chatClient').attr('id', 'conn'+connections.indexOf(conn)).show();
	conn.tab = $('#contP').clone(true,true).appendTo('#contactList').attr('id', 'cont'+connections.indexOf(conn)).show();
	conn.tab.find('span').text(conn.peer);
	conn.tab.on('click',function(){
		var index = Number($(this).attr('id').substring(4));
		console.log("Switching to "+index)
		switchConn(index);
	});
	conn.on('open', function(){
		conn.send('name'+name);
		this.div.find('.chatLog').html("");
		this.on('data',function(data){
			console.log(data);
			//get data tag
			var tag = data.substring(0,data.indexOf(':'));
				info = data.substring(data.indexOf(':')+1);
			//handle data based on tag
			if(tag === 'msg'){
				appendMessage(this.index, info, false);
			}

			if(tag === 'name'){
				$('#cont'+this.index+' span').text(info);
			}
		});
	});
	switchConn(conn.index);
}

function htmlEncode(value){
  return $('<div/>').text(value).html();
}

function htmlDecode(value){
  return $('<div/>').html(value).text();
}

function appendMessage(conn, msg, local){
	var log = $('#conn'+conn+' .chatLog');
	var div = $('<div></div>');
	div.text(htmlDecode(htmlEncode(msg)));
	if(!local){
		div.attr('class', 'them');
	}
	var h = log.height();
	log.append(div);
	log.scrollTop(log[0].scrollHeight);
	log.height(h);
}