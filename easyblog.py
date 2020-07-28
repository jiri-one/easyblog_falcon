import falcon
from wsgiref import simple_server
from settings import file_path, topics, posts, conn, r
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
		resp.body = {"posts": index_posts, "topics": self.all_topics}
	
	@falcon.after(render_template, "index.mako")
	def on_get_page(self, req, resp, page_number):
		"""Handles GET requests on /page/{page_number} and /strana/{page_number}"""
		start, end = slice_posts(page_number)
		page_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(conn))
		print(req.relative_uri)
		resp.body = {"posts": page_posts, "topics": self.all_topics, "page": page_number}
	
	@falcon.after(render_template, "index.mako")
	def on_get_topic(self, req, resp, topic_url):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(1) # number one is here hardcoded, because index of topic is always page one
		topic = topics.filter(r.row["url"]["cze"] == topic_url).order_by("id").run(conn)[0]["topic"]["cze"]
		topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(conn))
		resp.body = {"posts": topic_posts, "topics": self.all_topics}
		
# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML)
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)

# Resources are represented by long-lived class instances
easyblog = EasyBlog()
app.add_route('/', easyblog)
app.add_route('/page/{page_number:int}', easyblog, suffix="page")
app.add_route('/strana/{page_number:int}', easyblog, suffix="page")
app.add_route('/topic/{topic_url}', easyblog, suffix="topic")
app.add_route('/tema/{topic_url}', easyblog, suffix="topic")


#from hupper import start_reloader
from waitress import serve
#reloader = start_reloader("easyblog.app") #test
#reloader.watch_files(['settings.py', 'helpers.py', 'mako_imports/mako_imp.py'])
serve(app, host='0.0.0.0', port=8080)