var canvas;
var ctx;
function renderHex(x, y, size, options) {

	options = $.extend({
		border: true,
		borderColor: '#000000',
		borderThickness: 5,

		fill: false,
		fillColor: '#000000'
	}, options);

	ctx.beginPath();
	ctx.moveTo(x-size/2,y);
	ctx.lineTo(x-size/4,y-size/4*Math.sqrt(3));
	ctx.lineTo(x+size/4,y-size/4*Math.sqrt(3));

	ctx.lineTo(x+size/2,y);
	ctx.lineTo(x+size/4,y+size/4*Math.sqrt(3));
	ctx.lineTo(x-size/4,y+size/4*Math.sqrt(3));
	ctx.lineTo(x-size/2,y);
	
	if(options.fill){
		ctx.fillStyle = options.fillColor;
		ctx.fill();
	}

	if(options.border){
		ctx.lineWidth = options.borderThickness;
		ctx.strokeStyle = options.borderColor;
		ctx.stroke();
	}
}
function renderGridHex(x,y,size,options){
	console.log('Drawing hexagon at ('+x+', '+y+')')
	var shiftx = x*0.75*size,
		shifty = y*size*Math.sqrt(3)/2 + (x%2)*Math.sqrt(3)/4*size;
	renderHex(shiftx,shifty,size,options);
}
function renderHexArray(width, height, size, options){
	var shiftx = options.x ? options.x : 0;
	var shifty = options.y ? options.y : 0;

	for (var x = 0; x < width; x++) {
		for (var y = 0; y < height; y++) {
			renderGridHex(x + shiftx, y + shifty,size,options);
		};
	};
}
function renderHexHex(x,y,size,options){

	renderGridHex(x,y-2, size, options);
	for (var j = -1; j < 2; j++) {
		for(var i = -2; i < 3; i++){
			renderGridHex(x+i, y+j,size,options);
		}
	};

	for (var i = -1; i < 2; i++) {
		renderGridHex(x+i,y+2,size,options);
	};

}