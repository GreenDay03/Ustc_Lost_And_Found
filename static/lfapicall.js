var pagenum = 1 ;
var blogs = [] ;
var redata ;

function showblogs( blogsarr ) {
	let l = blogsarr.length ;
	for( let i = 0 ; i < l ; i++ ){
		document.getElementsById('item'+i).innerHTML = 
		`<p>${blogsarr[i]['title']}</p><p>${blogsarr[i]['date_old']}-${blogsarr[i]['date_new']}</p><div style="margin-right:10px;display:inline-block">${blogsarr[i]['place']}</div><div>${blogsarr[i]['name']}</div>` ;
	}
}
$(function () {
	$("form").on("submit",function (e) {
		e.preventDefault();
		let type = $("input[name=type]").val() ;
		let titlev = $("input[name=title]").val() ;
		let dateoldv = $("input[name=date_old]").val();
		let datenewv = $("input[name=date_new]").val();
		let placev = $("input[name=place").val() ;
		let namev = $("input[name=name]").val() ;
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
			redata = data ;
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


