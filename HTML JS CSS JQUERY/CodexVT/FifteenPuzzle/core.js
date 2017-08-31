var debug = {};
var empty = {
	x:3,
	y:3
};
function init() {
	initBoard();
}
function initBoard() {
	var table = document.getElementById('game-board');
	for (var r = 0; r < 4; r++) {
		var row = document.createElement('tr');
		for(var d = 0; d < 4; d++){
			var detail = document.createElement('td');
			detail.id = r+"."+d;
			if(d+4*r+1 != 16){
				detail.innerHTML=d+4*r+1;
				detail.classList.add("tile"+(((d+r)%2 == 0)?"-white":"-red"));
			}else{
				debug.detail = detail;
				detail.classList.add("tile-empty");
			}
			detail.setAttribute("onclick", "switchTile(this.id)");
			row.appendChild(detail);
		}
		table.appendChild(row);
	}
}
function scrambleBoard(){
	var table = document.getElementById('game-board');
	var cellsLeft = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
	for (var r = 0; r < 4; r++) {
		var row = table.rows[r];
		for(var d = 0; d < 4; d++){
			var detail = row.cells[d];
			detail.id = r+"."+d;
			if(d+4*r+1 != 16){
				var num = getRandomInt(0, cellsLeft.length);
				detail.innerHTML=cellsLeft[num];
				var y = (cellsLeft[num]-1)%4;
				var x = Math.floor((cellsLeft[num]-1)/4);
				console.log(cellsLeft[num]+": "+x+" , "+y)
				detail.classList = ("tile"+(((x+y)%2==0)?"-white":"-red"));
				cellsLeft[num] = '';
			}
			cellsLeft = cellsLeft.filter(function(str) {
			    return /\S/.test(str);
			});
		}
	}
}
function switchTile(id){
	var split = id.split(".")
	var x = split[0];
	var y = split[1];
	if(Math.pow(x-empty.x, 2) + Math.pow(y-empty.y, 2)==1){
		var tmp = document.getElementById(empty.x+"."+empty.y);
		tmp.innerHTML=document.getElementById(id).innerHTML;
		tmp.classList = document.getElementById(id).classList;
		tmp = document.getElementById(id);
		tmp.innerHTML="";
		tmp.classList=["tile-empty"];
		empty.x = x;
		empty.y = y;
	}
	if(checkBoard()){
		window.alert("You Win!")
	}
}
function checkBoard() {
	var table = document.getElementById('game-board');
	var good = true;
	for (var r = 0; r < 4; r++) {
		var row = table.rows[r];
		for(var d = 0; d < 4; d++){
			var detail = row.cells[d];
			detail.id = r+"."+d;
			if(d+4*r+1 != 16){
				if(detail.innerHTML != d+4*r+1)good=false;
			}
		}
	}
	return good;
}
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}