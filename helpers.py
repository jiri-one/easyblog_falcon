from settings import posts_per_page, templatelookup
import re
from unidecode import unidecode

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