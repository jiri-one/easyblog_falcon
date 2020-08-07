<%inherit file="base.mako"/>

<div class="titulek">${data["post"]["header"]["cze"]}</div>
<div class="meta"><div class="zarazen_do">Zařazen do: <a href="http://jiri.one/kategorie/programovani">Programování</a>, <a href="http://jiri.one/kategorie/linux">Linux</a> — Jiri, 17. Červenec, 2020, 
21:24
</div></div>
${data["post"]["content"]["cze"]}<br>
<div class="postend">• • •</div>

% if data["post"]["comments"] > 0:
	<div id="komentare"><h1>Komentáře:</h1></div>
	% for comment in data["comments"]:
		<div id="nadpis_commentu">
		<b>${comment["header"]}</b><br>
		Komentář od <b>${comment["nick"]}</b> — ${mako_imp.format_date(comment["when"].split()[0][0:10])} @ ${comment["when"].split()[1][0:5]}
		</div>
		${comment["content"]}<br><br>
	% endfor	
% endif
<h1>Nový komentář:</h1>

<div id="komentare_obsah">
<form action="" method="post">
<div class="konecobtekani">
<label>Nadpis</label>
<input type="text" id="nadpis_komentare" name="comment_header" size="50"></div>
<div class="konecobtekani">
<label>Nick</label>
<input type="text" id="nick" name="comment_nick" size="50"></div>
<div class="konecobtekani">
<label>Antispam</label>
<input name="antispam" value="Sem napište ČÍSLEM součet čísel dvě a tři (tedy pět ;-))" class="cleardefault" type="text" id="antispam" size="50"></div>
<div class="konecobtekani">
<label>Obsah</label>
<textarea rows="8" id="obsah" name="comment_content" cols="50"></textarea></div>
<div class="konecobtekani">
<button id="Odeslat" name="Odeslat">Odeslat</button></div>
</form>
</div>
<br>
