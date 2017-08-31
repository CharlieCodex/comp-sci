var op = {fill:true, borderColor : '#333', fillColor: '#b0eb00', borderThickness: 1};

$(function(){
	document.addEventListener('mousemove', function(e){
		if(isOverlapping(5,5,e.clientX,e.clientY,100)){
			console.log('cool shit')
		}
	});
	canvas = $('canvas')[0];
	ctx = canvas.getContext('2d');
	//renderHexHex(5,100, op);
})

function isOverlapping(x,y,x2,y2,size) {
	
	var x1 = x * size * 0.75;
	var y1 = y * size * Math.sqrt(3) / 2 + (x%2)*Math.sqrt(3)/4*size;

	return (dist(x1,y1,x2,y2)<=size/2)

}

function dist(x1,y1,x2,y2) {
	
	var a = Math.abs(x1 - x2);
	var b = Math.abs(y1 - y2);

	return Math.sqrt(Math.pow(a,2)+Math.pow(b,2));
}