<%inherit file="base.mako"/>
<div class="titulek">Chystáš se smazat téma:</div>
<center>
Název tématu je: <b>${data["topic"]["topic"]["cze"]}</b><br>
Popis tématu je: <b>${data["topic"]["description"]["cze"]}</b><br>
V tomto tématu je zařazeno: <b>${data["posts_count"]}</b> příspěvků<br>
% if data["delete_allowed"] == 0:
	<b><hr>!!! Toto téma nelze smazat, protože jsou v něm příspěvky, 
	které by po smazání tématu nebyly nikam přiřazeny.
	Pokud téma opravdu chceš smazat, tak si projdi příspěvky v tomto tématu 
	a přiřaď jim i jiné kategorie, pak bude smazání umožněno. 
	!!!</b><br>
	Zobrazování příspěvků bez témat by sice fungovalo, ale je to nežádoucí.
	<div class="comment_form">
	<form method="get" action="" accept-charset="UTF-8">
		<input type="submit" name="delete" value="Nemazat a zpět">
	</form>
	</div>
% else:
	<br><b>Chceš ho opravdu smazat?</b>
	<div class="comment_form">
	<form method="get" action="" accept-charset="UTF-8">
		<input type="submit" name="delete" value="Ano"> <input type="submit" name="delete" value="Ne">
	</form>
	</div>
% endif
</center>