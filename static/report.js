var pagenum = 1 ;
var blogs = [] ;
var redata ;
var currentpage = 1 ;

function showdata( dataarr ) {
	dataarr.forEach( function( data ){
		$(`<li class="items">
			<a class="items" href="/">
				<div class="half">
					<p> <font color="red" size="8"> ${data.title} </font> </p>
					<p> <font color="blue" size="5"> 时间 </font> : <input type="datetime" value="${data.time}" disabled/></p>
					<p> <font color="blue" size="5"> 内容 </font> : ${data.text}</p>
					<p> <font color="blue" size="5"> 作者 </font> : ${data.author}</p>
				</div>
				<div class="half">
					<br/>
					<p><input type="datetime" value="${data.reply_time || "Null" }" disabled/></p>
					<p>${data.reply}</p>
				</div>
			</a>
			</li>`).appendTo( '#main' )
	} )
}

function loadrsc( order ) {
	$( "#main" ).children().remove( ) ;
	$.get( "../api/report/list", {
		"order": order ,
		"page": currentpage 
	} , function( data ){
		if( data.result != 'success' )
			return ;
		redata = data ;
		pages = data.total_page ;
		showdata( data.data ) ;
	} )
}

$(function(){
	$("input[name=turnleft]").on("click",function(e){
		e.preventDefault() ;
		if( currentpage == 1 ) ;
		else currentpage-- ;
		loadrsc( 'new' ) ;
		$("input[name=currentpage]").val(currentpage) ;
	}) ;
	$("input[name=turnright]").on("click",function(e){
		e.preventDefault() ;
		if( currentpage == pages ) ;
		else currentpage++ ;
		loadrsc( 'new' ) ;
		$("input[name=currentpage]").val(currentpage) ;
	})
})

$(document).ready( function(){
	$("input[name=currentpage]").val(currentpage) ;
	loadrsc( 'new' ) ;
} )