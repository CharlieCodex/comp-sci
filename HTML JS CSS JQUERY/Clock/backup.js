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
var Colors = colorBank[0];
var color = 0;
Date.prototype.monthDays= function(){
    var d = new Date(this.getFullYear(), this.getMonth()+1, 0);
    return d.getDate();
}
var canvas;
var ctx;
function init()
{
	canvas = document.getElementsByTagName('canvas')[0];
	ctx = canvas.getContext('2d');
	setInterval(update, 1000/60);
}
function rotateScheme(){
	color=(color+1)%colorBank.length;
	Colors = colorBank[color];
}
function millens(date)
{
	return Math.PI*(Math.floor(date.getFullYear()%10000/1000)/5-0.5);
}
function cents(date)
{
	return Math.PI*(Math.floor(date.getFullYear()%1000/100)/5-0.5);
}
function decs(date)
{
	return Math.PI*(Math.floor(date.getFullYear()%100/10)/5-0.5);
}
function years(date)
{
	return Math.PI*(date.getFullYear()%10/5 - 0.5);
}
function months(date)
{
	return Math.PI*(date.getMonth()/6-0.5);
}
function monthDays(date)
{
	return Math.PI*(date.getDate()/date.monthDays()*2-0.5);
}
function days(date)
{
	return Math.PI*(date.getDay()/3.5-0.5);
}
function hours(date)
{
	return Math.PI*(date.getHours()/6-0.5);
}
function minutes(date)
{
	return Math.PI*(date.getMinutes()/30-0.5);
}
function seconds(date)
{
	return Math.PI*(date.getSeconds()/30-0.5);
}
function millis(date)
{
	return Math.PI*(date.getMilliseconds()/500-0.5);
}

function update()
{
	ctx.save();

	var height = document.getElementById('div').clientHeight;
	var width = document.getElementById('div').clientWidth;
	var date = new Date();
	canvas.height = height;
	canvas.width = width;
	

	ctx.fillStyle = Colors[0];
	ctx.fillRect(0, 0,canvas.width,canvas.height);

	ctx.translate(width/2,height/2);

	if(height<width)
	{
		ctx.scale(height/700,height/700);
	}
	else
	{
		ctx.scale(width/700,width/700);
	}

	ctx.lineWidth=20;

	renderArc(millens(date),Colors[1],255);

	renderArc(cents(date),Colors[2],235);

	renderArc(decs(date),Colors[3],215);

	renderArc(years(date),Colors[4],195);

	renderArc(months(date),Colors[5],175);

	renderArc(monthDays(date),Colors[6],155);

	renderArc(hours(date),Colors[7],135);

	renderArc(minutes(date),Colors[8],115);

	renderArc(seconds(date),Colors[9],95);

	renderArc(millis(date),Colors[10],75);
	
	document.title = date.getHours()+':'+date.getMinutes()+':'+date.getSeconds()+'.'+date.getMilliseconds();

	ctx.restore();
}
function renderArc(value, color, dist)
{
	ctx.strokeStyle = color;
	ctx.beginPath();
	ctx.arc(0, 0, dist, value-0.25, value+0.25);
	ctx.stroke();
	//gridlines

	var old = ctx.lineWidth;
	ctx.lineWidth = 2;
	ctx.strokeStyle = '#eee'
	ctx.beginPath();
	ctx.arc(0, 0, dist-old/2,0, Math.PI*2);
	ctx.stroke();
	ctx.beginPath();
	ctx.arc(0, 0, dist+old/2,0, Math.PI*2);
	ctx.stroke();
	ctx.lineWidth = old;

}