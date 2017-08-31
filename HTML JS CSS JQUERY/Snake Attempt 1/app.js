var xlen=0; var ylen=0;
var score = 0;
var scoreLabel;
var cells;
var food;
var colorArray = ['#ff0000','#ff4400','#ff8800','#ffbb00','#ffff00','#88ff00','#00ff00','#00ff88','#00ffff','#00bbff','#0088ff','#0044ff','#0000ff'];
var speed = 125;
var keyEnum =
{
	dontMove: -1,
	left: 0,
	up: 1,
	right: 2,
	down: 3
};
var direction = keyEnum.right;
var tempDirection = keyEnum.right;
var moveClock = setInterval(update, speed);
var table;

function updateCell(cell, pos)
{
	var refinedPos = Math.abs((pos%(colorArray.length*2-1))-colorArray.length+1);

	if(pos == -1)
	{
		cell.setAttribute('bgcolor', '#ffffff');
		return;
	}
	cell.setAttribute('bgcolor', colorArray[refinedPos]);
	if(pos==cells.length-1)
	{
		cell.setAttribute('bgcolor', '#ffffff');
	}
}

function pushCell(cell)
{
	oldCells = cells;
	newCells = new Array(cells.length);
	if(typeof(cells[cells.length])!=typeof(undefined))
	{
		updateCell(oldCells[oldCells.length],-1);
	}
	newCells[0] = cell
	for (var i = 0; i<oldCells.length; i++)
	{
		if(i != 0)
		{
			newCells[i] = oldCells[i-1]
		}
		if(typeof(newCells[i])!==typeof(undefined))
		{
			updateCell(newCells[i],i);
		}
	}
	cells = newCells;

}

function onKeyPressed()
{
	console.log(event.keyCode)
	var dir = tempDirection;
	switch(event.keyCode)
	{
		case 32: restart(); break;
		case 37: dir = keyEnum.left; break;
		case 38: dir = keyEnum.up; break;
		case 39: dir = keyEnum.right; break;
		case 40: dir = keyEnum.down; break;
	}
	if(dir%2==direction%2){return;}
	tempDirection = dir;
}

function update()
{
	direction = tempDirection;
	moveDirection();
	food.setAttribute('bgcolor','#000000');
	if(cells[0]==food)
	{
		eatFood();
	}
}

function moveDirection()
{
	if(direction>keyEnum.dontMove)
	{
		var cell = cells[0];
		var row = cell.parentNode.rowIndex;
		var col = cell.cellIndex;
		switch(direction)
		{
			case keyEnum.left: col-=1; break;
			case keyEnum.up: row-=1; break;
			case keyEnum.right: col+=1; break;
			case keyEnum.down: row+=1; break;
		}
		var table = document.getElementById('tbl01');
		pushCell(table.rows[row].cells[col]);
	}
}

function getCellFromPos(x, y)
{
	var table = document.getElementById('tbl01');
	var rows = table.rows;
	return rows[x].cells[y];
}

function onMouseOver(x, y)
{
	var table = document.getElementById('tbl01')
	var rows = table.rows
	var cell = rows[x].cells[y]
	var hasIndex = false;
	for(var i = 0; i < cells.length; i++)
	{
		hasIndex = (cells[i]==cell)
		if(hasIndex)
		{
			return;
		}
	}
	pushCell(cell);
}

function eatFood()
{
	score++;
	scoreLabel.innerHTML = 'Score: ' + score;
	var size = cells.length;
	var oldCells = cells;
	speed*=0.9;
	window.clearInterval(moveClock);
	moveClock = setInterval(update,speed)
	cells = new Array(size+5);
	for(var i = 0; i<oldCells.length; i++)
	{
		cells[i]=oldCells[i];
	}
	food.setAttribute('bgcolor', '#ffffff');
	food = getCellFromPos(Math.round(Math.random()*50)-1, Math.round(Math.random()*50)-1);
}

function restart()
{
	table.remove();
	direction = keyEnum.dontMove;
	tempDirection = keyEnum.dontMove;
	init(xlen, ylen);
}

function init(x, y)
{
	score = 0;
	xlen = x;
	ylen = y;
	switch(document.getElementById('difficulty').selectedIndex)
	{
		case 0: speed = 150; break;
		case 1: speed = 125; break;
		case 2: speed = 100; break;
	}
	console.log(document.getElementById('difficulty').selectedIndex);
	moveClock = window.clearInterval(moveClock);
	moveClock = setInterval(update,speed);
	table = tableCreate(x, y) //Make out table
	cells = new Array(5) //Setuo starting snake length
	onMouseOver(2,2); //Set-up first block of the snake
	food = getCellFromPos(48, 48); //Initialize the food
	scoreLabel = document.getElementById('scoreLabel'); //Grab the score label
	eatFood(); //Randomize the food location, and verify the score label is working
}

function tableCreate(x, y)
{
	var div = document.getElementById('tableDiv');
	var tbl = document.createElement('table');
	var tbdy = document.createElement('tbody');
	tbl.setAttribute('id','tbl01');
	tbl.setAttribute('class','fixed');
	for (var i = 0; i < x; i++) {
	    var tr = document.createElement('tr');
		for (var j = 0; j < y; j++) {
    		var td = document.createElement('td');
			td.appendChild(document.createTextNode(''));
            tr.appendChild(td);
        }
    	tbdy.appendChild(tr);
    }
   	tbl.appendChild(tbdy);
   	div.appendChild(tbl);
   	return tbl;
}