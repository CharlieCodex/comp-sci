var table;
jQuery(document).ready(function($) {
	table = $('#tbp');
	for(var y = 0; y < 20; y++){

		var row = $(document.createElement('div')).attr('class','row');

		for (var x = 0; x < 10; x++) {
			
			var cell = $(document.createElement('div')).attr('class','detail');
			var img = Math.round(Math.random()*6);
			var imgloc;

			switch(img){
				case 0: imgloc = 'background: url(arc.png)'; break;
				case 1: imgloc = 'background: url(fourarc.png)'; break;
				case 2: imgloc = 'background: url(ring.png)'; break;
				case 3: imgloc = 'background: url(twoarc.png)'; break;
				default: imgloc = 'background: url()'; break;
			}

			cell.attr('style',imgloc);
			row.append(cell);
		};

		table.append(row);
	}
	$('.detail').click(function(event){
		var obj = $(event.target);
		var angle = obj.getRotateAngle();
		obj.rotate({animateTo:angle[0]==undefined?90:Math.round(angle[0]/90)*90 + 90});
	})	
});