var CTRL = 0;
var u=.2,
    U=1;

if(!maps)var maps = {};
$.extend(maps, {
  secure_cube: function(pt){
    return [
      Math.sin(pt[0]*100+pt[1])+1,
      Math.cos(pt[1]*100+pt[2]+1),
      Math.cos(pt[2]*100+pt[0])-1
    ];
  },
  testermode: function(pt){
    return [
      10*Math.sin(pt[0]*100*pt[1]-1),
      Math.cos(pt[1]*100+pt[2]+1),
      Math.cos(pt[2]*100/pt[0])
    ];
  },
  maperino: function(point){
    var x = point[0],
        y = point[1],
        z = point[2],
        t = Math.atan2(y,x);
    return [
      Math.sin(t-z*x),
      Math.sin(t+z*y),
      Math.sin(t+z)
    ];
  },
  cplxQuad: function(point){
    return [
      Math.pow(point[0],2)-Math.pow(point[1],2)+point[2],
      2*point[0]*point[1],
      point[2]
    ];
  },
  mcvicker: function (pt){
    var x = pt[0],
        y = pt[1],
        z = pt[2]
        a = 1.1,
        b = z,
        c = 1;
    return [
      y*x+Math.exp(c*Math.sin(y-b))+Math.exp(c*Math.sin(b-y)),
      a*Math.sin(x),
      a*Math.cos(x)
    ];
  },
  reciprocalDifference: function(point){
    point[0] = point[0]-1/point[0];
    point[1] = point[1]-1/point[1];
    point[2] = point[2]-1/point[2];
    return point;
  },
  rotation: function(point){
    var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
    var rot = Math.atan2(point[1],point[0])+.1;
    point[0] = Math.cos(rot)*r;
    point[1] = Math.sin(rot)*r;
    return point;
  },
  stahler: function(point){
    var x = point[0],
        y = point[1],
        z = point[2];
    return [
      x+z/y,
      Math.atan2(y,x),
      Math.sin(Math.tan(x))+Math.cos(Math.tan(y))
    ]
  },
  dennan: function(point){
    var x = point[0],
        y = point[1],
        z = point[2];
    return [
        y*z-Math.pow(x,2),
        1-(Math.cos(Math.PI*Math.sin(Math.PI*x))/(1+Math.exp(-x))),
        z
      ];
  },
  static: function(point){
    return point;
  },
  asjkf: function(point){
    point[0]=1-1/point[1];
    point[1]=1-1/point[2];
    point[2]=1-1/point[0];
    return point;
  },
  pulse1: function(point){
    var theta = Math.atan2(point[1], point[0]) + 0.1;
    point[0] = Math.cos(theta);
    point[1] = Math.sin(theta);
    
    theta = Math.atan2(point[2], point[1]);
    point[2] = Math.cos(theta);
    
    return point;
  },
  pulse2: function(point){
    var theta = Math.atan2(point[1], point[0]);
    theta+=Math.PI/12;
    point[0] = Math.cos(theta);
    point[1] = Math.sin(theta);
    
    theta = Math.atan2(point[2], point[1]);
    point[2] = Math.cos(theta);
    
    return point;
  },
  pulse3: function(point){
    var theta = Math.atan2(point[1], point[0]);
    theta+=Math.PI*Math.abs(Math.sin(depth/100));
    point[0] = Math.cos(theta);
    point[1] = Math.sin(theta);
    
    theta = Math.atan2(point[2], point[1]);
    point[2] = Math.cos(theta);
    
    return point;
  },
  pulse4: function(point){

    var theta = Math.atan2(point[1], point[0]);
    var tmp = point.slice();

    theta += Math.PI*(Math.abs(Math.sin(depth/100))+1/8);
    tmp[0] = Math.cos(theta);
    tmp[1] = Math.sin(theta);
    
    theta = Math.atan2(point[2], point[1]);

    theta += Math.PI*(Math.abs(Math.sin(depth/100))+1/8);
    tmp[2] = Math.cos(theta);
    
    return tmp;

  },
  pulse5: function(point){

    var theta = Math.atan2(point[1], point[0]);
    var tmp = point.slice();

    theta += Math.PI*(Math.abs(Math.cos(depth/100))+1/3);
    tmp[0] = Math.cos(theta);
    tmp[1] = Math.sin(theta);
    
    theta = Math.atan2(point[2], point[1]);

    theta += Math.PI*(Math.abs(Math.sin(depth/100))+1/4);
    tmp[2] = Math.cos(theta);
    
    return tmp;

  },
  simple: function(point){
    point[2] = Math.pow(point[0],2) - Math.pow([1],2)
    return point;
  },
  test_3d: function(point){

    var theta = Math.atan2(point[1], point[0]);
    point[0] = Math.cos(theta);
    point[1] = Math.sin(theta);
    
    point[2] = (point[0]>0)?point[0]:0;
    
    return point;

  },
  roots: function(point){
    
    point[0] = Math.sqrt(Math.pow(point[1],2)+Math.pow(point[2],2));
    point[1] = Math.sqrt(Math.pow(point[2],2)+Math.pow(point[0],2));
    point[2] = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
    
    return point;
    
  },
  woop: function(point){
    
    point[0] = Math.sqrt(Math.pow(point[1],2)+Math.pow(point[2],2));
    point[1] = Math.sqrt(Math.pow(point[2],2)+Math.pow(point[0],2));
    point[2] = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
    
    return point;
    
  },
  meme: function(point){
    
    point[0] -= Math.sin(point[1]);
    point[1] -= Math.sin(point[2]);
    point[2] -= Math.sin(point[0]);
    
    return point;
  },
  memechose: function(point){
    var tmp = point.slice();

    tmp[0] -= Math.sin(point[1]);
    tmp[1] -= Math.sin(point[2]);
    tmp[2] += Math.sin(point[0]);
    
    return tmp;
  },
  memechose2: function(point){
    var tmp = point.slice();
    tmp[0] -= Math.sin(point[1]+.1);
    tmp[1] -= Math.sin(point[2]+.1);
    tmp[2] += Math.sin(point[0]+.1);
    
    return tmp;
  },
  testerino: function(point){

    var tmp = [];

    point = maps.unitSphere(point);

    tmp[0] += Math.cos(point[1]);
    tmp[1] += Math.cos(point[2]);
    tmp[2] += Math.cos(point[0]);
    
    return tmp;
  },
  circle: function(point){
    var theta = Math.atan2(point[1], point[0]) + 0.1;
    point[0] = Math.cos(theta);
    point[1] = Math.sin(theta);
    
    point[2] = 0;
    
    return point;
  },
  quadratic: function(point){
    
    var quads = function(point) {
  		return [
  			Math.pow(point[0],2) - Math.pow(point[1],2) + Number(params['quads.a']),
  			2*point[0]*point[1] + Number(params['quads.b'])
  		];
	  };
	  
	  var tmp = [point[0], point[1]];
	  
	  tmp = quads(tmp);
	  
	  point[0] = tmp[0];
	  
	  point[1] = tmp[1];
	  
	  tmp = [point[1], point[2]];
	  
	  tmp = quads(tmp);
	  
	  point[1] = tmp[0];
	  
	  point[2] = tmp[1];
	  
	  tmp = [point[2], point[0]];
	  
	  tmp = quads(tmp);
	  
	  point[2] = tmp[0];
	  
	  point[0] = tmp[1];
	  
    return point;
  },
  crayZ: function(point) {
    point[2] = point[1]*point[0]
    return point;
  },
  lorenz: function(point) {
    
    var tmp = point.slice();
    console.log(tmp);
    tmp[0] = Number(params['lorenz.sigma'])*(point[0]*point[1]-Math.pow(point[0],2)/2);
    tmp[1] = point[0]*point[1]*(Number(params['lorenz.r'])-point[2])-Math.pow(point[1],2)/2;
    tmp[2] = point[0]*point[1]*point[2]-(Number(params['lorenz.b'])*Math.pow(point[2],2)/2);
    
    return tmp;
  },
  plane: function(point) {

    var theta = Math.atan2(point[1], point[0]);

    theta = (theta/Math.cos(theta))/Math.sin(theta)%theta || 0;
    
    var tmp = point.slice();
    
    tmp[2] = point[0] * Math.cos(theta) + point[1] * Math.sin(theta)

    return tmp;
  },
  unitSphere: function(point) {

    //treat point as vector and then normalize
    var tmp = point.slice();
    //euclian normalization / length of vector
    var r = distance(point, [0,0,0])
    //divide each chord by the norm (the norm now becomes one)
    for (var i = tmp.length - 1; i >= 0; i--) {
      tmp[i] /= r;
    }

    return tmp;
  },
  unitSphere2: function(point) {

    var theta1 = Math.atan2(point[1], point[0]);
    var theta2 = Math.atan2(point[2], point[1]);

    theta1 += Math.log(Math.abs(theta2))

    var tmp = point.slice();

    var r1 = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2))
    var r2 = Math.sqrt(Math.pow(point[2],2)+Math.pow(point[1],2))

    tmp[0] = r1*Math.cos(theta1);
    tmp[1] = r1*Math.sin(theta1);
    tmp[2] = r2*Math.sin(theta2*theta1);

    return tmp;
  },
  plane2: function(point) {

    var theta = Math.atan2(point[1], point[0]);

    var tmp = point.slice();

    theta *= Math.log(theta+Math.PI);

    tmp[2] = Math.cos(theta) + Math.sin(theta)

    return tmp;
  },
  completenonesenseREALX: function(point){
    var tmp = point.slice();
    var x = point[0];
    var r = Math.pow(x,-x) * Math.exp(-x);
    var theta = -Math.PI * x;

    tmp[1] = r*Math.cos(theta);
    tmp[2] = r*Math.sin(theta);

    return tmp;
  },
  completenonesenseCOMPLEX: function(point){
    var tmp = point.slice();
    var A = point[0];
    var B = depth/100
    var argZ = Math.atan2(B,A);
    var lenZ = Math.sqrt(Math.pow(A,2)+Math.pow(B,2));
    var theta = -Math.PI * A + (-B*argZ);
    //r = ( e^-πB ) (|Z|^-Z) (e^-A arg Z)
    //( e^-πB ) * e^(-A arg Z)
    var r = Math.exp(-Math.PI*B + -A*argZ);
    //we have to split the rotation happening in |Z|^Z
    //so here we only account for the radius (|Z|^-A)
    //as (|Z|^-Bi) will define a sin/cos pair
    r *= Math.pow(lenZ,-A)
    //here is the sin/cos pair being integrated
    theta += -Math.log(lenZ)*B

    tmp[1] = r*Math.cos(theta)*200;
    tmp[2] = r*Math.sin(theta)*200;

    return tmp;
  },
  zach: function(point){
    var tmp = [
      1+point[1]-point[2]*Math.pow(point[0],2),
      -1*point[0],
      point[2]
      ];
    return tmp;
  },
  henon3d: function(point){
    var tmp = [
        1+point[1]-point[2]*Math.pow(point[0],2),
        -1*point[0],
        point[2]
      ];
    return tmp;
  },
  moreSines3d: function(point) {

    return [
      (point[0]-1/point[0]+point[2])*Math.pow(Math.sin(Math.atan(point[0]/point[1])),2),
      (point[1]-1/point[1])*Math.pow(Math.cos(Math.atan(point[1]/point[0])),Math.abs(1-point[0]/point[1])),
      point[2]
    ]
  },
  hjsdghjk: function(point){
    var theta1 = Math.atan2(point[1],point[0]);

    return [
      Math.cos(theta1)*Math.abs(point[2]),
      Math.sin(theta1)*Math.abs(point[2]),
      point[2]+1/point[0]+1/point[1]
    ]
  },
  expandLinear: function(point){
    var tmp = point.slice(0);

    tmp[0]+=.1*point[0]/Math.abs(point[0]);
    tmp[1]+=.1*point[1]/Math.abs(point[1]);
    tmp[2]+=.1*point[2]/Math.abs(point[2]);

    return tmp;
  },
  ikedaUVarient: function(point) {
    var t = 0.4 - 6 / (1 + Math.pow(point[0],2) + Math.pow(point[1],2));
    return [
      1+point[2]*(point[0]*Math.cos(t)-point[1]*Math.sin(t)),
      point[2]*(point[0]*Math.sin(t)+point[1]*Math.cos(t)),
      point[2]
    ];
  },
  ikedaMcvicker: function(point) {
    var t = .4 - 6 / (1 + Math.pow(point[0],2) + Math.pow(point[1],2) + Math.pow(point[2],2));
    return [
      1+U*(point[0]*Math.cos(t)-point[1]*Math.sin(t)),
      U*(point[2]*Math.sin(t)+point[1]*Math.cos(t)),
      1-U*(point[1]*Math.sin(t)- point[2]*Math.cos(t))
    ];
  },
  ikedaMcvickerN: function(point) {
    var t = .4 - 6 / (1 + Math.pow(point[0],2) + Math.pow(point[1],2) + Math.pow(point[2],2));
    return [
      1+U*(point[0]*Math.cos(t)-point[1]*Math.sin(t)),
      U*(point[2]*Math.sin(t)+point[1]*Math.cos(t)),
      U*(point[0]*Math.sin(t)-point[2]*Math.cos(t))-1
    ];
  },
  ikedaMcvicker2: function(point) {
    var t = 1 - 6 / (1 + Math.pow(point[0],2) + Math.pow(point[1],2) + Math.pow(point[2],2));
    return [
      1+u*(point[0]*Math.cos(t)-point[1]*Math.sin(t)),
      u*(point[1]*Math.cos(t)+point[2]*Math.sin(t)),
      u*(point[2]*Math.cos(t)-point[0]*Math.sin(t))-1
    ];
  },
  ikedaVector: function(point) {
    var t = .4 - 6 / (1 + Math.pow(point[0],2) + Math.pow(point[1],2)),
        tmp = [
          1+(point[0]*Math.cos(t)-point[1]*Math.sin(t)),
          (point[1]*Math.cos(t)+point[0]*Math.sin(t))
        ],
        vec = [tmp[0]-point[0],tmp[1]-point[1]],
        magDif = Math.sqrt(Math.pow(vec[0],2)+Math.pow(vec[1],2));
    return [
      point[0],
      point[1],
      magDif
    ]
  },
  ikedaVector2: function(point) {
    var t = .4 - 6 / (1 + Math.pow(point[0],2) + Math.pow(point[1],2)),
        tmp = [
          1+(point[0]*Math.cos(t)-point[1]*Math.sin(t)),
          (point[1]*Math.cos(t)+point[0]*Math.sin(t))
        ],
        mag = Math.sqrt(Math.pow(tmp[0],2)+Math.pow(tmp[1],2))/Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
    return [
      point[0],
      point[1],
      mag
    ]
  },
  ikedaChange: function(point) {
    var t = 0.4 - 6 / (1 + Math.pow(point[0],2) + Math.pow(point[1],2));
    return [
      1+.7*(point[0]*Math.cos(t)-point[1]*Math.sin(t)),
      .7*(point[0]*Math.sin(t)+point[1]*Math.cos(t)),
      point[2]+.001
    ];
  },
  tinker: function(point) {
    var x = point[0],
        y = point[1],
        z = point[2],
        a = .9,
        b = -.6013,
        c = 2,
        d = .5;

    return [
      Math.pow(x,2)-Math.pow(z,2)+a*x+b*z,
      Math.pow(x,2)-Math.pow(y,2),
      2*x*z+c*x+d*z
    ];
  }
});

//