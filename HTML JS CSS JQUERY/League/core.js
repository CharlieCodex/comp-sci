var champions;
var search;
var complete = false;
var activeChamps = [];
var allChamps = [];
Array.prototype.clean = function(deleteValue) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] == deleteValue) {         
      this.splice(i, 1);
      i--;
    }
  }
  return this;
};
jQuery.getJSON("http://ddragon.leagueoflegends.com/cdn/6.3.1/data/en_US/champion.json", 
		{}, 
		function(json, textStatus) {
			champions = json.data;
			if(complete){
				initChamps();
			}else{c
				complete = true;
			}	
		}
)
jQuery(document).ready(function($) {

	search = $('#search');
	search.on('input',function(e) {
		if(search.val()==''){
			for (var i = 0; i < allChamps.length; i++) {
				$('#'+allChamps[i]).show();
				activeChamps[i] = allChamps[i];
			};
			return;
		}
		if(activeChamps.length>0){
			var text = search.val().toLowerCase();
			for (var i = 0; i < activeChamps.length; i++) {
				if(activeChamps[i].indexOf(text) == -1){
					$('#'+activeChamps[i]).hide();
					console.log(activeChamps[i]);
					activeChamps[i]=null;
				}
			};
			activeChamps.clean(null)
		}else{
			search.val('');
			for (var i = 0; i < allChamps.length; i++) {
				$('#'+allChamps[i]).show();
				activeChamps[i] = allChamps[i];
			};
		}
	});

	if(complete){
		initChamps();
	}else{
		complete = true;
	}
});
var debug;
function initChamps () {
	var div = $('#champions');
	var proto = $('#prototype');
	for (var champ in champions) {
		var e = proto.clone();
		e.children()[0].href+=champ;
		e.children()[0].children[0].src = 'http://ddragon.leagueoflegends.com/cdn/6.3.1/img/champion/'+champ+'.png'
		e.children()[1].innerText = champ;
		e.children()[0].onclick = function(event){
			window.setTimeout(
			loadMoreInfo,10);
		}
		e[0].setAttribute('id', champ.toLowerCase());
		div.append(e);
		allChamps[allChamps.length] = champ.toLowerCase();
		activeChamps[activeChamps.length] = champ.toLowerCase();

	}
	proto.hide();
}
function loadMoreInfo(){
	var champ = window.location.hash.substr(1);
	$('.padding').hide();
	$('.info').show();
	$('.wrapper').css('width', '33%');
	$('#champions').css('width', '100%');
	$('#name').text(champ);
	var info = champions[champ].blurb;
	console.log(info);
	$('#infop').text(info);
}
function closeMoreInfo(){
	$('.padding').show();
	$('.info').hide();
	$('.wrapper').css('width', '100%');
	$('#champions').css('width', '33%');
}