from rethinkdb import RethinkDB
#import sys
#sys.path.append("../")

#from math import ceil

#from settings import posts_per_page


# RethinkDB settings
r = RethinkDB()
conn = r.connect( "192.168.222.20", 28015).repl()
topics = r.db("blog_jirione").table("topics")
#posts = r.db("blog_jirione").table("posts")

#posts_count = posts.count().run(conn)

#page_count = ceil(posts_count / posts_per_page)
#pages = range(1,page_count+1)

months = {'cze': ('Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen', 'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec'), 'eng': ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')}

def format_date(date):
	splited_date = date.split("-")
	final_date = f"""
	     {str(int(splited_date[2]))}. 
	     {str(months["cze"][int(splited_date[1])-1])}, 
	     {str(splited_date[0])}"""
	return final_date

temata = "Knihy;Linux;Seriály;Filmy;O LinuxGames.cz;Hry;Život;Ostatní;Programování;"

def format_topics(post_topics, all_topics):
	topics_in_list = list(filter(None, post_topics.split(";")))
	topics_links = ""
	for topic_name_in_post in topics_in_list:
		for topic_from_list in all_topics:
			if topic_from_list["topic"]["cze"] == topic_name_in_post:
				topic_url = topic_from_list["url"]["cze"]
				# in first version I wanted to get the url from database, but I would like to not acces to db from templates
				# topic_url = list(topics.filter(r.row["topic"]["cze"] == topic_name).run(conn))[0]["url"]["cze"]
				topic_link = f"""<a href="/tema/{topic_url}">{topic_name_in_post}</a>"""
				topics_links = topics_links + ", " + topic_link
	return topics_links[2:] # this slice here is for delete firs comma