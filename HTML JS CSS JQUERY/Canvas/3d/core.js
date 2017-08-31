var canvas;
var ctx;
var mainLoop;
var oppScore = 0;
var score = 0;
function invertPaddle() {
	return {
		x: peer.paddle.x * -1,
		y: peer.paddle.y,
		z: 3.5
	};
}
function invertBall() {
	var tmp = {};
	tmp.z = 5.5-ball.z;
	tmp.y = ball.y;
	tmp.x = ball.x * -1;
	tmp.vector = {
		x: 0,
		y: 0
	}
	tmp.towards = !ball.towards;
	//tmp.forwards = !ball.forwards;
	return tmp;
}
function ballUpdate(){
	return Math.abs(new Date().getMilliseconds()-499.5)/499.5*1.5+2;
	//Old sine ball move thing: 
	//return Math.sin(new Date().getMilliseconds()/999*Math.PI)*2.5+1.25;
}
function update(){
	if(isHost){
		ball.z = ballUpdate();
		var toSend = {
			ball: invertBall(),
			paddle: invertPaddle()
		};
		conn.send(toSend);
	}else{
		ball = sync.ball;
		var toSend = {
			paddle: invertPaddle()
		};
		conn.send(toSend);
	}
	ball.x+=ball.vector.x;
	ball.y+=ball.vector.y;
	if(Math.abs(ball.x)>=canvas.width/2)
	{
		ball.vector.x = -ball.vector.x
	}
	if(Math.abs(ball.y)>=canvas.height/2)
	{
		ball.vector.y = -ball.vector.y
	}
	if(ball.lastPos<ball.z && ball.towards){
		ball.towards = isHost ? !ball.towards : ball.towards;
		console.log('near');
		if(ball.x >= peer.paddle.x-128 && ball.x <= peer.paddle.x+128 && ball.y >= peer.paddle.y-96 && ball.y <= peer.paddle.y+96 ){
			console.log('hit');
			if(isHost){
				ball.vector.x = (ball.vector.x + (ball.x-peer.paddle.x)/12 + Math.random(-2, 2))/3;
				ball.vector.y = (ball.vector.y + (ball.y-peer.paddle.y)/8 + Math.random(-2, 2))/3;
				conn.send('hit');
				console.log('hit message sent');
			
			}else{
				console.log('yolo dude')
				conn.send({
					x: (ball.x-peer.paddle.x)/12,
					y: (ball.y-peer.paddle.y)/8
				});
			}
			score++;
			$('#your-score').text('Your Score: '+score);
			document.title = score + ' vs ' + oppScore;
			//console.log('hit: '+ball.vector.x+', '+ball.vector.y);
		}
	}
	if(ball.lastPos>ball.z && !ball.towards){
		console.log('far')
				ball.towards = isHost ? !ball.towards : ball.towards;
				if(ball.x >= sync.paddle.x-128 && ball.x <= sync.paddle.x+128 && ball.y >= sync.paddle.y-96 && ball.y <= sync.paddle.y+96 ){
					ball.vector.x = (ball.vector.x + (ball.x-sync.paddle.x)/12 + Math.random(-2, 2))/3;
					ball.vector.y = (ball.vector.y + (ball.y-sync.paddle.y)/8 + Math.random(-2, 2))/3;

					conn.send('you-hit');

					oppScore++;
					$('#your-score').text('Your Score: '+score);
					document.title = score + ' vs ' + oppScore;
				}
	}
	ball.lastPos = ball.z;
	draw();
}
function draw(){
	//Clear Screen
	ctx.fillStyle = 'white';
	ctx.fillRect(-canvas.width/2,-canvas.height/2,canvas.width,canvas.height);
	//Thier Paddle
	ctx.fillStyle = 'rgba(255,0,0,0.25)';
	ctx.fillRect((sync.paddle.x-96)/sync.paddle.z,(sync.paddle.y-48)/sync.paddle.z, 192/sync.paddle.z, 96/sync.paddle.z);
	//Rectangle Rendering
	ctx.lineWidth = 5;
	for (var i = 2; i <= 3.5; i+=0.5) {
		ctx.lineWidth = 5/i;
		ctx.rect(-canvas.width/2/i,-canvas.height/2/i, canvas.width/i, canvas.height/i);
		ctx.stroke();
	};
	//Ball Rendering
	ctx.beginPath();
	ctx.fillStyle = 'black';
	ctx.arc(ball.x/ball.z, ball.y/ball.z, 64/ball.z, 0, 2 * Math.PI, false);
	ctx.fill();
	//Paddle Rendering
	ctx.fillStyle = 'rgba(0,255,0,0.25)';
	ctx.fillRect((peer.paddle.x-96)/peer.paddle.z, (peer.paddle.y-48)/peer.paddle.z, 192/peer.paddle.z, 96/peer.paddle.z);

}