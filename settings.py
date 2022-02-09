# import RethinkDB
from rethinkdb import RethinkDB
# import mako
from mako.lookup import TemplateLookup

# RethinkDB settings
db_name = "blog_jirione" # main db is blog_jirione, another one is devel
r = RethinkDB()
rethinkdb_ip = "172.17.0.3"
rethinkdb_port = 28015
topics = r.db(db_name).table("topics")
posts = r.db(db_name).table("posts")
comments = r.db(db_name).table("comments")
authors = r.db(db_name).table("authors")

# blog settings
posts_per_page = 10 # here you can set post per page, it will everywher in the blog

# mako settings
templatelookup = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules', collection_size=500, output_encoding='utf-8', encoding_errors='replace', imports=['from mako_imports import mako_imp'])

###### my notes
#### I created secondary index for CZE url
# posts.index_create("url_cze", r.row["url"]["cze"]).run(conn)
#### and how to insert new author
# authors.insert({"name": "", "password": "", "cookie": ""})
#### and how to copy database to another (devel), because rethinkdb-restore is broken
#conn = r.connect(rethinkdb_ip, rethinkdb_port)
#r.db('blog_jirione').table_list().for_each(r.db('devel').table(r.row).insert(r.db('blog_jirione').table(r.row)))
#r.db('blog_jirione').table_list().for_each(r.db('devel').table(r.row).insert(r.db('blog_jirione').table(r.row))).run(conn)
#posts.index_create("url_cze", r.row["url"]["cze"]).run(conn)
