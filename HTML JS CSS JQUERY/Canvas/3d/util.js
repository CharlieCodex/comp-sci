var peer = new Peer({key: 'ej52dou975pnwmi',
					debug: 3,
					config: {'iceServers': [
					{url: 'stun:stun.l.google.com:19302'},
					{url: 'stun:stun1.l.google.com:19302'}
					]}});
var conn;
var isHost = false;
var ball = {
	x:0,
	y:0,
	z:1,
	vector:{
		x:1,
		y:1
	},
	towards:false,
	lastPos:0
};
peer.paddle = {
	x:0,
	y:0,
	z:2
};
$(function(){
	canvas = document.getElementById('canvas');
	ctx = canvas.getContext('2d');
	ctx.save();
	ctx.translate(canvas.width/2, canvas.height/2);
	$('#new-room').click(function(){
		window.location.reload(true);
	})
	$('#connect').click(function(){
		conn = peer.connect($('#conn-id').val());
		initConn();
	});
});
peer.on('open', function() {
	$('#my-id').text(peer.id);
});
peer.on('error', function(err){
	console.log(err.type);
	if(err.type === 'peer-unavailable'){
		$('#my-id').text(peer.id);
		window.alert('Connection failed... Check Peer ID')
		console.log('caught');
	}
});
peer.on('connection', function(connection){
	conn = connection;
	conn.on('open', function(){
		conn.send('startGame');
		initConn();
	});
  	isHost = true;
	console.log('host');
  	startGame();
});

function startGame()
{
	$('#conn-info').hide();
	mainLoop = window.setInterval(update, 1000/60);
}

var sync = {
	ball: null,
	paddle: null
};
function initConn(){
	conn.on('data', function(data){
		//console.log(data);
		if(isHost){
			console.log(typeof(data));
		}
		if(data === 'startGame'){
			startGame();
		}
		if(data === 'hit'){
			oppScore++;
			$('#opp-Score').text('Opponent: '+oppScore);
			document.title = score + ' vs ' + oppScore;
		}
		if(data === 'you-hit'){
			score++;
			$('#your-Score').text('Your Score: '+score);
			document.title = score + ' vs ' + oppScore;
		}
		if(data.ball != null && data.ball != undefined){
			sync.ball = data.ball;
		}
		if(data.paddle != null && data.paddle != undefined){
			sync.paddle = data.paddle;
		}
		if(data.x != null && data.x != undefined
			&& data.y != null && data.y != undefined){
			if(isHost){
				ball.vector.x = (ball.vector.x + data.x + Math.random(-2, 2))/3;
				ball.vector.y = (ball.vector.y + data.y + Math.random(-2, 2))/3;
				oppScore++;
				$('#opp-Score').text('Opponent: '+oppScore);
				document.title = score + ' vs ' + oppScore;
			}
		}
	});
}
function mouseUpdate(e)
{
	var pos = getPosition(canvas);
	peer.paddle.x = ( e.clientX - pos.x - canvas.width/2 ) * peer.paddle.z;
	peer.paddle.y = ( e.clientY - pos.y - canvas.height/2 ) * peer.paddle.z;
	if(peer.paddle.x < 96 - canvas.width/2){
		peer.paddle.x = 96 - canvas.width/2
	}
	if(peer.paddle.x > - 96 + canvas.width/2){
		peer.paddle.x = -96 + canvas.width/2
	}
	if(peer.paddle.y < 48 - canvas.height/2){
		peer.paddle.y = 48 - canvas.height/2
	}
	if(peer.paddle.y > - 48 + canvas.height/2){
		peer.paddle.y = -48 + canvas.height/2
	}
}
function keyUpdate(e)
{
	console.log(e);
	//if(e.keyCode == 119){ball.z = (ball.z<40) ? ball.z+1 : ball.z}
	//if(e.keyCode == 115){ball.z = (ball.z>1) ? ball.z-1 : ball.z}
}
function getPosition(element) {
    var xPosition = 0;
    var yPosition = 0;
  
    while(element) {
        xPosition += (element.offsetLeft - element.scrollLeft + element.clientLeft);
        yPosition += (element.offsetTop - element.scrollTop + element.clientTop);
        element = element.offsetParent;
    }
    return { x: xPosition, y: yPosition };
}
function toConnUpdate (e) {
	$('#connect')[0].disabled = ($('#conn-id').val() != "" && $('#conn-id').val() != peer.id) ? false : true;
}