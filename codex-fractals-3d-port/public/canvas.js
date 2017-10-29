var drawAnchor;
var debug = {};
function startDraw() {
	if(settings.deep){

		clearAll();
		addPoints();
		drawAnchor = window.setInterval(draw, 17);

	} else {

		if(points.length === 0){

			addPoints();
			depth = 0;
		
		}

		draw();
	}

}

function draw() {

	//console.log(depth);
	if(!settings.keep){
		ctx.fillStyle = 'rgba(255,255,255,0.125)';
		if(settings.color=='inverted'){
			ctx.fillStyle = 'rgba(0,0,0,1)';
		}

		ctx.fillRect(-canvas.width/2, -canvas.height/2, canvas.width, canvas.height);
	}

	if(settings.axis || settings.grid){
		ctx.strokeStyle = 'rgb(0,255,0)';
		ctx.lineWidth = size/10;

		var vecs = [
			castCoord([10,0,0]),
			castCoord([0,10,0]),
			castCoord([0,0,10]),
		]

		var thetas = [
			Math.atan2(vecs[0][1],vecs[0][0]),
			Math.atan2(vecs[1][1],vecs[1][0]),
			Math.atan2(vecs[2][1],vecs[2][0])]

		var intersects = [[[],[]],[[],[]],[[],[]]];

		for(var i = 0; i < thetas.length; i++) {
			//evaluates j = -1 and j = 1
			for(var j = -1; j <= 1; j+=2) {
				var tmp = Math.cotan(thetas[i])*canvas.height/2*j;
				if(Math.abs(tmp) > canvas.width/2) {
					tmp = Math.tan(thetas[i])*canvas.width/2*j;
					intersects[i][(j+1)/2] = [canvas.width/2*j, tmp];
				} else {
					intersects[i][(j+1)/2] = [tmp, canvas.height/2*j];
				}
			}
			if(settings.axis) {
				switch(i){
					case 0: 
						ctx.strokeStyle = 'rgb(255,0,0)';
						break;
					case 1: 
						ctx.strokeStyle = 'rgb(0,255,0)';
						break;
					case 2: 
						ctx.strokeStyle = 'rgb(0,0,255)';
						break;
				}

				ctx.beginPath();
				//ctx.moveTo(intersects[i][0][0],intersects[i][0][1]);
				//ctx.lineTo(intersects[i][1][0],intersects[i][1][1]);
				ctx.stroke();
			}

		}

		//gridlines, so i guess just evenly spaced lines parellel to the axis?
		if(settings.grid){

			for(var i = 0; i < thetas.length; i++){
				switch(i){
					case 0: 
						ctx.strokeStyle = 'rgba(255,0,0,0)';
						break;
					case 1: 
						ctx.strokeStyle = 'rgba(0,255,0,0)';
						break;
					case 2: 
						ctx.strokeStyle = 'rgba(0,0,255,0)';
						break;
				}
				/*
				for(var j = 0; j <= 5; j++){
					var disp1 = [(j-2) * (vecs[(i+1)%3][0]), (j-2) * (vecs[(i+1)%3][1])];
					for(var K = -1; K <= 1; K++){
						var disp2 = [(K) * (vecs[(i+2)%3][0]),(K) * (vecs[(i+2)%3][1])];
						//disp2 = [0,0];
						var h = disp1[0] + disp2[0],
							k = disp1[1] + disp2[1];

						var drawPoints = [[],[]];

						for(var J = -1; J <= 1; J+=2) {
							var tmp = Math.cotan(thetas[i])*(canvas.height/2*J-k)+h;
							if(Math.abs(tmp) > canvas.width/2) {
								tmp = Math.tan(thetas[i])*(canvas.width/2*J-h)+k;
								drawPoints[(J+1)/2] = [canvas.width/2*J, tmp];
							} else {
								drawPoints[(J+1)/2] = [tmp, canvas.height/2*J];
							}
						}
						console.log(drawPoints);
						ctx.beginPath();
						ctx.moveTo((drawPoints[0][0]),(drawPoints[0][1]));
						ctx.lineTo((drawPoints[1][0]),(drawPoints[1][1]));
						ctx.stroke();
					}
				}*/
			}

			for(var x=5; x <= 5; x++){
				for(var y=-5; y <= 5; y++){
					var setVecs = [
							[castCoord([10,x*5,y*5]),
							castCoord([-10,x*5,y*5])],
							[castCoord([y*5,10,x*5]),
							castCoord([y*5,-10,x*5])],
							[castCoord([x*5,y*5,10]),
							castCoord([x*5,y*5,-10])]],
						setThetas = [
							Math.atan2(setVecs[0][0][1]-setVecs[0][1][1],setVecs[0][0][0]-setVecs[0][1][0]),
							Math.atan2(setVecs[1][0][1]-setVecs[1][1][1],setVecs[1][0][0]-setVecs[1][1][0]),
							Math.atan2(setVecs[2][0][1]-setVecs[2][1][1],setVecs[2][0][0]-setVecs[2][1][0])
						],
						tmp = [
							[Math.cotan(setThetas[0])*(canvas.height/2-setVecs[0][0][1])+setVecs[0][0][0],
							Math.cotan(setThetas[0])*(-canvas.height/2-setVecs[0][0][1])+setVecs[0][0][0]],
							[Math.cotan(setThetas[1])*(canvas.height/2-setVecs[1][0][1])+setVecs[1][0][0],
							Math.cotan(setThetas[1])*(-canvas.height/2-setVecs[1][0][1])+setVecs[1][0][0]],
							[Math.cotan(setThetas[2])*(canvas.height/2-setVecs[2][0][1])+setVecs[2][0][0],
							Math.cotan(setThetas[2])*(-canvas.height/2-setVecs[2][0][1])+setVecs[2][0][0]]];
					
					ctx.strokeStyle = 'rgba(0,0,0,0)';
					ctx.beginPath();
						ctx.moveTo((tmp[0][0]),(canvas.height/2));
						ctx.lineTo((tmp[0][1]),(-canvas.height/2));

						ctx.moveTo((tmp[2]),(canvas.height/2));
						ctx.lineTo((tmp[3]),(-canvas.height/2));

						ctx.moveTo((tmp[2][0]),(canvas.height/2));
						ctx.lineTo((tmp[2][1]),(-canvas.height/2));
					ctx.stroke();
				}
			}


		}

		debug.intersects = intersects;
		debug.thetas = thetas;
		var X = angle[1],
			Y = angle[0],
			Z = angle[2] || 0;

		var vp = [
			[
				Math.cos(Y)*Math.cos(Z)/(Math.sin(X)*Math.sin(Z) - Math.cos(X)*Math.cos(Z)*Math.cos(Y)),
				(Math.cos(Z)*Math.sin(X)*Math.sin(Y) - Math.cos(X)*Math.sin(Z))/(Math.sin(X)*Math.sin(Z) - Math.cos(X)*Math.cos(Z)*Math.cos(Y))
			],
			[
				-Math.cos(Y)*Math.sin(Z)/(Math.cos(Z)*Math.sin(X) + Math.cos(X)*Math.sin(Y)*Math.sin(Z)),
				(Math.cos(X)*Math.cos(Z) - Math.sin(X)*Math.sin(Y)*Math.sin(Z))/(Math.cos(Z)*Math.sin(X) + Math.cos(X)*Math.sin(Y)*Math.sin(Z))
			],
			[
				Math.tan(Y)/Math.cos(X),
				-Math.tan(X)
			]
		]
		ctx.fillStyle = 'rgb(0,0,0)';
		ctx.fillRect(canvas.width*vp[0][0]-2, canvas.width*vp[0][1]-2,4,4)
		ctx.fillRect(canvas.width*vp[1][0]-2, canvas.width*vp[1][1]-2,4,4)
		ctx.fillRect(canvas.width*vp[2][0]-2, canvas.width*vp[2][1]-2,4,4)

		for(var n = 0; n < 3; n++){
			ctx.beginPath();
			ctx.moveTo(canvas.width*vp[n][0], canvas.width*vp[n][1]);
			ctx.lineTo(vp[n][0]/vp[n][1]*(-canvas.height*Math.sign(vp[n][1])),-canvas.height*Math.sign(vp[n][1]));
			switch(n){
				case 0: 
					ctx.strokeStyle = 'rgb(255,0,0)';
					break;
				case 1: 
					ctx.strokeStyle = 'rgb(0,255,0)';
					break;
				case 2: 
					ctx.strokeStyle = 'rgb(0,0,255)';
					break;
			}
			ctx.stroke();
		}

	}
	switch(settings.color){
	  case 'gsgrad':
	    ctx.fillStyle = 'rgba(0,0,0,'+depth/10000+')';
	    break;
	  case 'gsbin':
	    ctx.fillStyle = 'rgba(0,0,0,0.5)';
	    break;
	  case 'clgrad':
	    ctx.fillStyle = 'hsla('+depth*10+', 100%, 50%, '+depth/1000+')';
	    break;
	  case 'clbin':
	    ctx.fillStyle = 'hsla('+depth*10+', 100%, 50%, 1)';
	    break;
	  case 'inverted':
	    ctx.fillStyle = 'rgba(255,255,255,'+depth/10000+')';
	    break;
	}
	//ctx.fillStyle = 'rgba(244,67,54,'+depth/1000+')';

	points.forEach(function(elm){
		
		var point = castCoord(elm);
    	if(point[2]>0){
			ctx.fillRect(point[0], point[1], size/point[2], size/point[2]);
		}

	});

	settings.maps.forEach(function(elm){
		points = points.map(maps[elm]);
	});
	
	if(settings.rotate){
	  	angle[0]+=0.01;
	  	angle[1]+=0.01;
	  	fixAngle();
	}

	depth++;

}

function unitSphere(){
  
}