import falcon
from math import ceil
from datetime import datetime
import argon2
from settings import posts_per_page, topics, posts, comments, authors, drafts, r
from helpers import file_path, render_template, slice_posts, create_url, Authorize, RethinkDBConnector, reorder_topics

class EasyBlog(object):
    @falcon.after(render_template, "index.mako")
    def on_get(self, req, resp):
        """Handles GET requests on index (/)"""
        start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
        index_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # get index post (page 1) from RethinkDB
        posts_count = posts.count().run(req.context.conn) # get number of all posts
        page_count = ceil(posts_count / posts_per_page) # get number of pages
        pages = list(range(1,page_count+1))	# list of all pages
        resp.text = {"posts": index_posts, "pages": pages} # sending data to make tepmplate in resp.text

    @falcon.after(render_template, "index.mako")
    def on_get_page(self, req, resp, page_number):
        """Handles GET requests on /page/{page_number} and /strana/{page_number}"""
        start, end = slice_posts(page_number) # page number is parameter from web adress
        page_posts = list(posts.order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # get all page posts from RethinkDB ordered by post time
        posts_count = posts.count().run(req.context.conn) # get number of all posts
        page_count = ceil(posts_count / posts_per_page) # get number of pages
        pages = list(range(1,page_count+1)) # list of all pages
        resp.text = {"posts": page_posts, "pages": pages, "page": page_number} # sending data to make tepmplate in resp.text

    @falcon.after(render_template, "index.mako")
    def on_get_topic(self, req, resp, topic_url):
        """Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
        start, end = slice_posts(1) # number one is here hardcoded, because index of topic is always page one
        topic = list(topics.filter(r.row["url"]["cze"] == topic_url).run(req.context.conn))[0]["topic"]["cze"] # in topic is after this questin just topic name (string), obtained from topic_url
        topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # list of all posts which included topic from previous row
        topic_url = "/tema/" + topic_url + "/" # make topic_url complete - its used in teplate in added_url and that is used fot topics, search, ...
        posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(req.context.conn) # number of posts from topic
        page_count = ceil(posts_count / posts_per_page) # get number of pages from the current topic
        pages = list(range(1,page_count+1)) # list of all pages from the current topic
        resp.text = {"posts": topic_posts, "added_url": topic_url, "pages": pages} # sending data to make tepmplate in resp.text

    @falcon.after(render_template, "index.mako")
    def on_get_topic_page(self, req, resp, topic_url, page_number):
        """Handles GET requests on /topic/{topic_url} and /tema/{topic_url}"""
        start, end = slice_posts(page_number) # get page number a returns two numbers for slice posts
        topic = list(topics.filter(r.row["url"]["cze"] == topic_url).run(req.context.conn))[0]["topic"]["cze"] # in topic is after this questin just topic name (string), obtained from topic_url
        topic_posts = list(posts.filter(lambda post: post["topics"]["cze"].match(topic)).order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # list of all posts which included topic from previous row
        topic_url = "/tema/" + topic_url + "/" # make topic_url complete - its used in teplate in added_url and that is used fot topics, search, ...
        posts_count = posts.filter(lambda post: post["topics"]["cze"].match(topic)).count().run(req.context.conn)
        page_count = ceil(posts_count / posts_per_page) # get number of pages from the current topic
        pages = list(range(1,page_count+1)) # list of all pages from the current topic
        resp.text = {"posts": topic_posts, "added_url": topic_url, "pages": pages, "page": page_number} # sending data to make tepmplate in resp.text

    @falcon.after(render_template, "index.mako")
    def on_get_search(self, req, resp, searched_word):
        """Handles GET requests on /search/{searched_word} and /hledej/{searched_word}"""
        start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
        regex_word = rf"(?i){searched_word}" # for case insensitivity
        results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(req.context.conn))
        search_url = "/hledej/" + searched_word + "/"
        posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(req.context.conn)
        page_count = ceil(posts_count / posts_per_page)
        pages = list(range(1,page_count+1))	
        resp.text = {"posts": results, "added_url": search_url, "pages": pages} # sending data to make tepmplate in resp.text

    @falcon.after(render_template, "index.mako")
    def on_get_search_page(self, req, resp, searched_word, page_number):
        """Handles GET requests on /search/searched_word/{page_number} and /hledej/searched_word/{page_number}"""
        start, end = slice_posts(page_number) # get page number a returns two numbers for slice posts
        regex_word = rf"(?i){searched_word}" # for case insensitivity
        results = list(posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).slice(start, end).run(req.context.conn))
        search_url = "/hledej/" + searched_word + "/"
        posts_count = posts.filter(lambda post: (post["content"]["cze"].match(regex_word)) or (post["header"]["cze"].match(regex_word))).order_by(r.desc("when")).count().run(req.context.conn)
        page_count = ceil(posts_count / posts_per_page)
        pages = list(range(1,page_count+1))		
        resp.text = {"posts": results, "added_url": search_url, "pages": pages, "page": page_number} # sending data to make tepmplate in resp.text

    def on_post_search_form(self, req, resp):
        """This method handles search form"""
        searched_word = req.get_param("search")
        new_url = falcon.uri.encode(f"/hledej/{searched_word}")
        raise falcon.HTTPSeeOther(new_url)

    @falcon.before(Authorize(only_admin=0))
    @falcon.after(render_template, "post.mako")
    def on_get_view(self, req, resp, post_url):
        """Handles requests (/post_url)"""
        try:
            post = list(posts.get_all(post_url, index="url_cze").run(req.context.conn))[0]
        except IndexError:
            raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
        post_comments = list(comments.filter(r.row["url"] == post_url).order_by(r.desc("when")).run(req.context.conn))
        resp.text = {"post": post, "comments": post_comments, "authorized": resp.context.authorized} # sending data to make tepmplate in resp.text

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
            resp.text = {}

    @falcon.before(Authorize())
    def on_post_new_post(self, req, resp):
        if resp.context.authorized == 1:
            post_topics = ""
            for key in req.params.keys():
                if "topic_" in key:
                    post_topics += req.params[key] + ";"
            dict_to_rethinkdb = {
                'comments': 0,
                'when': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'url': {"cze": create_url(req.get_param("post_header"))},
                'header': {"cze": req.get_param("post_header")},
                'content': {"cze": req.get_param("post_content")},
                'topics': {"cze": post_topics}
                }
            if req.get_param("draft") != None:
                drafts.insert(dict_to_rethinkdb).run(req.context.conn)
                redirect_to = "/drafts"
            else: # req.get_param("public") != None
                posts.insert(dict_to_rethinkdb).run(req.context.conn)
                redirect_to = "/"
            raise falcon.HTTPSeeOther(redirect_to)

    @falcon.before(Authorize(only_admin=0))
    @falcon.after(render_template, "login.mako")
    def on_get_login(self, req, resp):
        if resp.context.authorized == 1:
            if req.get_cookie_values('redir_from'):
                redirecting_address = req.get_cookie_values('redir_from')[0]
                resp.unset_cookie('redir_from')
                raise falcon.HTTPSeeOther(redirecting_address) 
            else:
                resp.unset_cookie('redir_from')
                raise falcon.HTTPSeeOther("/admin")
        else:
            resp.text = {}

    def on_post_login(self, req, resp):
        ph = argon2.PasswordHasher()
        for author in list(authors.run(req.context.conn)):
            try:
                if ph.verify(author["login"], req.get_param("login")):
                    if ph.verify(author["password"], req.get_param("password")):
                        new_cookie = r.uuid().run(req.context.conn)
                        authors.get(author["id"]).update({"cookie": new_cookie}).run(req.context.conn)
                        resp.set_cookie('cookie_uuid', new_cookie, max_age=72000, secure=True)
                        if ph.check_needs_rehash(author["login"]):
                            authors.get(author["id"]).update({"login": ph.hash(req.get_param("login"))}).run(req.context.conn)
                        if ph.check_needs_rehash(author["password"]):
                            authors.get(author["id"]).update({"password": ph.hash(req.get_param("password"))}).run(req.context.conn)
                        
                        redirecting_address = req.get_cookie_values('redir_from')
                        if redirecting_address:
                            resp.unset_cookie('redir_from')
                            raise falcon.HTTPSeeOther(redirecting_address[0])
                        else:
                            raise falcon.HTTPSeeOther("/admin")
            except argon2.exceptions.VerifyMismatchError:
                raise falcon.HTTPUnauthorized(title="Bad login or password! (Špatné jméno nebo heslo!)")

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
            except IndexError:
                raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
            post_comments = list(comments.filter(r.row["url"] == post_url).order_by(r.desc("when")).run(req.context.conn))
            resp.text = {"post": post, "comments": post_comments}
            if req.get_param("delete") is not None:
                if req.get_param("delete") == "Ano" or req.get_param("delete") == "Yes":
                    posts.get_all(post_url, index="url_cze").delete().run(req.context.conn)
                    comments.filter(r.row["url"] == post_url).delete().run(req.context.conn)
                    raise falcon.HTTPSeeOther("/")
                else:
                    raise falcon.HTTPSeeOther(f"/{post_url}")

    @falcon.before(Authorize())
    @falcon.after(render_template, "edit.mako")
    def on_get_edit(self, req, resp, post_url):
        """Handles requests (/edit/post_url)"""
        if resp.context.authorized == 1:
            try:
                post = list(posts.get_all(post_url, index="url_cze").run(req.context.conn))[0]
            except IndexError:
                raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
            resp.text = {"post": post}

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

    @falcon.before(Authorize())
    @falcon.after(render_template, "delete_comment.mako")
    def on_get_delete_comment(self, req, resp, comment_id):
        """Handles requests (/delete_comment/comment_id)"""
        if resp.context.authorized == 1:
            comment = comments.get(comment_id).run(req.context.conn)
            if comment is not None:
                resp.text = {"comment": comment}
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

    @falcon.before(Authorize())
    @falcon.after(render_template, "topics_admin.mako")
    def on_get_topics_admin(self, req, resp):
        if resp.context.authorized == 1:
            resp.text = {}

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
            resp.text = {"topic": topic, "posts_count": posts_count, "delete_allowed": delete_allowed}
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

    @falcon.before(Authorize())
    @falcon.after(render_template, "new_topic.mako")	
    def on_get_new_topic(self, req, resp):
        if resp.context.authorized == 1:
            resp.text = {}

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

    @falcon.before(Authorize())
    @falcon.after(render_template, "edit_topic.mako")			
    def on_get_edit_topic(self, req, resp, topic_id):
        if resp.context.authorized == 1:
            topic = topics.get(topic_id).run(req.context.conn)
            if topic is not None:
                resp.text = {"topic": topic}
            else:
                raise falcon.HTTPNotFound(title="Non-existent topic.\n", description="Please use only adresses from website.")

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

    @falcon.before(Authorize())
    @falcon.after(render_template, "admin.mako")			
    def on_get_admin(self, req, resp):
        if resp.context.authorized == 1:
            resp.text = {}
    
    @falcon.before(Authorize())
    @falcon.after(render_template, "drafts.mako")
    def on_get_drafts(self, req, resp):
        """Handles GET requests on /drafts"""
        if resp.context.authorized == 1:
            start, end = slice_posts(1) # number one is here hardcoded, because index is always page one
            index_posts = list(drafts.order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # get index post (page 1) from RethinkDB
            posts_count = drafts.count().run(req.context.conn) # get number of all posts
            page_count = ceil(posts_count / posts_per_page) # get number of pages
            pages = list(range(1,page_count+1))	# list of all pages
            resp.text = {"posts": index_posts, "added_url": "/drafts/", "pages": pages} # sending data to make tepmplate in resp.text

    @falcon.before(Authorize())
    @falcon.after(render_template, "index.mako")
    def on_get_drafts_page(self, req, resp, page_number):
        """Handles GET requests on /drafts/page/{page_number} and /drafts/strana/{page_number}"""
        if resp.context.authorized == 1:
            start, end = slice_posts(page_number) # page number is parameter from web adress
            page_posts = list(drafts.order_by(r.desc("when")).slice(start, end).run(req.context.conn)) # get all page posts from RethinkDB ordered by post time
            posts_count = drafts.count().run(req.context.conn) # get number of all posts
            page_count = ceil(posts_count / posts_per_page) # get number of pages
            pages = list(range(1,page_count+1)) # list of all pages
            resp.text = {"posts": page_posts, "added_url": "/drafts/", "pages": pages, "page": page_number} # sending data to make tepmplate in resp.text

    @falcon.before(Authorize())
    @falcon.after(render_template, "edit.mako")
    def on_get_edit_draft(self, req, resp, post_url):
        """Handles requests (/edit_draft/post_url)"""
        if resp.context.authorized == 1:
            try:
                post = list(drafts.filter(r.row["url"]["cze"] == post_url).run(req.context.conn))[0]
            except IndexError:
                raise falcon.HTTPNotFound(title="Non-existent address.\n", description="Please use only adresses from website.")
            resp.text = {"post": post, "added_url": "/draft_edit"}

    @falcon.before(Authorize())
    def on_post_edit_draft(self, req, resp, post_url):
        """Handles requests (/edit_draft/post_url)"""
        if resp.context.authorized == 1:
            post_topics = ""
            for key in req.params.keys():
                if "topic_" in key:
                    post_topics += req.params[key] + ";"
            dict_to_rethinkdb = {
                'comments': 0,
                'when': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'url': {"cze": create_url(req.get_param("post_header"))},
                'header': {"cze": req.get_param("post_header")},
                'content': {"cze": req.get_param("post_content")},
                'topics': {"cze": post_topics}
                }
            if req.get_param("draft") != None:
                drafts.filter(r.row["url"]["cze"] == post_url).update(dict_to_rethinkdb).run(req.context.conn)
                redirect_to = "/drafts"
            else: # req.get_param("public") != None
                posts.insert(dict_to_rethinkdb).run(req.context.conn)
                drafts.filter(r.row["url"]["cze"] == post_url).delete().run(req.context.conn)
                redirect_to = "/"
            raise falcon.HTTPSeeOther(redirect_to)        
        
    @falcon.before(Authorize())
    @falcon.after(render_template, "upload.mako")
    def on_get_upload(self, req, resp):
        """Handles GET requests (/upload)"""
        if resp.context.authorized == 1:
            resp.text = {}
   
    @falcon.before(Authorize())
    @falcon.after(render_template, "upload.mako")
    def on_post_upload(self, req, resp):
        """Handles POST requests (/upload)"""
        if resp.context.authorized == 1:
            form = req.get_media()
            for part in form:
                if part.name == 'filename':
                    with open(f"files/{part.filename}", "wb") as dest:
                        while True:
                            chunk = part.stream.read(4096)
                            if not chunk:
                                break
                            dest.write(chunk)
                resp.text = {"link": part.filename}

# falcon.API instances are callable WSGI apps
# everything is HTML and I am using my own middleware for connecting to rethinkdb in every request/response
app = falcon.App(media_type=falcon.MEDIA_HTML, middleware=RethinkDBConnector())
app.req_options.auto_parse_form_urlencoded = True # that needed because of forms
app.add_static_route("/templates", file_path("templates"), downloadable=True, fallback_filename=None)
app.add_static_route("/files", file_path("files"), downloadable=True, fallback_filename=None)


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
app.add_route('/drafts', easyblog, suffix="drafts")
app.add_route('/drafts/page/{page_number:int}', easyblog, suffix="drafts_page")
app.add_route('/drafts/strana/{page_number:int}', easyblog, suffix="drafts_page")
app.add_route('/edit_draft/{post_url}', easyblog, suffix="edit_draft")
app.add_route('/upload', easyblog, suffix="upload")


# the rest of code is not needed for server purposes
def local_run():
    """This is only helper function to run EasyBlog localy with hupper reloader"""
    from hupper import start_reloader
    from waitress import serve
    #app.resp_options.secure_cookies_by_default = False
    reloader = start_reloader('easyblog.local_run')
    # monitor an extra file
    #reloader.watch_files(['foo.ini'])
    serve(app, host='0.0.0.0', port=8000)

if __name__ == "__main__":
    local_run()
