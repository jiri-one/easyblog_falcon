<%inherit file="base.mako"/>

<div class="comment_title">Nový příspěvek:</div><hr>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8">
	<b>Kategorie příspěvku:</b>
	
	% for topic in data["topics"]:
		<div class="topics_admin"><span style="white-space: nowrap;">
		<input type="checkbox" id="" value="${topic["topic"]["cze"]}" name="topic_${topic["url"]["cze"]}">
		<label for="topic_${topic["url"]["cze"]}"> ${topic["topic"]["cze"]}</label><span></div>
	% endfor

	<br><br><label for="post_header">Titulek:</label><br>
	<input type="text" required="required" name="post_header" placeholder="Nadpis přístpěvku.." style="width:100%;"><br>
	
	<label for="post_content">Text příspěvku:</label><br>
	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script>window.jQuery || document.write('<script src="js/vendor/jquery-3.3.1.min.js"><\/script>')</script>
	
	<script src="https://cdnjs.cloudflare.com/ajax/libs/Trumbowyg/2.25.1/trumbowyg.min.js"></script>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Trumbowyg/2.25.1/ui/trumbowyg.min.css">

	<textarea id="editor" required="required" name="post_content" placeholder="Napiš něco.." style="height:400px; width:100%;"></textarea><br>
	<script>
    $('#editor').trumbowyg();
	</script>
	
	<input type="submit" name="public" value="Publikovat">
	<input type="submit" name="draft" value="Do rozepsaných">
</form>
</div>
