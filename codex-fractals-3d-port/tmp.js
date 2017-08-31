// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html
var ctx,
    tbl;
$(function() {

  var canvas = $('canvas');
      ctx = canvas[0].getContext('2d');
  
  ctx.clear = function(){
    var tmp = ctx.fillStyle;
    ctx.fillStyle = 'white'
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = tmp;
    return this;
  }
  
  ctx.axis = function(){
    ctx.fillRect(ctx.canvas.width/2-1,0,2,ctx.canvas.height);
    ctx.fillRect(0,ctx.canvas.height/2-1,ctx.canvas.width,2);
    return this;
  };
  
  ctx.graph = function(func, scale, detail, domain) {
    
    var table = [];
    
    if(!scale)scale = 1;
    if(!domain)domain = {min: -ctx.canvas.width/(2*scale), max:ctx.canvas.width/(2*scale)};
    if(!detail)detail = 1/scale;
    
    var started = false;
    
    for(var x = domain.min; x < domain.max; x += detail) {
      var realX = x * scale + ctx.canvas.width/2,
          y = func(x),
          realY = - ( y * scale ) + ctx.canvas.height/2;
      
      table.push([x, y]);
      if(isFinite(realY)) {
        if(!started) {
          console.log('New Path')
          ctx.beginPath();
          ctx.moveTo(realX, realY);
          started = true;
        } else {
          ctx.lineTo(realX, realY);
          ctx.fillRect(realX-.5, realY-.5, 1, 1)
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(realX, realY);
        }
      } else {
        console.log('Hole')
        ctx.stroke();
        started = false;
      }
    }
    
    ctx.stroke();
  
    return this;
    
  }
  
  ctx.strokeStyle = 'black';
  
  ctx.axis();
  
  ctx.graph(function(x){return x;});
  
  ctx.cobweb = function(func, seed, scale, iterations, detail) {
    
    var values = [];
    
    if(!scale)scale = 1;
    if(!detail)detail = 1/scale;
    if(!seed)seed = 0;
    
    ctx.graph(func, scale);
    
    var x = seed;
    
    //get it started    

    var realX = x * scale + ctx.canvas.width/2,
        y = func(x),
        realY = - ( y * scale ) + ctx.canvas.height/2;
    var realXY = - (x * scale) + ctx.canvas.height/2,
        realYX = y * scale + ctx.canvas.width/2;

    ctx.beginPath();

    ctx.moveTo(realX,  ctx.canvas.height/2);
    
    ctx.lineTo(realX, realY);
      
    ctx.lineTo(realYX, realY);
    
    ctx.stroke();
    
    console.log(x, y);
    
    x = y;

    
    for(var i = 0; i < iterations; i++) {
      
      console.log(i);
      i++;
      
      realX = x * scale + ctx.canvas.width/2;
      y = func(x);
      realY = - ( y * scale ) + ctx.canvas.height/2;
      
      
      var realXY = - (x * scale) + ctx.canvas.height/2,
          realYX = y * scale + ctx.canvas.width/2;
      
      ctx.beginPath();
      
      ctx.moveTo(realX,realXY);
      
      ctx.lineTo(realX, realY);
      
      ctx.lineTo(realYX, realY);
      
      ctx.stroke();
      
      console.log(x, y);
      
      x = y;
      
    }
    
    return this;
    
  }
  
  $('<li></li>').text('sine').on('click', function(e){
    ctx.clear().axis().cobweb(sine, -3, 250, 2000)
  }).appendTo('ul.buttons');
  
  $('<li></li>').text('quad 1').on('click', function(e){
    ctx.clear().axis().cobweb(quad(1,0,-13/16), 1, 250, 2000)
  }).appendTo('ul.buttons');
  
  $('<li></li>').text('quad 2').on('click', function(e){
    ctx.clear().axis().cobweb(quad(1,0,-16/13), 1, 250, 2000)
  }).appendTo('ul.buttons');
  
});

function linear(m, b) {
  return function(x) {
    return m*x + b;
  };
}

function twoPeriod(x) {
  return Math.pow(x,2) - 13/16;
}

function sine(x) {
  return Math.sin(Math.PI * x)
}

function cos(x) {
  return Math.cos(Math.PI * x)
}

function quad(a, b, c) {
  return function(x) {
    return a*Math.pow(x,2) + b*x + c
  }
}