# import RethinkDB
from rethinkdb import RethinkDB
# import mako
from mako.lookup import TemplateLookup

# RethinkDB settings
r = RethinkDB()
rethinkdb_ip = "192.168.222.20"
rethinkdb_port = 28015
topics = r.db("blog_jirione").table("topics")
posts = r.db("blog_jirione").table("posts")
comments = r.db("blog_jirione").table("comments")
authors = r.db("blog_jirione").table("authors")

# blog settings
posts_per_page = 10 # here you can set post per page, it will everywher in the blog

# mako settings
templatelookup = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules', collection_size=500, output_encoding='utf-8', encoding_errors='replace', imports=['from mako_imports import mako_imp'])

#### my notes
# I created secondary index for CZE url
# posts.index_create("url_cze", r.row["url"]["cze"]).run(conn)
#### and how to insert new author
# authors.insert({"name": "", "password": "", "cookie": ""})