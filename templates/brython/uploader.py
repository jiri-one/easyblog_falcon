from browser import document, ajax

def on_complete(req):
	if req.status == 200 or req.status == 0:
		document["results"].html = req.text
	else:
		document["results"].html = "There is some error: " + req.text

def ajax_post(button_search):
	document["results"].html = "Loading..."
	ajax.post("/searchengine",
			  headers={"Content-Type": "application/x-www-form-urlencoded"},
			  data={"language": document["language"].value,
					"searched_text": document["searched_text"].value,
					"fulltext": document["fulltext"].checked
					},
			  oncomplete=on_complete)

def hit_enter(ev):
	if ev.keyCode == 13:
		ajax_post(None)
		
document["button_search"].bind("click", ajax_post)
document["searched_text"].bind("keypress", hit_enter)