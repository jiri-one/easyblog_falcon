<!DOCTYPE html>
<html lang="cs">
<head>
	<title>Jiřího blog</title>
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	<meta name="description" content="Osobní blog o knihách, Linuxu, programování a prostě o životě.">
	<meta name="keywords" content="Linux, Python, programování, hry, seriály, filmy">
	<meta name="author" content="Jiri One">
	<link rel="stylesheet" href="/templates/reset.css">
	<link rel="stylesheet" href="/templates/styles.css">
	<link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon"> 
</head>
<body class="container">
<header>
<div class="title">
<a href="/?lang=cze">
	<img alt="Přepnout stránku na český jazyk" class="img_flag" src="/templates/flag_cze.svg"/></a>
 ·:[ <a href="/">Jiřího blog</a> ]:· 
<a href="/?lang=eng">
	<img alt="Switch site to english language" class="img_flag" src="/templates/flag_eng.svg"/></a>
</div>
</header>
<nav>
<div class="menu">
<b>O autorovi:</b><br>
<a class="topics" href="/o-mne">O mně</a>
<br>
<b>Témata:</b>
<div class="topics">
% for topic in data["topics"][:-1]: #all topics except of last one
	<a style="border-bottom: 1px solid #3c67be;" href="/tema/${topic["url"]["cze"]}">${topic["topic"]["cze"]}</a>
% endfor
## and just last topic (index [-1]) alone, because it does not include border-bottom
<a href="/tema/${data["topics"][-1]["url"]["cze"]}">${data["topics"][-1]["topic"]["cze"]}</a> 
	

</div><!-- .topics-->
<br>
<div class="search_form">
<b>Vyhledávání:</b>
<form method="post" action="/hledej/" accept-charset="UTF-8">
<input type="text" id="vyhledavani" name="search"><br>
<input type="submit" value="Vyhledat">
</form></div><!-- .search_form-->
<br>
<div class="nav-other">
	<b>Zajímavé odkazy:</b>
	<div class="other-links">
	<a style="border-bottom: 1px solid #3c67be;" href="https://github.com/jiri-one" target="_blank">Můj GitHub profil</a>
	<a style="border-bottom: 1px solid #3c67be;" href="http://EasyDict.jiri.one/" target="_blank">EasyDict.jiri.one</a>
	<a style="border-bottom: 1px solid #3c67be;" href="http://LinuxGames.cz" target="_blank">LinuxGames.cz</a>
	<a href="https://archlinux.org" target="_blank">ArchLinux.org</a>
	</div>
</div>

</div><!-- .menu-->
</nav>
<main>
<div id="middle">
${self.body()}
</div><!-- #middle-->
<div class="footer-other"> <!-- this links are here second time, because they are down in responsive view -->
	<br><b>Zajímavé odkazy:</b>
	<div class="other-links">
	<a style="border-bottom: 1px solid #3c67be;" href="https://codeberg.org/jiri.one" target="_blank">Mé GIT repozitáře</a>
	<a style="border-bottom: 1px solid #3c67be;" href="http://EasyDict.jiri.one/" target="_blank">EasyDict.jiri.one</a>
	<a style="border-bottom: 1px solid #3c67be;" href="http://LinuxGames.cz" target="_blank">LinuxGames.cz</a>
	<a href="https://archlinux.org" target="_blank">ArchLinux.org</a>
	</div>
</div>
</main>
<footer>Jiří Němec, 2022</footer>
</body>
</html>
