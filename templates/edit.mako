<%inherit file="base.mako"/>

<div class="comment_title">Editovat příspěvek:</div><hr>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8">
	<b>Kategorie příspěvku:</b>
	
	% for topic in data["topics"]:
		<div class="topics_admin"><span style="white-space: nowrap;">
		% if topic["topic"]["cze"] in data["post"]["topics"]["cze"].split(";"):
			<input type="checkbox" id="" value="${topic["topic"]["cze"]}" name="topic_${topic["url"]["cze"]}" checked	>
		% else:
			<input type="checkbox" id="" value="${topic["topic"]["cze"]}" name="topic_${topic["url"]["cze"]}"	>
		% endif
		<label for="topic_${topic["url"]["cze"]}"> ${topic["topic"]["cze"]}</label></span></div>
	% endfor

	<br><br><label for="post_header">Titulek:</label><br>
	<input type="text" name="post_header" style="width:100%;" value="${data["post"]["header"]["cze"]}"><br>
	
	<label for="post_header">URL příspěvku:</label><br>
	<input type="text" name="post_url" style="width:100%;" value="${data["post"]["url"]["cze"]}"><br>

	<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/jodit/3.4.25/jodit.min.css">
	<script src="//cdnjs.cloudflare.com/ajax/libs/jodit/3.4.25/jodit.min.js"></script>

	<label for="post_content">Text příspěvku:</label><br>
	<textarea id="editor" name="post_content" style="height:400px; width:100%;">${data["post"]["content"]["cze"]}</textarea><br>
	<script>var editor = new Jodit("#editor", {
	"minHeight": 400,
	"buttons": "source,,,,,,,brush,|,ul,ol,|,outdent,indent,|,|,image,file,video,table,link,,align,undo,redo,\n,selectall,cut,copy,paste,copyformat,|,hr,symbol,fullsize,print,preview,find"
	});</script>
	
	% if "added_url" in data:
		% if "/draft_edit" in data["added_url"]:
			<input type="submit" name="public" value="Publikovat">
			<input type="submit" name="draft" value="Znovu Uložit">
		% endif
	% else:
		<input type="submit" value="Editovat">
	% endif
</form>
</div>