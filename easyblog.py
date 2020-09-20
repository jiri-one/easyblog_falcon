import falcon
from math import ceil
from datetime import datetime
import argon2
from settings import posts_per_page, topics, posts, comments, authors, r
from helpers import file_path, render_template, slice_posts, create_url, Authorize, RethinkDBConnector, reorder_topics

class EasyBlog(object):
	@falcon.after(render_template, "index.mako")
	def on_get(self, req, resp):
		"""Handles GET requests on index (/)"""
		start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
		index_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(req.context.conn))
		posts_count = posts.count().run(req.context.conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))		
		resp.body = {"posts": index_posts, "pages": pages}
	
	@falcon.after(render_template, "index.mako")
	def on_get_page(self, req, resp, page_number):
		"""Handles GET requests on /page/{page_number} and /strana/{page_number}"""
		start, end = slice_posts(page_number)
		page_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(req.context.conn))
		posts_count = posts.count().run(req.context.conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": page_posts, "pages": pages, "page": page_number}
	
	@falcon.after(render_template, "index.mako")
	def on_get_topic(self, req, resp, topic_url):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(1) # number one is here hardcoded, because index of topic is always page one
		topic = list(topics.filter(r.row["url"]["cze"] == topic_url).run(req.context.conn))[0]["topic"]["cze"]
		topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(req.context.conn))
		topic_url = "/tema/" + topic_url + "/"
		posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(req.context.conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": topic_posts, "added_url": topic_url, "pages": pages}
		
	@falcon.after(render_template, "index.mako")
	def on_get_topic_page(self, req, resp, topic_url, page_number):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(page_number)
		topic = list(topics.filter(r.row["url"]["cze"] == topic_url).run(req.context.conn))[0]["topic"]["cze"]
		topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(req.context.conn))
		topic_url = "/tema/" + topic_url + "/"
		posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(req.context.conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))
		resp.body = {"posts": topic_posts, "added_url": topic_url, "pages": pages, "page": page_number}
		
	@falcon.after(render_template, "index.mako")
	def on_get_search(self, req, resp, searched_word):
		start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
		regex_word = rf"(?i){searched_word}" # for case insensitivity
		results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(req.context.conn))
		search_url = "/hledej/" + searched_word + "/"
		posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(req.context.conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))	
		resp.body = {"posts": results, "added_url": search_url, "pages": pages}
			
	@falcon.after(render_template, "index.mako")
	def on_get_search_page(self, req, resp, searched_word, page_number):
		"""Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
		start, end = slice_posts(page_number) # number one is here hardcoded, because search index is always page one
		regex_word = rf"(?i){searched_word}" # for case insensitivity
		results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(req.context.conn))
		search_url = "/hledej/" + searched_word + "/"
		posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(req.context.conn)
		page_count = ceil(posts_count / posts_per_page)
		pages = list(range(1,page_count+1))		
		resp.body = {"posts": results, "added_url": search_url, "pages": pages, "page": page_number}
	
	def on_post_search_form(self, req, resp):
		"""This method handles search form"""
		searched_word = req.get_param("search")
		new_url = falcon.uri.encode(f"/hledej/{searched_word}")
		raise falcon.HTTPSeeOther(new_url)
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "post.mako")
	def on_get_view(self, req, resp, post_url):
		"""Handles requests (/post_url)"""
		try:
			post = list(posts.get_all(post_url, index="url_cze").run(req.context.conn))[0]
		except:
			raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
		post_comments = list(comments.filter(r.row["url"] == post_url).order_by(r.desc("when")).run(req.context.conn))
		resp.body = {"post": post, "comments": post_comments, "authorized": resp.context.authorized}
	
	def on_post_view(self, req, resp, post_url):
		if req.get_param_as_int("antispam") == 5:
			comments.insert({
				"header": req.get_param("comment_header"),
				"nick": req.get_param("comment_nick"),
				"content": req.get_param("comment_content"),
				"when": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
				"url": post_url }).run(req.context.conn) # here is problem with later multilanguage version!
			# now we need to update number of comments by the post
			post_id = list(posts.get_all(post_url, index="url_cze").run(req.context.conn))[0]["id"] # first to get id of post from url
			posts.get(post_id).update({"comments": r.row["comments"]+1}).run(req.context.conn) # then to increment number +1
			raise falcon.HTTPSeeOther(f"/{post_url}")
		else:
			raise falcon.HTTPForbidden(title="Neprošel jsi antipspamovou kontrolou.\n", description="Stiskni tlačítko ZPĚT a zkus to znovu.")
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "new_post.mako")
	def on_get_new_post(self, req, resp):
		if resp.context.authorized == 1:
			resp.body = {}
		else:
			raise falcon.HTTPSeeOther("/login")		

	@falcon.before(Authorize())
	def on_post_new_post(self, req, resp):
		if resp.context.authorized == 1:
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
			}).run(req.context.conn)
			raise falcon.HTTPSeeOther("/")			
		else:
			raise falcon.HTTPSeeOther("/login")			

	@falcon.before(Authorize())
	@falcon.after(render_template, "login.mako")
	def on_get_login(self, req, resp):
		if resp.context.authorized == 1:
			raise falcon.HTTPSeeOther("/new_post")
		else:
			resp.body = {}

	def on_post_login(self, req, resp):
		ph = argon2.PasswordHasher()
		for author in list(authors.run(req.context.conn)):
			try:
				if ph.verify(author["login"], req.get_param("login")):
					if ph.verify(author["password"], req.get_param("password")):
						new_cookie = r.uuid().run(req.context.conn)
						authors.get(author["id"]).update({"cookie": new_cookie}).run(req.context.conn)
						resp.set_cookie('cookie_uuid', new_cookie, max_age=72000, secure=False)
						if ph.check_needs_rehash(author["login"]):
							authors.get(author["id"]).update({"login": ph.hash(req.get_param("login"))}).run(req.context.conn)
						if ph.check_needs_rehash(author["password"]):
							authors.get(author["id"]).update({"password": ph.hash(req.get_param("password"))}).run(req.context.conn)			
						raise falcon.HTTPSeeOther("/new_post")
			except argon2.exceptions.VerifyMismatchError:
				resp.status = falcon.HTTP_401
	
	def on_get_logout(self, req, resp):
		resp.unset_cookie('cookie_uuid')
		raise falcon.HTTPSeeOther("/")
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "delete.mako")	
	def on_get_delete(self, req, resp, post_url):
		"""Handles requests (/delete/post_url)"""
		if resp.context.authorized == 1:
			try:
				post = list(posts.get_all(post_url, index="url_cze").run(req.context.conn))[0]
			except:
				raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
			post_comments = list(comments.filter(r.row["url"] == post_url).order_by(r.desc("when")).run(req.context.conn))
			resp.body = {"post": post, "comments": post_comments}
			if req.get_param("delete") is not None:
				if req.get_param("delete") == "Ano" or req.get_param("delete") == "Yes":
					posts.get_all(post_url, index="url_cze").delete().run(req.context.conn)
					comments.filter(r.row["url"] == post_url).delete().run(req.context.conn)
					raise falcon.HTTPSeeOther("/")
				else:
					raise falcon.HTTPSeeOther(f"/{post_url}")
		else:
			raise falcon.HTTPSeeOther(f"/{post_url}")			
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "edit.mako")
	def on_get_edit(self, req, resp, post_url):
		"""Handles requests (/edit/post_url)"""
		if resp.context.authorized == 1:
			try:
				post = list(posts.get_all(post_url, index="url_cze").run(req.context.conn))[0]
			except:
				raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
			resp.body = {"post": post}
		else:
			raise falcon.HTTPSeeOther("/login")		
	
	@falcon.before(Authorize())
	def on_post_edit(self, req, resp, post_url):
		"""Handles requests (/edit/post_url)"""
		if resp.context.authorized == 1:
			post_topics = ""
			for key in req.params.keys():
				if not(key == "post_header" or key == "post_content" or key == "post_url"): # the rule is: if key is not post_header or post_content or post_url
					post_topics = post_topics + req.params[key] + ";"
			posts.get_all(post_url, index="url_cze").update({
				'url': {"cze": req.get_param("post_url")},
				'header': {"cze": req.get_param("post_header")}, 
				'content': {"cze": req.get_param("post_content")},
				'topics': {"cze": post_topics}				
			}).run(req.context.conn)
			comments.filter(r.row["url"] == post_url).update({"url": req.get_param("post_url")}).run(req.context.conn)
			raise falcon.HTTPSeeOther(f"""/{req.get_param("post_url")}""")
		else:
			raise falcon.HTTPSeeOther("/login")
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "delete_comment.mako")
	def on_get_delete_comment(self, req, resp, comment_id):
		"""Handles requests (/delete_comment/comment_id)"""
		if resp.context.authorized == 1:
			comment = comments.get(comment_id).run(req.context.conn)
			if comment is not None:
				resp.body = {"comment": comment}
				if req.get_param("delete") is not None:
					if req.get_param("delete") == "Ano" or req.get_param("delete") == "Yes":
						comments.get(comment_id).delete().run(req.context.conn)
						post_id = list(posts.get_all(comment["url"], index="url_cze").run(req.context.conn))[0]["id"] # first to get id of post from url
						posts.get(post_id).update({"comments": r.row["comments"]-1}).run(req.context.conn) # then to reduct number -1					
						raise falcon.HTTPSeeOther(f"""/{comment["url"]}""")
					else:
						raise falcon.HTTPSeeOther(f"""/{comment["url"]}""")
			else:
				raise falcon.HTTPNotFound(title="Non-existent comment.\n", description="Please use only adresses from website.")	
		else:
			raise falcon.HTTPSeeOther("/login")
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "topics_admin.mako")
	def on_get_topics_admin(self, req, resp):
		if resp.context.authorized == 1:
			resp.body = {}
		else:
			raise falcon.HTTPSeeOther("/login")
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "delete_topic.mako")
	def on_get_delete_topic(self, req, resp, topic_id):
		if resp.context.authorized == 1:
			topic = topics.get(topic_id).run(req.context.conn)
			if topic is not None:
				posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic["topic"]["cze"])).count().run(req.context.conn)
				if posts_count > 0:
					topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic["topic"]["cze"])).run(req.context.conn))
					for post in topic_posts:
						splited_topics = list(filter(None, post["topics"]["cze"].split(";")))
						if len(splited_topics) == 1:
							delete_allowed = False
							break
					else:
						delete_allowed = True
				else:
					delete_allowed = True
			else:
				raise falcon.HTTPNotFound(title="Non-existent topic.\n", description="Please use only adresses from website.")	
			resp.body = {"topic": topic, "posts_count": posts_count, "delete_allowed": delete_allowed}
			if req.get_param("delete") is not None and delete_allowed == True:
				if req.get_param("delete") == "Ano" or req.get_param("delete") == "Yes":
					if posts_count > 0: # if are some posts on this topic, then we need delete this topic from that posts 
						for post in topic_posts:
							splited_topics = list(filter(None, post["topics"]["cze"].split(";")))
							splited_topics.remove(topic["topic"]["cze"])
							merged_topics = ";".join(splited_topics) + ";"
							posts.get_all(post["url"]["cze"], index="url_cze").update({
								'topics': {"cze": merged_topics}				
							}).run(req.context.conn)
					topics.get(topic_id).delete().run(req.context.conn)
					#then I need to refresh topics order numbers
					reorder_topics(topics, req)
					raise falcon.HTTPSeeOther("/topics_admin")
				else:
					raise falcon.HTTPSeeOther("/topics_admin")
			elif req.get_param("delete") is not None and delete_allowed == False:
				# this is here, because I can click to No or anything and I will be back on topics_admin
				raise falcon.HTTPSeeOther("/topics_admin")
		else:
			raise falcon.HTTPSeeOther("/login")

	@falcon.before(Authorize())
	@falcon.after(render_template, "new_topic.mako")	
	def on_get_new_topic(self, req, resp):
		if resp.context.authorized == 1:
			resp.body = {}
		else:
			raise falcon.HTTPSeeOther("/login")
	
	@falcon.before(Authorize())
	def on_post_new_topic(self, req, resp):
		if resp.context.authorized == 1:
			topics.insert({
				'order': req.get_param_as_float("order"), # you can choose decimal number for order
				'topic': {"cze": req.get_param("topic_cze"),
						  "eng": req.get_param("topic_eng")},
				'url': {"cze": req.get_param("url_cze"),
						"eng": req.get_param("url_eng")},
				'description': {"cze": req.get_param("description_cze"),
								"eng": req.get_param("description_eng")},
			}).run(req.context.conn)			
			reorder_topics(topics, req)
			raise falcon.HTTPSeeOther("/topics_admin")
		else:
			raise falcon.HTTPSeeOther("/login")
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "edit_topic.mako")			
	def on_get_edit_topic(self, req, resp, topic_id):
		if resp.context.authorized == 1:
			topic = topics.get(topic_id).run(req.context.conn)
			if topic is not None:
				resp.body = {"topic": topic}
			else:
				raise falcon.HTTPNotFound(title="Non-existent topic.\n", description="Please use only adresses from website.")
		else:
			raise falcon.HTTPSeeOther("/login")		
	
	@falcon.before(Authorize())
	def on_post_edit_topic(self, req, resp, topic_id):
		if resp.context.authorized == 1:
			old_topic_name = topics.get(topic_id).run(req.context.conn)["topic"]["cze"]
			topics.get(topic_id).update({
				'order': req.get_param_as_float("order"),
				'topic': {"cze": req.get_param("topic_cze"),
						  "eng": req.get_param("topic_eng")},
				'url': {"cze": req.get_param("url_cze"),
						"eng": req.get_param("url_eng")},
				'description': {"cze": req.get_param("description_cze"),
								"eng": req.get_param("description_eng")}
			}).run(req.context.conn)
			posts_count = posts.filter(lambda post: post["topics"]["cze"].match(old_topic_name)).count().run(req.context.conn)
			if posts_count > 0:
				topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(old_topic_name)).run(req.context.conn))				
				for post in topic_posts:
					splited_topics = list(filter(None, post["topics"]["cze"].split(";")))
					splited_topics.remove(old_topic_name)
					splited_topics.append(req.get_param("topic_cze"))
					merged_topics = ";".join(splited_topics) + ";"
					posts.get_all(post["url"]["cze"], index="url_cze").update({'topics': {"cze": merged_topics}}).run(req.context.conn)
			reorder_topics(topics, req)
			raise falcon.HTTPSeeOther("/topics_admin")
		else:
			raise falcon.HTTPSeeOther("/login")
	
	@falcon.before(Authorize())
	@falcon.after(render_template, "admin.mako")			
	def on_get_admin(self, req, resp):
		if resp.context.authorized == 1:
			resp.body = {}
		else:
			raise falcon.HTTPSeeOther("/login")		
		

# falcon.API instances are callable WSGI apps
app = falcon.API(media_type=falcon.MEDIA_HTML, middleware=RethinkDBConnector())
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
app.add_route('/delete/{post_url}', easyblog, suffix="delete")
app.add_route('/edit/{post_url}', easyblog, suffix="edit")
app.add_route('/delete_comment/{comment_id}', easyblog, suffix="delete_comment")
app.add_route('/topics_admin', easyblog, suffix="topics_admin")
app.add_route('/delete_topic/{topic_id}', easyblog, suffix="delete_topic")
app.add_route('/new_topic', easyblog, suffix="new_topic")
app.add_route('/edit_topic/{topic_id}', easyblog, suffix="edit_topic")
app.add_route('/admin', easyblog, suffix="admin")


if __name__ == "__main__":
	#from hupper import start_reloader
	from waitress import serve
	#reloader = start_reloader("easyblog.app") #test
	#reloader.watch_files(['settings.py', 'helpers.py', 'mako_imports/mako_imp.py'])
	serve(app, host='0.0.0.0', port=8080)