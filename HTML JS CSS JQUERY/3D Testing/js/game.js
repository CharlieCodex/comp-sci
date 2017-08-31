angular.module("3DRendering")
.directive('game', function(){
	// Runs during compile
	return {
		// name: '',
		// priority: 1,
		// terminal: true,
		// scope: {}, // {} = isolate, true = child, false/undefined = no change
		controller: function($scope, $element, $attrs, $transclude) {
			var ctrl = this;
			this.square = function(center,side){
				return {
					points:[
						[center[0]-side/2,center[1]-side/2,center[2]-side/2],
						[center[0]-side/2,center[1]-side/2,center[2]+side/2],
						[center[0]-side/2,center[1]+side/2,center[2]-side/2],
						[center[0]-side/2,center[1]+side/2,center[2]+side/2],
						[center[0]+side/2,center[1]-side/2,center[2]-side/2],
						[center[0]+side/2,center[1]-side/2,center[2]+side/2],
						[center[0]+side/2,center[1]+side/2,center[2]-side/2],
						[center[0]+side/2,center[1]+side/2,center[2]+side/2]
					],
					colors:[
						[0,0,0],
						[0,0,255],
						[0,255,0],
						[0,255,255],
						[255,0,0],
						[255,0,255],
						[255,255,0],
						[255,255,255]
					],
					lines:[
						[0,1],
						[0,2],
						[0,4],
						[1,3],
						[1,5],
						[2,3],
						[2,6],
						[3,7],
						[4,5],
						[4,6],
						[5,7],
						[6,7]
					]
				};
			}
			this.dodeca = function(center, side, height){
				return {
					height:height,
					points:[
						//Set 1
						[center[0],center[1]-side*(1 + height),center[2]-side*(1-Math.pow(height,2))],
						[center[0],center[1]-side*(1 + height),center[2]+side*(1-Math.pow(height,2))],
						[center[0],center[1]+side*(1 + height),center[2]-side*(1-Math.pow(height,2))],
						[center[0],center[1]+side*(1 + height),center[2]+side*(1-Math.pow(height,2))],
						//Set 2
						[center[0]-side*(1 + height),center[1]-side*(1-Math.pow(height,2)), center[2]],
						[center[0]-side*(1 + height),center[1]+side*(1-Math.pow(height,2)), center[2]],
						[center[0]+side*(1 + height),center[1]-side*(1-Math.pow(height,2)), center[2]],
						[center[0]+side*(1 + height),center[1]+side*(1-Math.pow(height,2)), center[2]],
						//Set 3
						[center[0]-side*(1-Math.pow(height,2)),center[1], center[2]-side*(1 + height)],
						[center[0]-side*(1-Math.pow(height,2)),center[1], center[2]+side*(1 + height)],
						[center[0]+side*(1-Math.pow(height,2)),center[1], center[2]-side*(1 + height)],
						[center[0]+side*(1-Math.pow(height,2)),center[1], center[2]+side*(1 + height)],
						//Cube
						[center[0]-side,center[1]-side,center[2]-side],
						[center[0]-side,center[1]-side,center[2]+side],
						[center[0]-side,center[1]+side,center[2]-side],
						[center[0]-side,center[1]+side,center[2]+side],
						[center[0]+side,center[1]-side,center[2]-side],
						[center[0]+side,center[1]-side,center[2]+side],
						[center[0]+side,center[1]+side,center[2]-side],
						[center[0]+side,center[1]+side,center[2]+side]
			
					],
					colors:[
						[127,127-64,128-127],
						[127,127-64,127+127],
						[127,127+64,127-127],
						[127,127+64,127+127],
						[127-64,128-127,127],
						[127-64,127+127,127],
						[127+64,127-127,127],
						[127+64,127+127,127],
						[128-127,127,127,127-64],
						[127+127,127,127-64],
						[127-127,127,127+64],
						[127+127,127,127+64],
						[128-64,127,127,127-127],
						[127+64,127,127-127],
						[127-64,127,127+127],
						[127+64,127,127+127],
						[255,0,0],
						[255,0,255],
						[255,255,0],
						[255,255,255]
					],
					lines:[
						[0,1],
						[2,3],
						[2,14],
						[2,18],
						[3,15],
						[5,4],
						[5,14],
						[6,7],
						[7,18],
						[8,12],
						[8,10],
						[9,11],
						[10,16],
						[10,18],
						[11,19],
						[13,9],
						[13,4],
						[13,1],
						[14,8],
						[1,17],
						[17,6],
						[17,11],
						[6,16],
						[15,9],
						[15,5],
						[16,0],
						[0,12],
						[12,4],
						[19,7],
						[19,3]
					]
				};
			}
			this.distance = function(p1,p2){
				var dists = [
					Math.abs(p1[0]-p2[0]),
					Math.abs(p1[1]-p2[1]),
					Math.abs(p1[2]-p2[2])
				]
				return Math.sqrt(
					Math.pow(dists[0],2)+
					Math.pow(dists[1],2)+
					Math.pow(dists[2],2)
				)
			};
			this.clr = function(){
				var canv = this.canvas;
				var tmp = this.ctx.fillStyle;
				this.ctx.fillStyle = '#888888';
				this.ctx.fillRect(-canv.width/2,-canv.height/2,canv.width,canv.height);
			}
			this.drawPoint = function(point, color){
				var coord = this.castCoord(point)
				this.ctx.beginPath();
				this.ctx.strokeStyle = this.parseColor(color);
				this.ctx.lineWidth = 10;
				this.ctx.arc(coord[0], coord[1], 500/coord[2], 0, 2 * Math.PI, false);
				//console.log('Rendering Point of ('+point[0]+','+point[1]+','+point[2]+') at: ('+point[0]/z+', '+point[1]/z+')');
				this.ctx.stroke();
			}
			this.castCoord = function(point){
				var z = this.distance(point,this.viewpoint.point);
				
				return [(point[0]-this.viewpoint.point[0])/z*this.canvas.width, (point[1]-this.viewpoint.point[1])/z*this.canvas.height, z];
			}
			this.rotate = function(object, amounts, options){
				//this.rotationTotals[0] += amounts[0];
				//this.rotationTotals[1] += amounts[1];
				//this.rotationTotals[2] += amounts[2];
				console.log(amounts);
				options = $.extend({centerpoint:this.viewpoint.point, override: false},options);
				var centerpoint = options.centerpoint;
				var newObject = jQuery.extend(true, {}, object);
				for (var i = 0; i < object.points.length; i++) {
					if(amounts[0]!=0){
						var point = object.points[i];
						var r = this.distance(point,[centerpoint[0],point[1],centerpoint[2]]);
						var ca = Math.acos((point[0]-centerpoint[0])/r) || 0;
						ca *= (point[2]-centerpoint[2]>0)?1:-1;
						var ra = amounts[0];
						var na = (ca-ra);
						//console.log("Radius: "+r+", Central Angle: "+ca+", Rotation Angle: "+ra+", New Angle: "+na);
						var newPoint = [
							(r*Math.cos(na))+centerpoint[0],
							point[1],
							(r*Math.sin(na))+centerpoint[2]
						]
						//console.log("NA: "+na+" CA: "+ca+", COS of NA: "+Math.cos(na)+": \n"+newPoint);
						newObject.points[i] = newPoint;
					}
					if(amounts[1]!=0){
						var point = object.points[i];
						var r = this.distance(point,[centerpoint[0],centerpoint[1],point[2]]);
						var ca = Math.acos((point[0]-centerpoint[0])/r) || 0;
						ca *= (point[1]-centerpoint[1]>0)?1:-1;
						var ra = amounts[1];
						var na = (ca-ra);
						//console.log("Radius: "+r+", Central Angle: "+ca+", Rotation Angle: "+ra+", New Angle: "+na);
						var newPoint = [
							(r*Math.cos(na))+centerpoint[0],
							(r*Math.sin(na))+centerpoint[1],
							point[2]
						]
						//console.log(ca+", "+Math.cos(na)+": "+newPoint);
						newObject.points[i] = newPoint;
					}
					if(amounts[2]!=0){
						var point = object.points[i];
						var r = this.distance(point,[point[0],centerpoint[1],centerpoint[2]]);
						var ca = Math.acos((point[1]-centerpoint[1])/r) || 0;
						ca *= (point[2]-centerpoint[2]>0)?1:-1;
						var ra = amounts[2];
						var na = (ca-ra);
						var newPoint = [
							point[0],
							(r*Math.cos(na))+centerpoint[1],
							(r*Math.sin(na))+centerpoint[2]
						]
						//console.log(ca+", "+Math.cos(na)+": "+newPoint);
						newObject.points[i] = newPoint;
					}
				};
				if(options.override){
					object = newObject;
				}
				return newObject;
			}
			this.draw = function(object){
				var obj = this.rotate(object, this.viewpoint.angle);
				var controller = this;
				if(this.showPoints){
					var tmp = obj.points.slice(0).sort(function(a, b){
						return controller.distance(b,controller.viewpoint) - controller.distance(a,controller.viewpoint)
					});
					for (var i = 0; i < tmp.length; i++) {
						this.drawPoint(tmp[i],obj.colors[obj.points.indexOf(tmp[i])]);
					};
				}
				if(obj.lines && this.showLines){
					for (var i = 0; i < obj.lines.length; i++) {

						var p1 = this.castCoord(obj.points[obj.lines[i][0]]);
						var p2 = this.castCoord(obj.points[obj.lines[i][1]]);

						var grad = this.ctx.createLinearGradient(p1[0], p1[1], p2[0], p2[1]);
						grad.addColorStop(0, this.parseColor(obj.colors[obj.lines[i][0]]));
						grad.addColorStop(1, this.parseColor(obj.colors[obj.lines[i][1]]));

						this.ctx.strokeStyle = grad;

						this.ctx.beginPath();
						this.ctx.moveTo(p1[0],p1[1]);
						this.ctx.lineTo(p2[0],p2[1]);
						this.ctx.stroke();
					};
				}
			}
			this.parseColor = function(color){
				return 'rgb('+color[0]+','+color[1]+','+color[2]+')';
			}
			this.mouseMove = function($event){
				var e = $event.originalEvent
				var movementX = e.movementX ||
				    e.mozMovementX          ||
				    0;
				var movementY = e.movementY ||
				    e.mozMovementY      	||
				    0;
				this.viewpoint.angle[1]-=movementX/200;
				this.viewpoint.angle[2]-=movementY/200;
				this.clr();
				this.draw(this.obj);

			};
			this.keyDown = function(control){
				
				this.keys[control] = true;

			};
			this.keyUp = function(control){

				this.keys[control] = false;

			}
			this.update = function(){
				//console.log(ctrl);
				for (var i = 0; i < ctrl.keys.length; i++) {
					if(ctrl.keys[i]){
						switch(i){
							case 0:
								ctrl.viewpoint.point[2] -= 0.1;
							break;
							case 1:
								ctrl.viewpoint.point[0] += 0.1;
							break;
							case 2:
								ctrl.viewpoint.point[2] += 0.1;
							break;
							case 3:
								ctrl.viewpoint.point[0] -= 0.1;
							break;
						}
					}
				}
				ctrl.clr();
				ctrl.draw(ctrl.obj);
			};
			//this.rotationTotals = [0,0,0];
			this.keys = [false, false, false, false];
			this.updateInterval = window.setInterval(this.update, 1000/60);
			this.height=0;
			this.showLines = true;
			this.showPoints = false;
			this.viewpoint = {
				point:[0,0,40],
				angle:[0,0,0]
			};
			//this.obj = this.dodeca([0,0,0],1, (Math.sqrt(5)-1)/2);
			this.obj = this.square([0,0,0], 1)
			//(Math.sqrt(5)-1)/2
			console.log(this.obj);
			for(var i = 0; i<this.obj.length; i++){
				console.log(this.distance([4,0,0],this.obj[i]));
			}
		},
		controllerAs:'vm',
		// require: 'ngModel', // Array = multiple requires, ? = optional, ^ = check parent elements
		restrict: 'A', // E = Element, A = Attribute, C = Class, M = Comment
		// template: '',
		// templateUrl: '',
		// replace: true,
		// transclude: true,
		// compile: function(tElement, tAttrs, function transclude(function(scope, cloneLinkingFn){ return function linking(scope, elm, attrs){}})),
		link: function($scope, iElm, iAttrs, controller) {


			controller.canvas = iElm.find('canvas')[0];
			controller.ctx = controller.canvas.getContext('2d');
			console.log(controller.canvas.width+', '+controller.canvas.height)
			controller.ctx.translate(controller.canvas.width/2,controller.canvas.height/2);
			controller.clr();
			controller.draw(controller.obj);

			controller.canvas.onclick = function() {
			  	controller.canvas.requestFullscreen = controller.canvas.requestFullscreen ||
			  										controller.canvas.webkitRequestFullScreen ||
			  										controller.canvas.mozRequestFullScreen;
			  	if(!document.fullscreen)controller.canvas.requestFullscreen();
			  	controller.canvas.requestPointerLock();
			}

			document.addEventListener('pointerlockchange', controller.lockChangeAlert, false);
			document.addEventListener('mozpointerlockchange', controller.lockChangeAlert, false);

			controller.lockChangeAlert = function() {
			  if(document.pointerLockElement === canvas ||
			  document.mozPointerLockElement === canvas) {
			    console.log('The pointer lock status is now locked');
			  } else {
			    console.log('The pointer lock status is now unlocked');  
			  }
			}

			iElm.parents('body').on('keydown', function(event) {
				event.preventDefault();
				if(event.keyCode == 37){
					controller.viewpoint.angle[0] -= 0.1;
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 39){
					controller.viewpoint.angle[1] -= 0.1;
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 38){
					controller.viewpoint.angle[0] += 0.1;
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 40){
					controller.viewpoint.angle[1] += 0.1;
					controller.clr();
					controller.draw(controller.obj);
				}
				//WASD
				if(event.keyCode == 87){
					controller.keyDown(0);
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 65){
					controller.keyDown(3);
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 83){
					controller.keyDown(2);
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 68){
					controller.keyDown(1);
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 67){
					controller.height = 0.01;
					controller.obj = controller.dodeca([0,0,0], 1, (Math.sqrt(5)-1)/2);
					var tmp = controller.rotationTotals.slice(0);
					controller.rotate(controller.obj,tmp);
					controller.rotationTotals = tmp;
					console.log(controller.rotationTotals);
					controller.clr();
					controller.draw(controller.obj);
				}
			});
			iElm.parents('body').on('keyup', function(event) {
				event.preventDefault();
				if(event.keyCode == 87){
					controller.keyUp(0);
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 65){
					controller.keyUp(3);
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 83){
					controller.keyUp(2);
					controller.clr();
					controller.draw(controller.obj);
				}
				if(event.keyCode == 68){
					controller.keyUp(1);
					controller.clr();
					controller.draw(controller.obj);
				}
			});
			
		}
	};
});