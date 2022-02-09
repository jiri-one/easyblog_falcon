<%inherit file="base.mako"/>
<%
     last_date = None
%>

<!-- this part is here only for topics and search, it shows what you are searched or current topic-->
<b>
% if "added_url" in data:
    % if ("/hledej/" in data["added_url"] or "/search/" in data["added_url"]) and len(data["posts"]) == 0:
        Nebyly nalezeny žádné výsledky pro vyhledávání slova "${data["added_url"].split("/")[2]}".
    % elif "/hledej/" in data["added_url"] or "/search/" in data["added_url"]:
        Nacházíte se ve výsledcích vyhledávání slova "${data["added_url"].split("/")[2]}":
    % elif "/tema/" in data["added_url"] or "/topic/" in data["added_url"]:
        % for topic in data["topics"]:
            % if topic["url"]["cze"] == data["added_url"].split("/")[2]:
                Nacházíte se v tématu "${topic["topic"]["cze"]}":
            % endif
        % endfor
    % endif
% endif
</b><br><br>

% for post in data["posts"]:
     % if last_date != post["when"].split()[0][0:10]:
          <div class="date">${mako_imp.format_date(post["when"].split()[0][0:10])}</div>  
     % endif
     <div class="titulek"><a href="/${post["url"]["cze"]}">${post["header"]["cze"]}</a></div>
     <div class="meta">
     <div class="zarazen_do">Zařazen do: ${mako_imp.format_topics(post["topics"]["cze"], data["topics"])} — Jiří @ ${post["when"].split()[1][0:5]}</div></div>
     <div class="obsah">${post["content"]["cze"]}</div>
     <div class="feedback">Počet komentářů: ${post["comments"]}</div> 
     <div class="postend">• • •</div>
     <% 
          last_date = post["when"].split()[0][0:10]
     %>
% endfor

<div class="pages">
<%
if "page" not in data:
     data["page"] = 1
%>

<%
if "added_url" not in data:
     data["added_url"] = "/"
%>

% if len(data["pages"]) < 2:
     Strana 1/1
% else:
     % if data["page"] == 1 and 2 in data["pages"]:
          <a href="${data["added_url"]}strana/2">Další strana</a>
     % else:
          % for site in data["pages"]:
               % if site == 1:
                    <a href="${data["added_url"]}strana/1">[Zpět na index]</a>         
               % elif site == data["page"]:
                    <a href="${data["added_url"]}strana/${site}">[_]</a> 
               % else:
                    <a href="${data["added_url"]}strana/${site}">[${site}]</a> 
               % endif
          % endfor
     % endif
% endif
</div>



     
