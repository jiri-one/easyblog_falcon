<%inherit file="base.mako"/>

<div class="comment_title">Editovat příspěvek:</div><hr>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8">
	<b>Kategorie příspěvku:</b>
	
	% for topic in data["topics"]:
		<div class="topics_admin"><span style="white-space: nowrap;">
		% if topic["topic"]["cze"] in data["post"]["topics"]["cze"].split(";"):
			<input type="checkbox" id="" value="${topic["topic"]["cze"]}" name="${topic["url"]["cze"]}" checked	>
		% else:
			<input type="checkbox" id="" value="${topic["topic"]["cze"]}" name="${topic["url"]["cze"]}"	>
		% endif
		<label for="${topic["url"]["cze"]}"> ${topic["topic"]["cze"]}</label></span></div>
	% endfor

	<br><br><label for="post_header">Titulek:</label><br>
	<input type="text" name="post_header" style="width:100%;" value="${data["post"]["header"]["cze"]}"><br>
	
	<label for="post_header">URL příspěvku:</label><br>
	<input type="text" name="post_url" style="width:100%;" value="${data["post"]["url"]["cze"]}"><br>

	<label for="post_content">Text příspěvku:</label><br>
	<textarea name="post_content" style="height:400px; width:100%;">${data["post"]["content"]["cze"]}</textarea><br>

	<input type="submit" value="Odeslat">
</form>
</div>