<%inherit file="base.mako"/>

<div class="titulek">${data["post"]["header"]["cze"]}</div>
## this part is here because of admin staff and if I am authorized, then I can dele or edit post
% if data["authorized"] == 1:
	<div style="float: right;">
	<a title="Editovat tento příspěvek" href="/edit/${data["post"]["url"]["cze"]}">[EDIT]</a> 
	<a title="Smazat tento příspěvek" href="/delete/${data["post"]["url"]["cze"]}">[X]</a>
	</div>
% endif

<div class="meta"><div class="zarazen_do">Zařazen do: ${mako_imp.format_topics(data["post"]["topics"]["cze"], data["topics"])} — Jiří, ${mako_imp.format_date(data["post"]["when"].split()[0][0:10])} @ ${data["post"]["when"].split()[1][0:5]}
</div></div>
${data["post"]["content"]["cze"]}<br>
<div class="postend">• • •</div>

% if data["post"]["comments"] > 0:
	<div id="komentare"><div class="comment_title">Komentáře:</div></div>
	% for comment in data["comments"]:
		<div class="comment_header">
		<b>${comment["header"]}</b>
		% if data["authorized"] == 1:
			<div style="float: right;">
			<a title="Smazat tento komentář" href="/delete_comment/${comment["id"]}">[X]</a>
			</div>
		% endif
		<br>
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
	<input type="text" required="required" name="comment_header" placeholder="Nadpis komentáře.."><br>

	<label for="comment_nick">Nick:</label><br>
	<input type="text" required="required" name="comment_nick" placeholder="Tvoje přezdívka.."><br>
	
	<label for="antispam">Antispam:</label><br>
	<input type="text" required="required" name="antispam" placeholder="Napiš číslem pětku."><br>
	
	<label for="comment_content">Text komentáře:</label><br>
	<textarea name="comment_content" required="required" placeholder="Napiš něco.." style="height:200px"></textarea><br>

	<input type="submit" value="Odeslat">
</form>
</div>