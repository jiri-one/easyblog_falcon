import falcon
from math import ceil
from datetime import datetime
import argon2
from uuid import uuid4
from settings import file_path, posts_per_page, topics, posts, comments, authors, conn, r
from helpers import render_template, slice_posts, create_url, Authorize

class EasyBlog(object):
	def __init__(self):
		self.all_topics = list(topics.order_by("id").run(conn))
		self.ph = argon2.PasswordHasher()
	
	@falcon.after(render_template, "index.mako")
	def on_get(self, req, resp):
		"""Handles GET requests on index (/)"""
		start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
		index_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(conn))
		posts_count = posts.count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))		
		resp.body = {"posts": index_posts, "topics": self.all_topics, "pages": pages}
	
	@falcon.after(render_template, "index.mako")
	def on_get_page(self, req, resp, page_number):
		"""Handles GET requests on /page/{page_number} and /strana/{page_number}"""
		start, end = slice_posts(page_number)
		page_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(conn))
		posts_count = posts.count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": page_posts, "topics": self.all_topics, "pages": pages, "page": page_number}
	
	@falcon.after(render_template, "index.mako")
	def on_get_topic(self, req, resp, topic_url):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(1) # number one is here hardcoded, because index of topic is always page one
		topic = list(topics.filter(r.row["url"]["cze"] == topic_url).run(conn))[0]["topic"]["cze"]
		topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(conn))
		topic_url = "/tema/" + topic_url + "/"
		posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": topic_posts, "topics": self.all_topics, "added_url": topic_url, "pages": pages}
		
	@falcon.after(render_template, "index.mako")
	def on_get_topic_page(self, req, resp, topic_url, page_number):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(page_number)
		topic = list(topics.filter(r.row["url"]["cze"] == topic_url).run(conn))[0]["topic"]["cze"]
		topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(conn))
		topic_url = "/tema/" + topic_url + "/"
		posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": topic_posts, "topics": self.all_topics, "added_url": topic_url, "pages": pages, "page": page_number}
		
	@falcon.after(render_template, "index.mako")
	def on_get_search(self, req, resp, searched_word):
		start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
		regex_word = rf"(?i){searched_word}" # for case insensitivity
		results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(conn))
		search_url = "/hledej/" + searched_word + "/"
		posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))	
		resp.body = {"posts": results, "topics": self.all_topics, "added_url": search_url, "pages": pages}
			
	@falcon.after(render_template, "index.mako")
	def on_get_search_page(self, req, resp, searched_word, page_number):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(page_number) # number one is here hardcoded, because index is always page one
		regex_word = rf"(?i){searched_word}" # for case insensitivity
		results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(conn))
		search_url = "/hledej/" + searched_word + "/"
		posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))		
		resp.body = {"posts": results, "topics": self.all_topics, "added_url": search_url, "pages": pages, "page": page_number}
	
	def on_post_search_form(self, req, resp):
		"""This method handles search form"""
		searched_word = req.get_param("search")
		new_url = falcon.uri.encode(f"/hledej/{searched_word}")
		raise falcon.HTTPSeeOther(new_url)
	
	@falcon.after(render_template, "post.mako")
	def on_get_view(self, req, resp, post_url):
		"""Handles requests (/post_url)"""
		try:
			post = list(posts.get_all(post_url, index="url_cze").run(conn))[0]
		except:
			raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
		post_comments = list(comments.filter(r.row["url"] == post_url).order_by(r.desc("when")).run(conn))
		resp.body = {"post": post, "topics": self.all_topics, "comments": post_comments}
	
	def on_post_view(self, req, resp, post_url):
		if req.get_param("antispam") == 5:
			comments.insert({
				"header": req.get_param("comment_header"),
				"nick": req.get_param("comment_nick"),
				"content": req.get_param("comment_content"),
				"when": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				"url": post_url }).run(conn)
			# now we need to update number of comments by the post
			post_id = list(posts.get_all(post_url, index="url_cze").run(conn))[0]["id"] # first to get id of post from url
			posts.get(post_id).update({"comments": r.row["comments"]+1}).run(conn) # then to increment number +1
			raise falcon.HTTPSeeOther(f"/{post_url}")
		else:
			raise falcon.HTTPForbidden(title="Neprošel jsi antipspamovou kontrolou.\n", description="Stiskni tlačítko ZPĚT a zkus to znovu.")
	
	@falcon.after(render_template, "new_post.mako")
	def on_get_new_post(self, req, resp):
		if req.get_cookie_values('cookie_uuid'):
			cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
			all_authors = list(authors.run(conn))
			for author in all_authors:
				if author["cookie"] == cookie_uuid:
					resp.body = {"topics": self.all_topics}
					break
			else:
				raise falcon.HTTPSeeOther("/login")
		else:
			raise falcon.HTTPSeeOther("/login")		

	def on_post_new_post(self, req, resp):
		if req.get_cookie_values('cookie_uuid'):
			cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
			all_authors = list(authors.run(conn))
			for author in all_authors:
				if author["cookie"] == cookie_uuid:
					post_topics = ""
					for key in req.params.keys():
						if not(key == "post_header" or key == "post_content"): # the rule is: if key is not post_header or post_content
							post_topics = post_topics + req.params[key] + ";"
					posts.insert({
					'comments': 0,
					'when': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
					'url': {"cze": create_url(req.get_param("post_header"))},
					'header': {"cze": req.get_param("post_header")}, 
					'content': {"cze": req.get_param("post_content")},
					'topics': {"cze": post_topics}
					}).run(conn)
					raise falcon.HTTPSeeOther("/")				
			else:
				raise falcon.HTTPSeeOther("/login")
		else:
			raise falcon.HTTPSeeOther("/login")

	@falcon.after(render_template, "login.mako")
	def on_get_login(self, req, resp):
		if req.get_cookie_values('cookie_uuid'):
			cookie_uuid = req.get_cookie_values('cookie_uuid')[0]
			all_authors = list(authors.run(conn))
			for author in all_authors:
				if author["cookie"] == cookie_uuid:
					raise falcon.HTTPSeeOther("/new_post")
			else:
				resp.body = {"topics": self.all_topics}
		else:
			resp.body = {"topics": self.all_topics}	
	def on_post_login(self, req, resp):
		all_authors = list(authors.run(conn))
		for author in all_authors:
			try:
				if self.ph.verify(author["login"], req.get_param("login")):
					if self.ph.verify(author["password"], req.get_param("password")):
						new_cookie = str(uuid4())
						authors.get(author["id"]).update({"cookie": new_cookie}).run(conn)
						resp.set_cookie('cookie_uuid', new_cookie, max_age=7200, secure=False)
						if self.ph.check_needs_rehash(author["login"]):
							authors.get(author["id"]).update({"login": self.ph.hash(req.get_param("login"))}).run(conn)
						if self.ph.check_needs_rehash(author["password"]):
							authors.get(author["id"]).update({"password": self.ph.hash(req.get_param("password"))}).run(conn)			
						raise falcon.HTTPSeeOther("/new_post")
			except argon2.exceptions.VerifyMismatchError:
				resp.status = falcon.HTTP_401
	
	def on_get_logout(self, req, resp):
		resp.unset_cookie('cookie_uuid')
		raise falcon.HTTPSeeOther("/")

# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML)
app.req_options.auto_parse_form_urlencoded = True
app.resp_options.secure_cookies_by_default = False
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)

# Resources are represented by long-lived class instances
easyblog = EasyBlog()
app.add_route('/', easyblog)
app.add_route('/page/{page_number:int}', easyblog, suffix="page")
app.add_route('/strana/{page_number:int}', easyblog, suffix="page")
app.add_route('/topic/{topic_url}', easyblog, suffix="topic")
app.add_route('/tema/{topic_url}', easyblog, suffix="topic")
app.add_route('/topic/{topic_url}/page/{page_number:int}', easyblog, suffix="topic_page")
app.add_route('/tema/{topic_url}/strana/{page_number:int}', easyblog, suffix="topic_page")
app.add_route('/search/', easyblog, suffix="search_form")
app.add_route('/hledej/', easyblog, suffix="search_form")
app.add_route('/search/{searched_word}', easyblog, suffix="search")
app.add_route('/hledej/{searched_word}', easyblog, suffix="search")
app.add_route('/search/{searched_word}/page/{page_number:int}', easyblog, suffix="search_page")
app.add_route('/hledej/{searched_word}/strana/{page_number:int}', easyblog, suffix="search_page")
app.add_route('/{post_url}', easyblog, suffix="view")
app.add_route('/new_post', easyblog, suffix="new_post")
app.add_route('/login', easyblog, suffix="login")
app.add_route('/logout', easyblog, suffix="logout")


#from hupper import start_reloader
from waitress import serve
#reloader = start_reloader("easyblog.app") #test
#reloader.watch_files(['settings.py', 'helpers.py', 'mako_imports/mako_imp.py'])
serve(app, host='127.0.0.1', port=8080)