import falcon
from wsgiref import simple_server
from mako.lookup import TemplateLookup
from settings import file_path, topics, posts, conn, r, slice_posts

templatelookup = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules', collection_size=500, output_encoding='utf-8', encoding_errors='replace')

# decorator for Mako templates - works on GET method
def render_template(req, resp, resource, template):
	mytemplate = templatelookup.get_template(template)
	others = {"posts_count": 227}
	resp.body = mytemplate.render(data=resp.body, others=others)

class EasyBlog(object):
	def __init__(self):
		self.all_topics = list(topics.order_by("id").run(conn))
		self.posts_count = posts.count().run(conn)
	
	@falcon.after(render_template, "index.mako")
	def on_get(self, req, resp):
		"""Handles GET requests on index (/)"""
		#resp.status = falcon.HTTP_200  # This is the default status
		start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
		index_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(conn))
		resp.body = {"posts": index_posts, "topics": self.all_topics, "posts_count": self.posts_count}
	
	@falcon.after(render_template, "index.mako")
	def on_get_page(self, req, resp, page_number):
		"""Handles GET requests on /page/{page_number} od /strana/{page_number}"""
		start, end = slice_posts(page_number)
		page_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(conn))
		resp.body = {"posts": page_posts, "topics": self.all_topics, "posts_count": self.posts_count}

# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML)
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)

# Resources are represented by long-lived class instances
easyblog = EasyBlog()
app.add_route('/', easyblog)
app.add_route('/page/{page_number:int}', easyblog, suffix="page")
app.add_route('/strana/{page_number:int}', easyblog, suffix="page")

from hupper import start_reloader
from waitress import serve
reloader = start_reloader("easyblog.app") #test
reloader.watch_files(['settings.py'])
serve(app, host='0.0.0.0', port=8080)