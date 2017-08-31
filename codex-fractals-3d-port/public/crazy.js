
if(!maps)var maps = {};
$.extend(maps, {
	cplxQuad: function(point) {
		//f(z)=z^2+c
		return [
			Math.pow(point[0],2) - Math.pow(point[1],2) + Number(params['quads.a']),
			2*point[0]*point[1] + Number(params['quads.b'])
		];
	},
	quads: function(point) {
		//f(z)=x^2+y^2+c
		return [
			Math.pow(point[0],3) + Number(params['quads.a']),
			Math.pow(point[1],3) + Number(params['quads.b'])
		];
	},
	invCos: function(point) {
		return [
			Math.cos(Math.PI*point[1]),
			Math.sin(Math.PI/point[0])
		]
	},
	henon: function(point) {
		return [
			1+point[1]-params['henon.a']*Math.pow(point[0],2),
			params['henon.b']*point[0]
		];

	},
	scramble: function(point) {
		return [
			-point[1],
			-point[0]
		];

	},
	woop: function(point) {
		return [
			point[0]+1/point[1],
			point[1]+1/point[0]
		];

	},
	crazy: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		var theta = Math.atan2(point[0], point[1]);
		return [
			(r-r/4)*Math.cos(theta*1.1), (r+r/4)*Math.sin(theta/1.1)
		];
	},
	moop: function(point) {
	  var c = 1 - 1/point[0];
		return [
		  c*point[0], point[1]/Math.abs(point[1])*Math.sqrt(Math.pow(point[1],2)+Math.pow(point[0],2)*(1-c))
		];
	},
	ring: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		return [
		  r*Math.sin(Math.pow(r,2)),
		  r*(1-Math.cos(Math.pow(r,2))) * (Math.abs(point[1])/point[1])
		];
	}
});
