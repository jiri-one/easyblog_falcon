from rethinkdb import RethinkDB
db_name = "blog_jirione" # main db is blog_jirione, another one is devel
r = RethinkDB()
r.connect("172.17.0.2", 28015).repl()
r.db(db_name).table_create("drafts").run()
