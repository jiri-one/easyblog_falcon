<%!
	from rethinkdb import RethinkDB
	r = RethinkDB()
	conn = r.connect("192.168.222.20", 28015).repl()
	topics = r.db("blog_jirione").table("topics")
	posts = r.db("blog_jirione").table("posts")
%>

<!DOCTYPE html>
<html>
<head>
	<title>Jiřího blog</title>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="/templates/reset.css">
	<link rel="stylesheet" href="/templates/styles.css">
</head>
<body class="container">
<header>
<a title="Přepnout stránku na český jazyk" href="/?lang=cze"><img align="right" class="img_flag" src="/templates/flag_cze.svg"/></a>
<a title="Switch site to english language" href="/?lang=eng"><img align="right" class="img_flag" src="/templates/flag_eng.svg"/></a>
<div class="title">·:[ <a href="http://jiri.one/">Jiřího blog</a> ]:·</div>
</header>
<nav>
<div class="menu">
<b>O autorovi:</b><br>
<a class="topics" href="http://jiri.one/o-mne">O mně</a>
<p>
<b>Témata:</b><br>
<div class="topics">
<%
	all_topics = list(topics.order_by("id").run(conn))
%>
% for topic in all_topics:
	% if topic["id"] != len(all_topics):
		<a style="border-bottom: 1px solid #3c67be;" href="/topics/${topic["url"]["cze"]}">${topic["topic"]["cze"]}</a>
	% else:
		<a href="/topics/${topic["url"]["cze"]}">${topic["topic"]["cze"]}</a>
	% endif
% endfor
</div><!-- .topics-->
</p>
<div class="search_form">
<b>Vyhledávání:</b><br>
<form method="post" action="http://jiri.one/hledej">
<input type="text" id="vyhledavani" name="vyhledavani" size="15"><br>
<button id="Vyhledat" name="Vyhledat">Vyhledat</button>
</form></div><!-- .search_form-->
</div><!-- .menu-->
</nav>
<main>
<div id="middle">
${self.body()}
</div><!-- #middle-->
</main>
<footer>Jiří Němec, 2020</footer>
</body>
</html>
