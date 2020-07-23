<%inherit file="base.mako"/>

<%
     last_date = None
%>
% for post in data["posts"]:
     % if last_date != post["when"].split()[0][0:10]:
          <div class="date">${post["when"]}</div>  
     % endif
     <div class="titulek"><a href="${post["url"]["cze"]}">${post["header"]["cze"]}</a></div>
     <div class="meta">
     <div class="zarazen_do">Zařazen do: <a href="${post["topics"]["cze"]}"> ${post["topics"]["cze"]} </a> — Jiri @ ${post["when"].split()[1][0:5]}</div></div>
     <div class="obsah">${post["content"]["cze"]}</div>
     <div class="feedback" align="right">Počet komentářů: ${post["comments"]}</div> 
     <div class="postend">• • •</div>
     <% 
          last_date = post["when"].split()[0][0:10]
     %>
% endfor