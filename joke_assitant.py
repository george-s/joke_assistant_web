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

def CleanUpCheckBoxList(checkboxlist):
	cleanlist=[]
	for line in checkboxlist:
 		line = re.sub('[()]', '', line)
 		line = re.sub("u'", "", line)
 		line = re.sub('u"', '', line)
 		line = re.sub("'", "", line)
 		line = re.sub('"', '', line)
 		print line
 		# don't need dictionary necessarily
 		cleanlist.append(line)
	return cleanlist

def split_comma1(string):
	dave = string.split(",")[0]
	return dave

def split_comma2(string):
	barry = string.split(",")[1]
	return barry


app.jinja_env.filters['split_comma1'] = split_comma1
app.jinja_env.filters['split_comma2'] = split_comma2
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



# Get The Article Feed Object As list Handle the checkboxes array as list
@app.route('/feedlist', methods=['GET', 'POST'])
def feedlist():
	
	chosenfeed = eval(str(session['source'])+ "_feed")
	index_article_list = chosenfeed.articlesTitleLinkList()
	
	if request.method == "POST":
		if request.form.getlist("checkboxes"):
			cleanlist = CleanUpCheckBoxList(request.form.getlist("checkboxes"))
			session['shortlistitems'] = cleanlist
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


