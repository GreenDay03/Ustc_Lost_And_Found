document.write('<div class="Page Title"><ul class="directory"><li class="directory"><a href="#" class="directory"><div style="float: left;margin-top: 15px;width: auto;"><p style="width:100%;text-align: center;">USTC权益柜</p></div><img src="/static/icon.jpg" style="height: 80px;float: right;" /></a></li><li class="directory"><a href="/lf/" class="directory">寻物失物</a></li><li class="directory"><a href="/report/" class="directory">权益投诉</a></li><li class="directory"><a href="/tips/" class="directory">柜君tips</a></li><li class="directory"><a href="/qa/" class="directory">Q&A</a></li><li class="directory"><a href="/user/" class="directory">我的</a></li><li class="directory"><a class="directory" id="logout">退出登陆</a></li></ul></div>')
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