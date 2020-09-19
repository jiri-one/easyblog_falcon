<%inherit file="base.mako"/>

<div class="comment_title">Nové téma zápisků:</div><hr>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8">
	<label for="topic_cze"><b>Název tématu v CZE:</b></label><br>
	<input type="text" required="required" name="topic_cze" placeholder="Název tématu v CZE" style="width:100%;" value="${data["topic"]["topic"]["cze"]}"><br>
	
	<label for="topic_eng">Název tématu v ENG:</label><br>
	<input type="text" name="topic_eng" placeholder="Název tématu v ENG" style="width:100%;" value="${data["topic"]["topic"]["eng"]}"><br>
	
	<label for="url_cze"><b>URL adresa tématu v CZE:</b></label><br>
	<input type="text" required="required" name="url_cze" placeholder="Popis tématu v CZE" style="width:100%;" value="${data["topic"]["url"]["cze"]}"><br>
	
	<label for="url_eng">URL adresa tématu v ENG:</label><br>
	<input type="text" name="url_eng" placeholder="Popis tématu v ENG" style="width:100%;" value="${data["topic"]["url"]["eng"]}"><br>
	
	<label for="description_cze">Popis tématu v CZE:</label><br>
	<input type="text" name="description_cze" placeholder="Popis tématu v CZE" style="width:100%;" value="${data["topic"]["description"]["cze"]}"><br>
	
	<label for="description_eng">Popis tématu v ENG:</label><br>
	<input type="text" name="description_eng" placeholder="Popis tématu v ENG" style="width:100%;" value="${data["topic"]["description"]["eng"]}"><br>
	
	<label for="order"><b>Pořadí tématu:</b></label><br>
	<input type="number" step=".1" required="required" name="order" placeholder="Pořadí může být jakékoliv celé číslo nebo desetinné číslo, které bude určovat výsledné pořadí." style="width:100%;" value="${data["topic"]["order"]}"><br>
	<b>[Tučné texty je nutné vyplnit.]</b><br>

	<input type="submit" value="Odeslat">
</form>
</div>