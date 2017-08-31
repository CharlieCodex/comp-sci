if(!maps)var maps = {};
$.extend(maps, {
	absRoots: function(point) {
		return [
			Math.pow(Math.abs(point[0]), 1-1/Math.abs(point[0]))*(point[0]/Math.abs(point[0])- 1/point[1]),
			Math.pow(Math.abs(point[1]), 1-1/Math.abs(point[0]))*(point[1]/Math.abs(point[1])- 1/point[0])
		];
	},
	rootFun: function(point) {
		return [
			(1/point[1]-Math.sqrt(Math.abs(point[0]))*point[1]/Math.abs(point[0]))*(point[0]/point[1]),
			(1/point[0]-Math.sqrt(Math.abs(point[1]))*point[0]/Math.abs(point[1]))*(point[0]/point[1])
		]
	},
	sines: function(point) {
		return [
			(point[0]-1/point[0])*Math.pow(Math.sin(Math.atan(point[0]/point[1])),2),
			//(point[1]-1/point[1])*Math.pow(Math.cos(Math.atan(point[1]/point[0])),1/2)
			(point[1]-1/point[1])*Math.pow(Math.cos(Math.atan(point[1]/point[0])),Math.abs(1-point[0]/point[1]))
		]
	},
	dynamicSines: function(point) {
		return [
			(point[0]-1/point[0])*Math.pow(Math.sin(Math.atan(point[0]/point[1])),params['dynamicSines.a']),
			//(point[1]-1/point[1])*Math.pow(Math.cos(Math.atan(point[1]/point[0])),1/2)
			(point[1]-1/point[1])*Math.pow(Math.cos(Math.atan(point[1]/point[0])),params['dynamicSines.b'])
		]
	},
	moreSines: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		var theta = Math.atan2(point[0], point[1]);
		theta -= theta/r;
		return [
			r*Math.sin(theta),

			r*Math.cos(theta)
		]
	},
	twist: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		var theta = Math.atan2(point[0], point[1]);
		return [
			//x
			(r*(Math.sin(theta+.01))),
			//y
			(r*(Math.cos(theta+.01)))
		]
	},
	spiral: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		var theta = Math.atan2(point[0], point[1]);
		r+=Math.sin(theta);
		return [
			//x
			((1-1/r)*(r-1/r)*(Math.sin(theta+.01))),
			//y
			((1-1/r)*(r-1/r)*(Math.cos(theta+.01)))
		]
	},
	spiral2: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		var theta = Math.atan2(point[0], point[1]);
		theta*=Math.log(theta);
		return [
			//x
			(r*(Math.cos(theta))),
			//y
			(r*(Math.sin(theta)))
		]
	},
	wak: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		var theta = Math.atan2(point[0], point[1]);
		r+=Math.sin(theta);
		return [
			//x
			((1-1/r)*(r+1/r)*(Math.cos(theta))),
			//y
			((1+1/r)*(r-1/r)*(Math.sin(-theta)))
		]
	},
	wikk: function(point) {
		var r = Math.sqrt(Math.pow(point[0],2)+Math.pow(point[1],2));
		var theta = Math.atan2(point[0], point[1]);
		r+=Math.sqrt(r)*Math.sin(theta);
		return [
			//x
			((r+1/r)*(Math.cos(theta))),
			//y
			((r-1/r)*(Math.sin(theta)))
		]
	},
	meme: function(point) {
		return [
			//x
			(point[0]+1/point[1]),
			//y
			(point[1]-1/point[0])
		]
	}
});
