from settings import posts_per_page, templatelookup, authors, conn
import re
from unidecode import unidecode
from rethinkdb import RethinkDB, errors

def render_template(req, resp, resource, template):
	"""@falcon.after decorator for Mako templates - works on GET and POST methodes"""
	mytemplate = templatelookup.get_template(template)
	resp.body = mytemplate.render(data=resp.body)
	
def slice_posts(page_number):
	"""Simple function, which accpet page number and return numbers of posts (first number and last number)"""
	end = posts_per_page * page_number - 1
	start = end - posts_per_page + 1
	return start, end

def create_url(header):
	"""Function for create url adress from header of post."""
	header = unidecode(header).lower() # firstly make all character lower and remove diacritics
	pattern = re.compile(r"\W") # \W means everythink non-alphanumeric
	splited_header = pattern.split(header) # split header with \W
	splited_header = [i for i in splited_header if i] # list comprehension for remove empty strings from list
	url = "-".join(splited_header) # and finaly join the list splited_header with "-"
	return url

class Authorize(object): # I will see in the future, if I will need this decorator to be class or just function
	"""@falcon.before decorator for authorize if successful login - works on GET and POST methodes"""
	def __call__(self, req, resp, resource, params):
		req.context.authorized = 0
		if req.get_cookie_values('cookie_uuid'):
			cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
			for author in list(authors.run(conn)):
				if author["cookie"] == cookie_uuid:
					req.context.authorized = 1
					break

class DB_Setter(object):
	r = RethinkDB()
	try:
		conn = r.connect( "192.168.222.20", 28015)
		topics = list(r.db("blog_jirione").table("topics").order_by("id").run(conn))
		posts = r.db("blog_jirione").table("posts")
		comments = r.db("blog_jirione").table("comments")
		authors = r.db("blog_jirione").table("authors")			
	except errors.ReqlDriverError:
		print("Database connection could be established.")	

class RethinkDBConnector(object):
	def process_request(self, req, resp):
		"""Process the request before routing it.

		Note:
		    Because Falcon routes each request based on req.path, a
		    request can be effectively re-routed by setting that
		    attribute to a new value from within process_request().

		Args:
		    req: Request object that will eventually be
		        routed to an on_* responder method.
		    resp: Response object that will be routed to
		        the on_* responder.
		"""
		pass

	def process_resource(self, req, resp, resource, params):
		"""Process the request after routing.

		Note:
		    This method is only called when the request matches
		    a route to a resource.

		Args:
		    req: Request object that will be passed to the
		        routed responder.
		    resp: Response object that will be passed to the
		        responder.
		    resource: Resource object to which the request was
		        routed.
		    params: A dict-like object representing any additional
		        params derived from the route's URI template fields,
		        that will be passed to the resource's responder
		        method as keyword arguments.
		"""
		print("první test")
		req.context.db = DB_Setter

	def process_response(self, req, resp, resource, req_succeeded):
		"""Post-processing of the response (after routing).

		Args:
		    req: Request object.
		    resp: Response object.
		    resource: Resource object to which the request was
		        routed. May be None if no route was found
		        for the request.
		    req_succeeded: True if no exceptions were raised while
		        the framework processed and routed the request;
		        otherwise False.
		"""
		print("zavíráme")
		print(resource)
		try:
			req.context.db.conn.close()
		except AttributeError:
			pass		
