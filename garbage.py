# not necessary now, but maybe useful in the future
def render_template_decor(template_name):
	print(template_name)
	def original_func(func):
		print(func)
		def wrapper(objects, req, resp):
			#resp.body = serve_template(template_name, data="test")
			for response in objects:
				if isinstance(response, falcon.Response):
					my_response = response
			print(my_response.body)
			resp.body = serve_template(template_name, test = "krleš", data=resp.body)
			print(resp.body)
			modified_func = func(objects, req, resp)
			return modified_func
		return wrapper
	return original_func

def serve_template(templatename, **kwargs):
	mytemplate = templatelookup.get_template(templatename)
	return mytemplate.render(**kwargs)