<%inherit file="base.mako"/>

<div class="titulek">${data["post"]["header"]["cze"]}</div>
<div class="meta"><div class="zarazen_do">Zařazen do: ${mako_imp.format_topics(data["post"]["topics"]["cze"], data["topics"])} — Jiri, ${mako_imp.format_date(data["post"]["when"].split()[0][0:10])} @ ${data["post"]["when"].split()[1][0:5]}
</div></div>
${data["post"]["content"]["cze"]}<br>
<div class="postend">• • •</div>

% if data["post"]["comments"] > 0:
	<div id="komentare"><div class="comment_title">Komentáře:</div></div>
	% for comment in data["comments"]:
		<div id="comment_header">
		<b>${comment["header"]}</b><br>
		Komentář od <b>${comment["nick"]}</b> — ${mako_imp.format_date(comment["when"].split()[0][0:10])} @ ${comment["when"].split()[1][0:5]}
		</div>
		${comment["content"]}<br><br>
	% endfor
% endif
<hr>
<div class="comment_title">Nový komentář:</div>
<div class="comment_form">
<form method="post" action="" accept-charset="UTF-8">
	<label for="comment_header">Nadpis:</label><br>
	<input type="text" name="comment_header" placeholder="Nadpis komentáře.."><br>

	<label for="comment_nick">Nick:</label><br>
	<input type="text" name="comment_nick" placeholder="Tvoje přezdívka.."><br>
	
	<label for="antispam">Antispam:</label><br>
	<input type="text" name="antispam" placeholder="Napiš číslem pětku."><br>
	
	<label for="comment_content">Text komentáře:</label><br>
	<textarea name="comment_content" placeholder="Napiš něco.." style="height:200px"></textarea><br>

	<input type="submit" value="Odeslat">
</form>
</div>