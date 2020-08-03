from settings import posts_per_page, templatelookup

def render_template(req, resp, resource, template):
	"""@falcon.after decorator for Mako templates - works on GET and POST methodes"""
	mytemplate = templatelookup.get_template(template)
	resp.body = mytemplate.render(data=resp.body)
	
def slice_posts(page_number):
	"""Simple function, which accpet page number and return numbers of posts (first number and last number)"""
	end = posts_per_page * page_number - 1
	start = end - posts_per_page + 1
	return start, end
