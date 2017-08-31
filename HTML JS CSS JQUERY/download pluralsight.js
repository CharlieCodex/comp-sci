var vid = document.getElementsByTagName('video')[0];
var a = document.createElement('a');
a.setAttribute('download','pluralsight-linux-install');
a.setAttribute('href', vid.src);
a.click();