var colorBank = [
	[
		'#FFFFFF',
		'#FFEB3B', //
		'#4CAF50', //
		'#F44336', //
		'#9C27B0', //
		'#673AB7', //
		'#FFC107', //
		'#8BC34A', //
		'#2196F3', //
		'#795548', //
		'#9E9E9E'
	],[
		'#FFFFFF',
		'#F44336', //
		'#E91E63', //
		'#9C27B0', //
		'#673AB7', //
		'#3F51B5', //
		'#2196F3', //
		'#03A9F4', //
		'#00BCD4', //
		'#009688', //
		'#4CAF50'
	],[
		'#FFFFFF',
		'#00BCD4', //
		'#009688', //
		'#4CAF50', //
		'#8BC34A', //
		'#CDDC39', //
		'#FFEB3B', //
		'#FFC107', //
		'#FF9800', //
		'#FF5722',
		'#F44336'
	]
]
var colors = colorBank[0];
var color = 0;
Date.prototype.monthDays= function(){
    var d = new Date(this.getFullYear(), this.getMonth()+1, 0);
    return d.getDate();
}
var canvas;
var ctx;
$(function()
{
	canvas = $('canvas')[0];
	ctx = canvas.getContext('2d');
	setInterval(update, 1000/60);
});
function rotateScheme(){
	color=(color+1)%colorBank.length;
	colors = colorBank[color];
}
var times = [
	{
		divs: 10,
		pos:function(date) {
			return Math.PI*(Math.floor(date.getFullYear()%10000/1000)/5-0.5);
		}
	},
	{
		divs: 10,
		pos: function (date)
		{
			return Math.PI*(Math.floor(date.getFullYear()%1000/100)/5-0.5);
		}
	},
	{
		divs: 10,
		pos: function (date)
		{
			return Math.PI*(Math.floor(date.getFullYear()%100/10)/5-0.5);
		}
	},
	{
		divs: 10,
		pos: function (date)
		{
			return Math.PI*(date.getFullYear()%10/5 - 0.5);
		}
	},
	{
		divs: 12,
		pos: function (date)
		{
			return Math.PI*(date.getMonth()/6-0.5);
		}
	},
	{
		divs: null,
		pos: function (date)
		{
			return Math.PI*(date.getDate()/date.monthDays()*2-0.5);
		}
	},
	{
		divs: 12,
		pos: function (date)
		{
			return Math.PI*(date.getHours()/6-0.5);
		}
	},
	{
		divs: null,
		pos: function (date)
		{
			return Math.PI*(date.getMinutes()/30-0.5);
		}
	},
	{
		divs: 12,
		pos: function (date)
		{
			return Math.PI*(date.getSeconds()/30-0.5);
		}
	},
	{
		divs: null,
		pos: function (date)
		{
			return Math.PI*(date.getMilliseconds()/500-0.5);
		}
	}
]
function update()
{
	ctx.save();

	var height = $('.container')[0].clientHeight;
	var width = $('.container')[0].clientWidth;

	var dem = height<width?height:width;

	var date = new Date();

	canvas.height = dem;
	canvas.width = dem;
	
	ctx.translate(dem/2,dem/2);

	ctx.scale(dem/700,dem/700);

	var day = (date.getHours()-6)%24<12;
	var theme = [
		['#fff','#eee'],
		['#000','#333']
	];
	theme = day?theme[0]:theme[1];

	if($('.container').attr('class').includes('night') && day) {
		$('.container').removeClass('night');
	} else if (!$('.container').attr('class').includes('night') && !day){
		$('.container').addClass('night');
	}

	ctx.fillStyle = theme[0];

	ctx.fillRect(-canvas.width/2, -canvas.height/2, canvas.width, canvas.height);

	if(day){

		//day
		var size = 75-10;
		ctx.fillStyle = '#2196F3';
		
		ctx.beginPath();
		ctx.arc(0, 0, size, -Math.PI, Math.PI);
		ctx.fill();


		ctx.fillStyle = '#FFEB3B';
		ctx.beginPath();
		ctx.arc(0, 0, size, Math.PI, Math.PI*3/2);
		ctx.arcTo(0, 0, -size, 0, size);
		ctx.fill();

	} else {

		//night
		var size = 75-10;
		ctx.fillStyle = '#eee';
		ctx.beginPath();
		ctx.arc(0, 0, size, Math.PI/2, -Math.PI/2);
		ctx.arcTo(-size*3,0,0,size,size);
		ctx.lineTo(0,size);
		ctx.fill();
	}


	ctx.lineWidth=20;

	for(var i = 0; i < times.length; i++){
		var dist = 255-i*ctx.lineWidth;
		renderGrid(times[i].divs, dist, colors[i+1]);
		renderArc(times[i].pos(date), colors[i+1], dist, times[i].divs);
	}

	ctx.strokeStyle = '#333';

	ctx.lineWidth = 2;

	ctx.beginPath();
	ctx.arc(0, 0, 65,0, Math.PI*2);
	ctx.stroke();

	ctx.restore();
}
function renderArc(value, color, dist, divs)
{
	var width = Math.PI / ((divs) || 12);
	ctx.strokeStyle = color;
	ctx.beginPath();
	ctx.arc(0, 0, dist, value-width, value+width);
	ctx.stroke();

}
function renderGrid(divs, dist, color)
{
	var width = ctx.lineWidth;
	//rings

	ctx.strokeStyle = color;

	ctx.globalAlpha=0.4;
	
	ctx.lineWidth = 20;

	ctx.beginPath();
	ctx.arc(0, 0, dist,0, Math.PI*2);
	ctx.stroke();

	ctx.strokeStyle = '#333';

	ctx.lineWidth = 4;

	//ctx.beginPath();
	//ctx.arc(0, 0, dist-width/2,0, Math.PI*2);
	//ctx.stroke();
	
	//ctx.beginPath();
	//ctx.arc(0, 0, dist+width/2,0, Math.PI*2);
	//ctx.stroke();

	//divisions
	if(divs){
		ctx.beginPath();
		for(var i = 0; i < divs; i++){
			var rads = 2 * Math.PI * (i / divs);
			var out = dist - width/2;
			ctx.moveTo(out*Math.cos(rads), out*Math.sin(rads));
			out += width;
			ctx.lineTo(out*Math.cos(rads), out*Math.sin(rads));
		}
		//ctx.stroke();
	}
	ctx.lineWidth = width;


	ctx.globalAlpha=1;
}