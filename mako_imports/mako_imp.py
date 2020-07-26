# import RethinkDB
from rethinkdb import RethinkDB

# RethinkDB settings
r = RethinkDB()
conn = r.connect( "192.168.222.20", 28015).repl()
topics = r.db("blog_jirione").table("topics")
posts = r.db("blog_jirione").table("posts")

posts_count = posts.count().run(conn)
test = 10
