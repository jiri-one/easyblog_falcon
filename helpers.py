from settings import posts_per_page, templatelookup, topics, authors, r, rethinkdb_ip, rethinkdb_port
import re
from unidecode import unidecode
from rethinkdb.errors import ReqlDriverError
from falcon.errors import HTTPError
# import to set current working directory
from os import path, chdir
from glob import glob

# set current working directory
cwd = path.dirname(path.abspath(__file__))
chdir(cwd)

# file path helper
def file_path(file_name):
	"""This function return full absolute path of given file_name, but it works correctly only when the filename is unique in all folders and subfolders!!!"""
	file_abs_path = path.abspath(glob(f"**/{file_name}", recursive=True)[0])
	return file_abs_path

def render_template(req, resp, resource, template):
	"""@falcon.after decorator for Mako templates - works on GET and POST methodes"""
	all_topics = list(topics.order_by("order").run(req.context.conn)) # this line and
	resp.text["topics"] = all_topics # this line are here because we need refresh topic everytime, so is best to do in on one place
	mytemplate = templatelookup.get_template(template)
	resp.text = mytemplate.render(data=resp.text)
	
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

def reorder_topics(topics, req):
	for new_order, topic in enumerate(topics.order_by("order").run(req.context.conn), start=1):
		topics.get(topic["id"]).update({"order": new_order}).run(req.context.conn)

class Authorize(object): # I will see in the future, if I will need this decorator to be class or just function
	"""@falcon.before decorator for authorize if successful login - works on GET and POST methodes"""
	def __call__(self, req, resp, resource, params):
		resp.context.authorized = 0
		if req.get_cookie_values('cookie_uuid'):
			cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
			for author in list(authors.run(req.context.conn)):
				if author["cookie"] == cookie_uuid:
					resp.context.authorized = 1
					break

class RethinkDBConnector(object):
	def process_resource(self, req, resp, resource, params):
		try:
			req.context.conn = r.connect(rethinkdb_ip, rethinkdb_port)
		except ReqlDriverError:
			print("Database connection could be established.")
			raise HTTPError(title="Database connection fail.\n", description="Database connection could be established.")

	def process_response(self, req, resp, resource, req_succeeded):
		try:
			req.context.conn.close()
		except AttributeError:
			pass		
