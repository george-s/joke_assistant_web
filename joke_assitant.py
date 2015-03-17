# We'll need the session object to manage session variables
# render_template to render html content from templates
# url_for to extract the url for a given view/route
# request to access the GET data request for the form view
# redirect to perform redirects to different routes
import sys
sys.path.append('/disk1/playpen/dev/joke_assistant/')
from flask import Flask, session, render_template, url_for, request, redirect
from  JA_Classes import ArticleFeed, ArticleShortList, Draft, Joke
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
import re

app = Flask("__name__",  static_folder = "images")
print app
app.debug = True
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


bbc_feed = ArticleFeed('bbc', "bbc.png", 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk')
dailymail_feed = ArticleFeed('dailymail', "dailymail.jpeg", 'http://www.dailymail.co.uk/news/index.rss')
fox_feed = ArticleFeed('fox', "fox.png", 'http://feeds.foxnews.com/foxnews/latest')



def CheckBoxListToDictList(checkboxlist):
	cleanlist=[]
	for line in checkboxlist:
 		line = re.sub('[()]', '', line)
 		line = re.sub("u'", "", line)
 		line = re.sub('u"', '', line)
 		line = re.sub("'", "", line)
 		line = re.sub('"', '', line)
 		dave = line.split(",")[0]
 		barry = line.split(",")[1]
 		print "dave " + dave
 		print "barry " + barry
 		dicti = {dave.encode('utf8') : barry.encode('utf8')}
 		print line
 		print dicti
 		cleanlist.append(dicti)
	return cleanlist


def collectOnlyNew(master, new):
	additions = []
	for a in new:
		if a not in master:
			additions.append(a)
			master.append(a)
		if len(additions) > 0:
			for i in additions:
				print str(i.values()) + " added to shortlist"
		else:
			print "no new items to add"
	return master



def deDictUni(something):
	something = str(something).strip('[]').strip("'").strip("u'")
	return something


app.jinja_env.filters['deDictUni'] = deDictUni
#app.jinja_env.globals.update(deDict=deDict)
@app.route('/')
def sourceSelector():
 	name = "fred"
 	if request.args.get('articleSource'):
 		session['source'] = request.args.get('articleSource')
 		return redirect(url_for('feedlist'))
 	else:
 		return render_template('sourceSelector.html', session=session)



@app.route('/user/<name>')
def user(name):
	return render_template('hello.html', name=name)

@app.route('/joke/<jokename>')
def joke(jokename):
	return render_template('joke.html', jokename=jokename)

@app.route('/clear')
def clear():
	session.clear()
	return redirect(url_for('sourceSelector'))

# Get The Article Feed Object As list Handle the checkboxes array as list of Dicts
@app.route('/feedlist', methods=['GET', 'POST'])
def feedlist():
	
	chosenfeed = eval(str(session['source'])+ "_feed")
	index_article_list = chosenfeed.articlesTitleLinkList()
	
	if request.method == "POST":
		if request.form.getlist("checkboxes"):
			if not session.get('shortlistitems'):
				cleanlist = CheckBoxListToDictList(request.form.getlist("checkboxes"))
				print "No Session - starting fresh on"
				session['shortlistitems'] = cleanlist
			else:
				cleanlist = CheckBoxListToDictList(request.form.getlist("checkboxes"))
				session['shortlistitems'] = collectOnlyNew(session['shortlistitems'], cleanlist) 
				print "woooo Sessions exist"
		return redirect(url_for('shortlist'))
	else:
		return render_template('feedlist.html', index_article_list=index_article_list, session=session)



@app.route('/shortlist')
def shortlist():
	return render_template('shortlist.html')

# if a name has been sent, store it in a session variable
# And then redirect the user to the main page
# If no name has been sent, show the form again

@app.route('/name_form')
def name_form():

  if request.args.get('yourname'):
    session['name'] = request.args.get('yourname')
    return redirect(url_for('sourceSelector'))
  else:
    return render_template('name_form.html', session=session)



if __name__ == '__main__':
    app.run()


