<%inherit file="base.mako"/>
<%namespace file="base.mako" import="posts"/>
takže? ${data["data"]}


<%
    all_posts = list(posts.order_by("id").run(conn))
%>
% for post in all_posts:
    ${post["header"]["cze"]}
% endfor