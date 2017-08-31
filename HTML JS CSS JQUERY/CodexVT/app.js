var ul;
var input;
function init() {
	ul = document.getElementById('stuff');
	input = document.getElementById('toAdd');
}
function onClick() {
	console.log("You clicked the button");
	var newItem = document.createElement('li');
	newItem.textContent = input.value;
	ul.appendChild(newItem);
	input.value = "";
}