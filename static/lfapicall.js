var pagenum = 1 ;
var blogs = [] ;
var redata ;

function delete_post(id) {
	$.post("../api/lf/delete", {"id": id}, 
		function( data ){
			if( data.result != "success") {
				alert('删除失败！' + data.msg);
			} else {
				alert('删除成功');
			}
		})
}

function showblogs( blogsarr ) {
	$('ul[class=items]').children().remove()
	let len = blogsarr.length ;
	for( let i = 0 ; i < len ; i++ ) {
		$(`<li class="items">
			<a class="items" id="item${i}" href="${blogsarr[i]['id']}">
				<div class="half"><font color="red" size="8"> ${blogsarr[i]['title']} </font>
				<p> <font color="blue" size="5"> 日期 </font>：<input type="date" value="${blogsarr[i]['date']}" disabled/></p>
				<p> <font color="blue" size="5"> 地点 </font>：${blogsarr[i]['place']}</p>
				<div> <font color="blue" size="5"> 物品 </font>：${blogsarr[i]['name']}</div>
				<div><p> <font color="blue" size="5"> 细节 </font>：${blogsarr[i]['text']}</p></div></div>
				<div class="half">
					${ function( imgrcs ){
						let imgstr = '' ;
						imgrcs.forEach( function( imgrc ){
							if( !imgrc )
								return ;
							else imgstr += `<img src="/media/${imgrc}" width=150 height=150/>` ;
						} );
						return imgstr ;
					}( [blogsarr[i]['pic1'] , blogsarr[i]['pic2'] , blogsarr[i]['pic3']] ) }
				</div>
			</a>
			<div>
				<a href="/user/${blogsarr[i]['author']}" style="float:left;"> 作者信息 </a>
				${
					blogsarr[i]["can_delete"] == "1" ? 
					"<button type='button' onclick='delete_post(" + blogsarr[i]['id'] +  ")' style='float:right;'> 点我删除 </button>" : ""
				}
			</div>
			</li>
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
