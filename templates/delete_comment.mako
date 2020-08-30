<%inherit file="base.mako"/>
<div class="titulek">Chystáš se smazat komentář:</div>
<center>
Nadpis mazaného komentáře: <b>${data["comment"]["header"]}</b><br>
Komentář je od: <b>${data["comment"]["nick"]}</b><br>
Komentář je z data: <b>${data["comment"]["when"]}</b><br>
Text komentáře je:<br>${data["comment"]["content"]}<br>
<br><b>Chceš ho opravdu smazat?</b>
<div class="comment_form">
<form method="get" action="" accept-charset="UTF-8">
	<input type="submit" name="delete" value="Ano"> <input type="submit" name="delete" value="Ne">
</form>
</div>
</center>