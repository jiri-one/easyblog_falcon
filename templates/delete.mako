<%inherit file="base.mako"/>
<div class="titulek">Chystáš se smazat příspěvek:</div>
<center>
Nadpis mazaného příspěvku: <b>${data["post"]["header"]["cze"]}</b><br>
URL mazaného příspěvku: <b>${data["post"]["url"]["cze"]}</b><br>
Tento příspěvek má <b>${data["post"]["comments"]} komentářů</b>, které budou smazány s ním.<br>
<br><b>Chceš ho opravdu smazat?</b>
<div class="comment_form">
<form method="get" action="" accept-charset="UTF-8">
	<input type="submit" name="delete" value="Ano"> <input type="submit" name="delete" value="Ne">
</form>
</div>
</center>