<%inherit file="base.mako"/>

<%
     last_date = None
     months = {'cze': ('Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec'), 'eng': ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')}
%>

<%def name="format_date(date)">
     <%
     splited_date = date.split("-")
     final_date = f"""
     {str(int(splited_date[2]))}. 
     {str(months["cze"][int(splited_date[1])-1])}, 
     {str(splited_date[0])}"""
     %>
     ${final_date}
</%def>

% for post in data["posts"]:
     % if last_date != post["when"].split()[0][0:10]:
          <div class="date">${format_date(post["when"].split()[0][0:10])}</div>  
     % endif
     <div class="titulek"><a href="/${post["url"]["cze"]}">${post["header"]["cze"]}</a></div>
     <div class="meta">
     <div class="zarazen_do">Zařazen do: <a href="${post["topics"]["cze"]}"> ${post["topics"]["cze"]} </a> — Jiri @ ${post["when"].split()[1][0:5]}</div></div>
     <div class="obsah">${post["content"]["cze"]}</div>
     <div class="feedback" align="right">Počet komentářů: ${post["comments"]}</div> 
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



     
