var pagenum = 1 ;
var blogs = [] ;
var redata ;

// function showblogs( blogsarr ) {
// 	let l = blogsarr.length ;
// 	for( let i = 0 ; i < l ; i++ ){
// 		// document.getElementsById('item'+i).innerHTML = 
// 		// `<p>${blogsarr[i]['title']}</p><p>${blogsarr[i]['date_old']}-${blogsarr[i]['date_new']}</p><div style="margin-right:10px;display:inline-block">${blogsarr[i]['place']}</div><div>${blogsarr[i]['name']}</div>` ;
// 		$(`#item${i}`).html(`<p>${blogsarr[i]['title']}</p><p>${blogsarr[i]['date_old']}-${blogsarr[i]['date_new']}</p><div style="margin-right:10px;display:inline-block">${blogsarr[i]['place']}</div><div>${blogsarr[i]['name']}</div>`) ;
// 		$(`#item${i}`).attr( 'href' , `/${blogsarr[i]['id']}`) ;
// 	}
// }

function showblogs( blogsarr ) {
	let len = blogsarr.length ;
	for( let i = 0 ; i < len ; i++ ) {
		$(`
			<a class="items" id="item${i}" href="${blogsarr[i]['id']}]">
				<div class="half">${blogsarr[i]['title']}
				<p><input type="date" value="${blogsarr[i]['date']}"/></p>
				<p>${blogsarr[i]['place']}</p>
				<div>${blogsarr[i]['name']}</div>
				<div><p>${blogsarr[i]['text']}</p></div></div>
			</a>
			`).appendTo( 'ul[class=items]' ) ;
	}
}

$(function () {
	$("form").on("submit",function (e) {
		e.preventDefault();
		let type 	= function( data ){
			if( data === undefined )
				return 'L' ;
			return data ;
		}($("input[name=type]:checked").val()) ;
		let titlev 	= $("input[name=title]").val() ;
		let dateoldv= $("input[name=date_old]").val();
		let datenewv= $("input[name=date_new]").val();
		let placev 	= $("input[name=place").val() ;
		let namev 	= $("input[name=name]").val() ;
		$.get( "../api/lf/list" , {
			"title" : titlev ,
			"date_old" : dateoldv ,
			"date_new" : datenewv ,
			"place" : placev ,
			"name" : namev ,
			"page" : pagenum ,
			"type" : type 
		}, 
		function( data ){
			if( data.result != "success")
				return ;
			for( i = 0 ; i < data.data.length ; i++ ){
				blogs.push( data.data[i] ) ;
			}
			redata = data['data'] ;
			showblogs( blogs ) ;
			//console.log(redata)
		})
	});
});


$(document).ready(function(){
	$("#logout").click(function(){
		$.ajax({
			type: "POST",
			url: "../api/auth/logout/",
			data: {},
			dataType: "JSON",
			success: function(result) {
				$(location).attr('href', '/lf/');
			},
			error: function(result) {
				alert('发生错误');
			}
		});
	});
});


