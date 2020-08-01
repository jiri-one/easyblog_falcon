import falcon
from math import ceil
from settings import file_path, posts_per_page, topics, posts, conn, r
from helpers import render_template, slice_posts

class EasyBlog(object):
	def __init__(self):
		self.all_topics = list(topics.order_by("id").run(conn))
	
	@falcon.after(render_template, "index.mako")
	def on_get(self, req, resp):
		"""Handles GET requests on index (/)"""
		#resp.status = falcon.HTTP_200  # This is the default status
		start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
		index_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(conn))
		posts_count = posts.count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))		
		resp.body = {"posts": index_posts, "topics": self.all_topics, "pages": pages}
	
	@falcon.after(render_template, "index.mako")
	def on_get_page(self, req, resp, page_number):
		"""Handles GET requests on /page/{page_number} and /strana/{page_number}"""
		start, end = slice_posts(page_number)
		page_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(conn))
		posts_count = posts.count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": page_posts, "topics": self.all_topics, "pages": pages, "page": page_number}
	
	@falcon.after(render_template, "index.mako")
	def on_get_topic(self, req, resp, topic_url):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(1) # number one is here hardcoded, because index of topic is always page one
		topic = topics.filter(r.row["url"]["cze"] == topic_url).order_by("id").run(conn)[0]["topic"]["cze"]
		topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(conn))
		topic_url = "/tema/" + topic_url + "/"
		posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": topic_posts, "topics": self.all_topics, "added_url": topic_url, "pages": pages}
		
	@falcon.after(render_template, "index.mako")
	def on_get_topic_page(self, req, resp, topic_url, page_number):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(page_number)
		topic = topics.filter(r.row["url"]["cze"] == topic_url).order_by("id").run(conn)[0]["topic"]["cze"]
		topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(conn))
		topic_url = "/tema/" + topic_url + "/"
		posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": topic_posts, "topics": self.all_topics, "added_url": topic_url, "pages": pages, "page": page_number}
		
	@falcon.after(render_template, "index.mako")
	def on_get_search(self, req, resp, searched_word):
		start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
		regex_word = "(?i)" + searched_word # for case insensitivity
		results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(conn))
		search_url = "/hledej/" + searched_word + "/"
		posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))		
		resp.body = {"posts": results, "topics": self.all_topics, "added_url": search_url, "pages": pages}
			
	@falcon.after(render_template, "index.mako")
	def on_get_search_page(self, req, resp, searched_word, page_number):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(page_number) # number one is here hardcoded, because index is always page one
		regex_word = "(?i)" + searched_word # for case insensitivity
		results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(conn))
		search_url = "/hledej/" + searched_word + "/"
		posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))		
		resp.body = {"posts": results, "topics": self.all_topics, "added_url": search_url, "pages": pages, "page": page_number}
	
	def on_post_search_form(self, req, resp):
		print(req.get_param("search"))
		searched_word = req.get_param("search")
		new_url = f"/hledej/{searched_word}"
		raise falcon.HTTPSeeOther(new_url)
		
# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML)
app.req_options.auto_parse_form_urlencoded = True
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)

# Resources are represented by long-lived class instances
easyblog = EasyBlog()
app.add_route('/', easyblog)
app.add_route('/page/{page_number:int}', easyblog, suffix="page")
app.add_route('/strana/{page_number:int}', easyblog, suffix="page")
app.add_route('/topic/{topic_url}', easyblog, suffix="topic")
app.add_route('/tema/{topic_url}', easyblog, suffix="topic")
app.add_route('/topic/{topic_url}/page/{page_number:int}', easyblog, suffix="topic_page")
app.add_route('/tema/{topic_url}/strana/{page_number:int}', easyblog, suffix="topic_page")
app.add_route('/search/', easyblog, suffix="search_form")
app.add_route('/hledej/', easyblog, suffix="search_form")
app.add_route('/search/{searched_word}', easyblog, suffix="search")
app.add_route('/hledej/{searched_word}', easyblog, suffix="search")
app.add_route('/search/{searched_word}/page/{page_number:int}', easyblog, suffix="search_page")
app.add_route('/hledej/{searched_word}/strana/{page_number:int}', easyblog, suffix="search_page")

#from hupper import start_reloader
from waitress import serve
#reloader = start_reloader("easyblog.app") #test
#reloader.watch_files(['settings.py', 'helpers.py', 'mako_imports/mako_imp.py'])
serve(app, host='0.0.0.0', port=8080)