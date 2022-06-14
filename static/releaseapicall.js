$("form button").on( "click" , function(e){
	e.preventDefault() ;
	$.post( "../api/lf/release" , {
		"title" : $("input[name=topic]").val() ,
		"date"  : $("input[name=time]").val()  ,
		"place" : $("input[name=place]").val() ,
		"name"  : $("input[name=item]").val()  ,
		"text"  : $("textarea").val() ,
		"pic1"  : $("input[type=file]").val()  ,
		"type"  : $("select").val() 
	} , function( data ){
		if( data.result == "success" ){
			window.navigate( `../lf/post/${data.id}` ) ;
		}
	})
})