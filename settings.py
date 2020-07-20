# import to set current working directory
from os import path, chdir
from glob import glob
# import RethinkDB
from rethinkdb import RethinkDB

# set current working directory
cwd = path.dirname(path.abspath(__file__))
chdir(cwd)

# file path helpers
def file_path(file_name):
    """This function return full absolute path of given file_name, but it works correctly only when the filename is unique in all folders and subfolders!!!"""
    file_abs_path = path.abspath(glob(f"**/{file_name}", recursive=True)[0])
    return file_abs_path

# RethinkDB settings
r = RethinkDB()
conn = r.connect( "192.168.222.20", 28015).repl()
topics = r.db("blog_jirione").table("topics")
posts = r.db("blog_jirione").table("posts")