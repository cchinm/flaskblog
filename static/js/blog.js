
$(function() {

});
function next(page) {
    var nextPage = page+1;
    var prePage = page-1;
	$.ajax({
		type : "POST",
		url : "/get?p="+page,
		data : {
			"test":page,
		},
		success : function(jsonResult) {
			var _content="";
			var page = $("#page").html() + 1;
			if (jsonResult.length < 1){
			    nextPage = prePage+1;
			}
			if (prePage < 1) {
			    prePage = 1;
			}
			var pageNum = nextPage-1;
			for (var i=0;i<jsonResult.length;i++){
                _content += "<div class=\"post-preview\">\
                            <a href=\"./post/"+ jsonResult[i].md5_id +"\">\
                            <h2 class=\"post-title\">"+jsonResult[i].title+ "</h2>\
                    <h3 class=\"post-subtitle\">"+jsonResult[i].short_summary+"</h3></a>\
                    <p class=\"post-meta\">Posted by\
                    <a href=\"about.html\">"+jsonResult[i].post_author+"&nbsp&nbsp</a>\
            <span class=\"glyphicon glyphicon-time\">"+jsonResult[i].post_time+"&nbsp&nbsp</span>\
            <span class=\"glyphicon glyphicon-tags\">&nbsp" +jsonResult[i].tags +"&nbsp&nbsp</span>\
            <span class=\"glyphicon glyphicon-eye-open\">&nbsp"+jsonResult[i].views +"&nbsp&nbsp</span>"
            if (jsonResult[i].is_priority > 0){
                _content += " <span class=\"glyphicon glyphicon-star-empty\"></span></p></div><hr>"
            } else {
                _content += "</p></div><hr>"
            }

			}
			_content += "<div class=\"clearfix\">\
                    <a class=\"btn btn-primary float-left\" href=\"javascrpit:void(0)\" onclick=\"next("+prePage+")\">&larr; Previous Page</a>\
                     <a class=\"btn btn-primary float-middle\" href=\"#\">"+pageNum+"</a>\
           <a class=\"btn btn-primary float-right\" href=\"javascrpit:void(0)\" onclick=\"next("+nextPage+");\">Next Page &rarr;</a>\
            </div>"

			$("#blog-content").html(_content);
		}
	});
}

function search() {
    var q=document.getElementById("search-text").value
	$.ajax({
		type : "GET",
		url : "/s?q="+q,

		success : function(jsonResult) {
            var _content="";

			for (var i=0;i<jsonResult.length;i++){
			    if (jsonResult[i].id > 0){
			        href = "./post/"+ jsonResult[i].md5_id ;
			    } else {
			        href = jsonResult[i].md5_id;
			    }
                _content += "<div class=\"post-preview\">\
                            <a href=\""+ href +"\" target=\"_blank\">\
                            <h2 class=\"post-title\">"+jsonResult[i].title+ "</h2>\
                    <h3 class=\"post-subtitle\">"+jsonResult[i].short_summary+"</h3></a>\
                    <p class=\"post-meta\">Posted by\
                    <a href=\"about.html\">"+jsonResult[i].post_author+"&nbsp&nbsp</a>\
            <span class=\"glyphicon glyphicon-time\">"+jsonResult[i].post_time+"&nbsp&nbsp</span>\
            <span class=\"glyphicon glyphicon-tags\">&nbsp" +jsonResult[i].tags +"&nbsp&nbsp</span>\
            <span class=\"glyphicon glyphicon-eye-open\">&nbsp"+jsonResult[i].views +"&nbsp&nbsp</span>"

            if (jsonResult[i].is_priority > 0){
                _content += " <span class=\"glyphicon glyphicon-star-empty\"></span></p></div><hr>"
            } else {
                _content += "</p></div><hr>"
            }

			}
			

			$("#blog-content").html(_content);
		}
	});
}


function recent_post() {
	$.ajax({
		type : "POST",
		url : "/get?p=1&count=5",
		data : {
			"count":5,
			"page":-1
		},
		success : function(jsonResult) {
			var _content="";
			_content += "<ul";
			for (var i=0;i<jsonResult.length;i++){
                _content+= "<li><a href=\"/post/" +jsonResult[i].md5_id+ "\">"+jsonResult[i].short_summary+"</a></li>";
            }
            _content += "</ul>"
			$("#recent_post").html(_content);
		}
	});
}


function post_publish() {
    var content=document.getElementById("content").value
    var title=document.getElementById("title").value
	$.ajax({
		type : "POST",
		url : "/edit/publish",
		data : {
			"content":content,
			"title":title
		},
		success : function(jsonResult) {
		    if (jsonResult.code > 0)
		    {
                alert("提交成功！");
		    } else {
		        alert("提交失败！原因:"+jsonResult.msg);
		    }

		}
	});
}
