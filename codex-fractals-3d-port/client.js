// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

var canvas, ctx, size;

$(function() {
  
  canvas = $('canvas');
  
  ctx = canvas[0].getContext('2d');
  
  size = ctx.canvas.height*.8;
  
  //center and flip y axis
  ctx.translate(ctx.canvas.width/2,ctx.canvas.height/2);
  //ctx.scale(0,-1);
  
  ctx.clear = function(){
    var tmp = ctx.fillStyle;
    ctx.fillStyle = 'white'
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = tmp;
    return this;
  }
  
  ctx.axis = function(){
    ctx.fillRect(-ctx.lineWidth/2,0,ctx.lineWidth,ctx.canvas.height);
    ctx.fillRect(0,-ctx.lineWidth,ctx.canvas.width,ctx.lineWidth);
    return this;
  };
  
  ctx.bounds = function(){
    ctx.beginPath();
    ctx.arc(0,0,size/2,0,7);
    ctx.stroke();
    return this;
  };
  
  //create our poincaré disk
  /*
  DOES NOT RETURN CONTEXT
  */
  ctx.hcoord = function(Z){
    
    var magZ = this.dist(Z,[0,0]);
    console.log(magZ);
    return [Z[0]/(magZ+1)*(size/2),Z[1]/(magZ+1)*(size/2)];
  }
  //normalizes a point
  ctx.norm = function(x,y){
    var Z = (y)?[x,y]:x;
    
    //if y is undefined x is a point [x,y]
    var magZ = this.dist(Z,[0,0]);
    
    return [Z[0]/(magZ)*(size/2),Z[1]/(magZ)*(size/2)];
  }
  
  ctx.dist = function(Z1,Z2){
    return Math.sqrt(Math.pow(Z1[0]-Z2[0],2)+Math.pow(Z1[1]-Z2[1],2));
  }
  //construct hyperbolic line 'l' where [x, y belong to l]
  ctx.hline = function(Z1,Z2,rad){
    Z1 = this.hcoord(Z1);
    Z2 = this.hcoord(Z2);
    //average the angles
    var argZ1 = Math.atan2(Z1[1],Z1[0]),
        argZ2 = Math.atan2(Z2[1],Z2[0]),
        arg = (argZ1+argZ2)/2;
    console.log('arg: '+arg);
    //find a circle that will work
    var r = size*rad;
    var O = [Math.cos(arg)*r,Math.sin(arg)*r];
    console.log('O: '+O);
    r = this.dist(O,Z1)
    console.log(Z1)
    
    ctx.beginPath();
    
    ctx.arc(O[0],O[1],r,argZ2,argZ1);
    
    ctx.stroke();
    
    return this;
  }
  
  ctx.hpoint = function(Z){
    
    Z=this.hcoord(Z);
    
    ctx.fillRect(Z[0]-2,Z[1]-2,4,4);
    
    return this;
  }

});
