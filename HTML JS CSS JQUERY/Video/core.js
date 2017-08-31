navigator.getWebcam = ( navigator.getUserMedia ||
						navigator.webkitGetUserMedia ||
						navigator.mozGetUserMedia ||
						navigator.msGetUserMedia);

var peer = new Peer({key: 'ej52dou975pnwmi',
					debug: 3,
					config: {'iceServers': [
					{url: 'stun:stun.l.google.com:19302'},
					{url: 'stun:stun1.l.google.com:19302'}
					]}});

peer.on('open', function(id){
	console.log('peer opened');
	$('#my-id').text(id);
});

peer.on('call', function(call){
	console.log('called');
	call.answer(window.localStream);
	step3(call);
})

$(function(){
	$('#make-call').click(function() {
		console.log('autocall attempt')
		var call = peer.call($('#callto-id').val(), window.localStream);
		step3(call);
	});
	$('#end-call').click(function() {
		window.existingCall.close();
		step2();
	});
	$('#step1-retry').click(function() {
		$('#step1-error').hide();
		step1();
	});

	step1();
});

function step1() {
	console.log('Step 1');
	navigator.getWebcam({audio: false, video: true}, function(stream){
			$('#my-video').prop('src',URL.createObjectURL(stream));
		
			window.localStream = stream;
			step2();
		}, function(){ $('#step1-error').show();});
}

function step2() {
	console.log('Step 2');
	$('#step1', '#step3').hide();
	$('#step2').show();
}

function step3(call)
{	
	console.log('Step 3');
	if(window.existingCall)
	{
		window.existingCall.close();
	}

	call.on('stream', function(stream){
		$('#thier-video').prop('src',URL.createObjectURL(stream));
	});

	$('#step1', '#step2').hide();
	$('#step3').show();
}