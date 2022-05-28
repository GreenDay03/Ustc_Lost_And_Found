var redata ;
var pages , currentpage = 1 ;
var writehead = 1 ;

function ShowQ( data ) {
	$(`<li class="Q&A questions" id="${data.id}">
		<a href="../lf/post/${data.id}" class="items">
		<p><input type="date" name="date" value="${data.time}" disabled/>
		${data.q}</p><p>${data.a}</p></a></li>`).appendTo('ul');
}

function ShowQAndA( showarr ) {
	if( showarr.result != "success" ){
		document.write( "<h1>出错了！请刷新试试<h1>") ;
		return ;
	}
	for( data in showarr.data ){
		if( data.top === 1 ){
			ShowQ( data ) ;
		}
	}
	for( data in showarr.data ){
		if( data.top === 0 ){
			ShowQ( data ) ;
		}
	}
}

$(document).ready(function(){
	$.get( "../api/post/list" , {
		"type": 'T' ,
		"page": 1 
	},
	function( data ){
		redata = data ;
		pages = data.total_page ;
	}) ;
	ShowQAndA( data ) ;
})