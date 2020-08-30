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
	<input type="text" name="post_header" placeholder="Nadpis přístpěvku.." style="width:100%;"><br>

	<label for="post_content">Text příspěvku:</label><br>
	<textarea name="post_content" placeholder="Napiš něco.." style="height:400px; width:100%;"></textarea><br>

	<input type="submit" value="Odeslat">
</form>
</div>