<%inherit file="base.mako"/>

<div class="comment_title">Nový příspěvek:</div><hr>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8">
	<b>Kategorie příspěvku:</b>
	
	% for topic in data["topics"]:
		<div class="topics_admin"><span style="white-space: nowrap;">
		<input type="checkbox" id="" value="${topic["topic"]["cze"]}" name="${topic["url"]["cze"]}">
		<label for="${topic["url"]["cze"]}"> ${topic["topic"]["cze"]}</label><span></div>
	% endfor

	<br><br><label for="post_header">Titulek:</label><br>
	<input type="text" required="required" name="post_header" placeholder="Nadpis přístpěvku.." style="width:100%;"><br>
	
	<label for="post_content">Text příspěvku:</label><br>
	
	<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/jodit/3.4.25/jodit.min.css">
	<script src="//cdnjs.cloudflare.com/ajax/libs/jodit/3.4.25/jodit.min.js"></script>
	
	<textarea id="editor" required="required" name="post_content" placeholder="Napiš něco.." style="height:400px; width:100%;"></textarea><br>
	<script>var editor = new Jodit("#editor", {
	"minHeight": 400,
	"buttons": "source,,,,,,,brush,|,ul,ol,|,outdent,indent,|,|,image,file,video,table,link,,align,undo,redo,\n,selectall,cut,copy,paste,copyformat,|,hr,symbol,fullsize,print,preview,find"
	});</script>
	
	<input type="submit" value="Odeslat">
</form>
</div>