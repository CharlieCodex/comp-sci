var form;
var letter = {
	from:{},
	to:{}
}

function init(){
	letter.from.name = document.getElementById('name-return');
	letter.from.street = document.getElementById('street-return');
	letter.from.csz = document.getElementById('csz-return');
	letter.to.name = document.getElementById('name-to');
	letter.to.street = document.getElementById('street-to');
	letter.to.csz = document.getElementById('csz-to');
	form = document.forms[0];
}

function submit(){
	letter.from.name.innerHTML = form['name-from'].value;
	letter.from.street.innerHTML = form['street-from'].value;
	letter.from.csz.innerHTML = form['csz-from'].value;

	letter.to.name.innerHTML = form['name-for'].value;
	letter.to.street.innerHTML = form['street-for'].value;
	letter.to.csz.innerHTML = form['csz-for'].value;
}