import falcon
from wsgiref import simple_server
from mako.lookup import TemplateLookup
from settings import file_path, topics, posts, conn, r

templatelookup = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules', collection_size=500, output_encoding='utf-8', encoding_errors='replace')

# decorator for Mako templates - forks on GET method
def render_template(req, resp, resource, template):
	mytemplate = templatelookup.get_template(template)
	resp.body = mytemplate.render(data=resp.body)

class EasyBlog(object):
	@falcon.after(render_template, "index.mako")
	def on_get(self, req, resp):
		"""Handles GET requests"""
		#resp.status = falcon.HTTP_200  # This is the default status
		all_posts = list(posts.order_by(r.desc("when")).run(conn))
		all_topics = list(topics.order_by("id").run(conn))
		resp.body = {"posts": all_posts, "topics": all_topics}

# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML)
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)

# Resources are represented by long-lived class instances
easyblog = EasyBlog()
app.add_route('/', easyblog)

#for windows run
from waitress import serve
serve(app, host='0.0.0.0', port=8080)