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
	$('li .questions').remove() ;
	if( showarr.result != "success" ){
		document.write( "<h1>出错了！请刷新试试<h1>") ;
		return ;
	}
	showarr.data.forEach( function( data ){
		if( data.top === 1 )
			ShowQ( data ) ;
	} ) ;
	showarr.data.forEach( function( data ){
		if( data.top === 0 )
			ShowQ( data ) ;
	} ) ;
}

function loadrsc( ) {
	$.get( "../api/post/list" , {
		"type": "T" ,
		"page": currentpage
	},
	function( data ){
		redata = data ;
		pages = data.total_page ;
		ShowQAndA( data ) ;
	}) ;
}

$(document).ready(function(){
	$("input[name=currentpage]").val(currentpage) ;
	loadrsc( ) ;
})

$(function(){
	$("input[name=turnleft]").on("click",function(e){
		e.preventDefault() ;
		if( currentpage == 1 ) ;
		else currentpage-- ;
		loadrsc( ) ;
		$("input[name=currentpage]").val(currentpage) ;
	}) ;
	$("input[name=turnright]").on("click",function(e){
		e.preventDefault() ;
		if( currentpage == pages ) ;
		else currentpage++ ;
		loadrsc( ) ;
		$("input[name=currentpage]").val(currentpage) ;
	})
})