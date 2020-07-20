import falcon
from wsgiref import simple_server
from mako.lookup import TemplateLookup
from settings import file_path, topics, posts

templatelookup = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules', collection_size=500, output_encoding='utf-8', encoding_errors='replace')

# decorator for Mako templates - forks on GET method
def render_template(req, resp, resource, template):
	mytemplate = templatelookup.get_template(template)
	resp.body = mytemplate.render(data=resp.body)

class EasyBlog(object):
	def __init__(self):
		"""Just init base mako template"""
		base_template = templatelookup.get_template("base.mako")
		
		base_template.render(data=DOPLNIME)
	
	@falcon.after(render_template, "index.mako")
	def on_get(self, req, resp):
		"""Handles GET requests"""
		#resp.status = falcon.HTTP_200  # This is the default status
		resp.body = {"data": "uvidime"}
		

# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML)
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)

# Resources are represented by long-lived class instances
easyblog = EasyBlog()

# things will handle all requests to the '/things' URL path
app.add_route('/', easyblog)
