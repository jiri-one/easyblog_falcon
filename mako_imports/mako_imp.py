# import RethinkDB
#from rethinkdb import RethinkDB
#import sys
#sys.path.append("../")

#from math import ceil

#from settings import posts_per_page


# RethinkDB settings
#r = RethinkDB()
#conn = r.connect( "192.168.222.20", 28015).repl()
#topics = r.db("blog_jirione").table("topics")
#posts = r.db("blog_jirione").table("posts")

#posts_count = posts.count().run(conn)

#page_count = ceil(posts_count / posts_per_page)
#pages = range(1,page_count+1)

last_date = None
months = {'cze': ('Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec'), 'eng': ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')}

def format_date(date):
	splited_date = date.split("-")
	final_date = f"""
	     {str(int(splited_date[2]))}. 
	     {str(months["cze"][int(splited_date[1])-1])}, 
	     {str(splited_date[0])}"""
	return final_date