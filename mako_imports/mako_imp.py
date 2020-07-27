# import RethinkDB
from rethinkdb import RethinkDB
import sys
sys.path.append("../")

from math import ceil

from settings import posts_per_page


# RethinkDB settings
r = RethinkDB()
conn = r.connect( "192.168.222.20", 28015).repl()
topics = r.db("blog_jirione").table("topics")
posts = r.db("blog_jirione").table("posts")

posts_count = posts.count().run(conn)

page_count = ceil(posts_count / posts_per_page)
pages = range(1,page_count+1)