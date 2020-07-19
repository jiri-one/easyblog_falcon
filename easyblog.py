import falcon
from wsgiref import simple_server
from mako.template import Template
from mako.lookup import TemplateLookup

templatelookup = TemplateLookup(directories=['templates'], module_directory='/tmp/mako_modules', collection_size=500, output_encoding='utf-8', encoding_errors='replace')

def render_template(req, resp, resource, template):
	mytemplate = templatelookup.get_template(template)
	resp.body = mytemplate.render(data=resp.body)

class EasyBlog(object):
	@falcon.after(render_template, "index.mako")
	def on_get(self, req, resp):
		"""Handles GET requests"""
		#resp.status = falcon.HTTP_200  # This is the default status
		resp.body = {"data": "uvidime"}

# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML)
app.add_static_route("/templates", "/home/jiri/Workspace/EasyBlog/easyblog_falcon/templates", downloadable=True, fallback_filename=None)

# Resources are represented by long-lived class instances
easyblog = EasyBlog()

# things will handle all requests to the '/things' URL path
app.add_route('/', easyblog)
