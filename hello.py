# We'll need the session object to manage session variables
# render_template to render html content from templates
# url_for to extract the url for a given view/route
# request to access the GET data request for the form view
# redirect to perform redirects to different routes
import sys
sys.path.append('/disk1/playpen/dev/joke_assistant/')
from flask import Flask, session, render_template, url_for, request, redirect
from  JA_Classes import ArticleFeed, ArticleShortList, Draft, Joke

app = Flask("__name__",  static_folder = "images")
print app
app.debug = True
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# def sumSessionCounter():
#   try:
#     session['counter'] += 1
#   except KeyError:
#     session['counter'] = 1


# @app.route('/')
# def index():
# 	name = "fred"
# 	return render_template('index.html', name=name)

bbc_feed = ArticleFeed('bbc', "bbc.png", 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk')
dailymail_feed = ArticleFeed('dailymail', "dailymail.jpeg", 'http://www.dailymail.co.uk/news/index.rss')
fox_feed = ArticleFeed('fox', "fox.png", 'http://feeds.foxnews.com/foxnews/latest')

@app.route('/')
def sourceSelector():
 	name = "fred"
 	if request.args.get('articleSource'):
 		session['source'] = request.args.get('articleSource')
 		return redirect(url_for('shortlist'))
 	else:
 		return render_template('sourceSelector.html', session=session)


@app.route('/user/<name>')
def user(name):
	return render_template('hello.html', name=name)

@app.route('/feedlist')
def shortlist():
	list_id="123"
	chosenfeed = eval(str(session['source'])+ "_feed")
	index_article_list = chosenfeed.articlesTitleLinkList()
	return render_template('feedlist.html', list_id=list_id, index_article_list=index_article_list)

@app.route('/joke/<jokename>')
def joke(jokename):
	return render_template('joke.html', jokename=jokename)

@app.route('/form')
def form():
  #sumSessionCounter()
  # if a name has been sent, store it on a session variable
  if request.args.get('yourname'):
    session['name'] = request.args.get('yourname')
    # And then redirect the user to the main page
    return redirect(url_for('sourceSelector'))
  else:
    # If no name has been sent, show the form
    return render_template('form.html', session=session)


if __name__ == '__main__':
    app.run()


