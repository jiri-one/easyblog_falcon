# import to set current working directory
from os import path, chdir
from glob import glob
# import RethinkDB
from rethinkdb import RethinkDB, errors
# import mako
from mako.lookup import TemplateLookup

# set current working directory
cwd = path.dirname(path.abspath(__file__))
chdir(cwd)

# RethinkDB settings
r = RethinkDB()
try:
    conn = r.connect( "192.168.222.20", 28015)
except errors.ReqlDriverError:
    print("Database connection could be established.")
topics = r.db("blog_jirione").table("topics")
posts = r.db("blog_jirione").table("posts")
comments = r.db("blog_jirione").table("comments")
authors = r.db("blog_jirione").table("authors")

# authors.insert({"name": "", "password": "", "cookie": ""})
# blog settings
posts_per_page = 10 # here you can set post per page, it will everywher in the blog

# file path helpers
def file_path(file_name):
    """This function return full absolute path of given file_name, but it works correctly only when the filename is unique in all folders and subfolders!!!"""
    file_abs_path = path.abspath(glob(f"**/{file_name}", recursive=True)[0])
    return file_abs_path

templatelookup = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules', collection_size=500, output_encoding='utf-8', encoding_errors='replace', imports=['from mako_imports import mako_imp'])

#### my notes
# I created secondary index for CZE url
# posts.index_create("url_cze", r.row["url"]["cze"]).run(conn)
