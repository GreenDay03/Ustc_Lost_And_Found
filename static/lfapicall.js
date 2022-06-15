var pagenum = 1 ;
var blogs = [] ;
var redata ;

function showblogs( blogsarr ) {
	let len = blogsarr.length ;
	for( let i = 0 ; i < len ; i++ ) {
		$(`<li class="items">
			<a class="items" id="item${i}" href="${blogsarr[i]['id']}">
				<div class="half">${blogsarr[i]['title']}
				<p><input type="date" value="${blogsarr[i]['date']}" disabled/></p>
				<p>${blogsarr[i]['place']}</p>
				<div>${blogsarr[i]['name']}</div>
				<div><p>${blogsarr[i]['text']}</p></div></div>
				<div class="half">
					${ function( imgrcs ){
						let imgstr = '' ;
						imgrcs.forEach( function( imgrc ){
							if( imgrc === undefined )
								return ;
							else imgstr += `<img src="/media/${imgrc}"/>` ;
						} );
						return imgstr ;
					}( blogsarr[i]['pic1'] , blogsarr[i]['pic2'] , blogsarr[i]['pic3'] ) ; }
				</div>
			</a></li>
			`).appendTo( 'ul[class=items]' ) ;
	}
}

$(function () {
	$("form").on("submit",function (e) {
		e.preventDefault() ;
		$( 'ul[class=items] a.items' ).remove( ) ;
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
			blogs = [] ;
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
