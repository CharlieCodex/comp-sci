function open(id,source)
{
	var div = document.getElementById(id);
	div.setAttribute('class','open');
	console.log('Opened '+div+'. Event: ',source);
	source.setAttribute('onclick','close('+id+', '+source+')');
}
function close(id,source)
{
	var div = document.getElementById(id);
	div.setAttribute('class','closed');
	console.log('Closed '+div+'. Event: ',source);
	source.setAttribute('onclick','open('+id+', '+source+')');
}