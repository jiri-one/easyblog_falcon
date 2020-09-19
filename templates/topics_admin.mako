<%inherit file="base.mako"/>

<a title="Vytvořit nové téma" href="/new_topic">[Vytvořit nové téma]</a><br><br>
% for topic in data["topics"]:
	
	<b>Pořadí tématu: ${topic["order"]}</b>
	<a title="Editovat tento téma" href="/edit_topic/${topic["id"]}">[EDIT]</a> 
	<a title="Smazat toto téma" href="/delete_topic/${topic["id"]}">[X]</a>
	<dl>
	<dt><b>Téma CZE: </b>${topic["topic"]["cze"]}</dt>
	<dt><b>Téma ENG: </b>${topic["topic"]["eng"]}</dt>
	<dd><b>Popis CZE: </b>${topic["description"]["cze"]}</dd>
	<dd><b>Popis ENG: </b>${topic["description"]["eng"]}</dd>
	</dl><br>
% endfor

