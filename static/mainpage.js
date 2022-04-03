var div = 1 ;
var ul = 2 ;
var li = 5 ;
var a = 1 ;
var p = 2 ;
for( var divc = 0 ; divc < div ; divc++ ){
	document.write("<div class=\"items\">") ;
	for( var ulc = 0 ; ulc < ul ; ulc++ ){
		document.write("<ul class=\"items\">") ;
		for( var lic = 0 ; lic < li ; lic++ ){
			document.write("<li class=\"items\">") ;
			for( var ac = 0 ; ac < a ; ac++ ){
				document.write("<a class=\"items\" id=\"item${ac}\">") ;
				document.write("<p class=\"half\">这里放文字</p><p class=\"half\">这里放图片</p>") ;
				document.write("</a>") ;
			}
			document.write("</li>") ;
		}
		document.write("</ul>") ;
	}
	document.write("</div>") ;
}