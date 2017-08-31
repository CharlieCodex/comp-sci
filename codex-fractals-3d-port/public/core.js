{
	Math.cotan = function(x) {
		return 1/this.tan(x);
	};
}


var points = [],
  dems = [2, 2, 2],
  angle = [0,0],
  viewpoint = [0, 0 , -50],
	canvas,
	jcanv,
	ctx,
	size,
	depth,
	mouse = [0, 0];

var settings = {},
	params = {},
	mousedown;

$(function() {

	jcanv = $('#out');

	//to unregerster / is added
	jcanv.on('mousemove', function(event){
		if(mousedown){
			var x = mouse[0]-event.originalEvent.clientX,
			y = mouse[1]-event.originalEvent.clientY;

			angle[0] += x*(Math.PI*4/jcanv.width());
			angle[1] += y*(Math.PI*4/jcanv.width());

			mouse[0] = event.originalEvent.clientX;
			mouse[1] = event.originalEvent.clientY;
		}
	});

	jcanv.on('mousedown', function(event){
		mousedown=true;
		mouse[0]=event.originalEvent.clientX;
		mouse[1]=event.originalEvent.clientY;
	  	fixAngle();
	});

	jcanv.on('mouseup mouseleave', function(event){
		mousedown=false;
	});
	
	canvas = jcanv[0];
	ctx = canvas.getContext('2d');
	ctx.imageSmoothingEnabled = "false";
	ctx.translate(canvas.width/2, canvas.height/2);
	ctx.scale(1,-1);
	size = canvas.width/1000;

	//settings

	$('.settings input[type=number]').on('change paste keyup', function(){
		var elm = $(this);
		settings[elm.attr('name')] = elm.val();
	}).change();
  
	$('.settings input[name=scale]').on('change paste keyup', function(){
		var elm = $(this);

		viewpoint[2] = -50 / Number(elm.val())
	})

	$('.settings input[name=angle0]').on('keyup change paste', function(){
		var elm = $(this);
		angle[0] = Number(elm.val());
		fixAngle();
	})

	$('.settings input[name=angle1]').on('keyup change paste', function(){
		var elm = $(this);
		angle[1] = Number(elm.val());
		fixAngle();
	}).change();

	$('.settings input[type=checkbox]').on('change', function(){
		var elm = $(this);
		settings[elm.attr('name')] = elm.is(':checked');
	}).change();

	var select = $('select[name=maps]');

	for(var mapper in maps) {
		if(maps.hasOwnProperty(mapper)) {
			select.append('<option>'+mapper+'</option>');
		}
	}


	select.on('change', function() {
		settings.maps = $(this).val();
		console.log(settings.maps);
	});


	select.val(select.children('option').first().val());

	select.change();
	
	$('select[name=color]').on('change', function() {
		settings.color = $(this).val();
		console.log(settings.color);
	}).change();

	$('.params input').on('change paste keyup', function(){
		var elm = $(this);
		params[elm.attr('name')] = elm.val();
	}).change();

})

function distance(p1, p2) {
  
  return Math.sqrt(
  	Math.pow(
  		p1[0]-
  		p2[0], 2)+
	Math.pow(
		p1[1]-
		p2[1], 2)+
	Math.pow(
		p1[2]-
		p2[2], 2));
  
}

function castCoord(point){

	//var out = rotate(point, angle);
	var out = linRot(point, angle[1], angle[0], 0)

	var z = distance(out, viewpoint);

	//adjust to viewpoint & flatten, keeping z as out last chord
	out = [(out[0]-viewpoint[0])/(z)*canvas.width, (out[1]-viewpoint[1])/(z)*canvas.width, z*Math.sign((out[2]-viewpoint[2]))];
	
	return out;

}

//depricated
function rotate(point, angle) {
  
 	var out = point.slice();
 	var tmp = rotate2d([out[0],out[2]],angle[0]);

 	out[0] = tmp[0];
	out[2] = tmp[1];

	tmp = rotate2d([out[2],out[1]],angle[1]);

	out[2] = tmp[0];
	out[1] = tmp[1];

	return out;
}
//mostly internal, used in some display/mapping equations
function rotate2d(point, angle) {
  
 	var out = [];

	var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));

	var theta = Math.atan2(point[1], point[0]);

	theta += angle;

	out[0] = Math.cos(theta) * r;

	out[1] = Math.sin(theta) * r;
  
  	return out;
}
/*
Linear algebra based rotation function

1st try:
	return [
		point[0]*(Math.cos(Y)*Math.cos(X))
			- point[1]*(Math.cos(Y)*Math.sin(Z))
			+ point[2]*Math.sin(Y),
		point[0]*(Math.cos(Z)*Math.pow(Math.sin(X),2)+Math.cos(X)*Math.sin(Z))
			+ point[1]*(Math.cos(X)*Math.cos(Z)+Math.pow(Math.sin(X),2)*Math.sin(Z))
			- point[2]*(Math.cos(X)*Math.sin(X)),
		point[0]*(-Math.cos(X)*Math.cos(Z)*Math.sin(Z)+Math.sin(X)*Math.sin(Z))
			+ point[1]*(Math.cos(Z)*Math.sin(X)+Math.cos(X)*Math.sin(X)*Math.sin(Z))
			+ point[2]*Math.pow(Math.cos(X),2)
	]

*/
function linRot(point, X, Y, Z){
	var tmp = point.slice(),
	a = point[0],
	b = point[1],
	c = point[2];

	tmp[0] = a * Math.cos(Y)*Math.cos(Z)
		+ c * Math.sin(Y)
		- b * Math.cos(Y)*Math.sin(Z);

	tmp[1] = - c * Math.cos(Y)*Math.sin(X)
		+ a * (Math.cos(Z)*Math.sin(X)*Math.sin(Y) + Math.cos(X)*Math.sin(Z))
		+ b * (Math.cos(X)*Math.cos(Z) - Math.sin(X)*Math.sin(Y)*Math.sin(Z))

	tmp[2] = c * Math.cos(Y)*Math.cos(X)
		+ a * (Math.sin(X)*Math.sin(Z) - Math.cos(X)*Math.cos(Z)*Math.sin(Y))
		+ b * (Math.cos(Z)*Math.sin(X) + Math.cos(X)*Math.sin(Y)*Math.sin(Z))

	return tmp;
}

function download() {
	//suspend drawing
	if(drawAnchor)window.clearInterval(drawAnchor);
	//convert to gif and download
	var a = document.createElement('a');
	a.download = 'fractal('+depth+').png';
	a.href = canvas.toDataURL('image/png');
	a.click();
	//resume drawing
	drawAnchor = window.setInterval(draw, 17);
}

function addPoints(){

	for(var i = 0; i < settings.points; i++) {
		//dems = [Number(settings['dems']),Number(settings['dems']),Number(settings['dems'])]
		points.push([(Math.random()*dems[0])-dems[0]/2, (Math.random()*dems[1])-dems[1]/2, (Math.random()*dems[2])-dems[2]/2]);

	}

}

function test() {
  points = [
    [-1,0,1],
    [0,1,0],
    [1,0,-1],
  ]
}

function clearAll() {

	console.log('clearing')

	if(drawAnchor)window.clearInterval(drawAnchor);
	depth = 0;

	ctx.fillStyle = '#fff';
	ctx.fillRect(-canvas.width/2, -canvas.height/2, canvas.width, canvas.height);

	points = []

}

function fixAngle(){
	$('input[name=angle0]').val(angle[0])
	$('input[name=angle1]').val(angle[1])
}