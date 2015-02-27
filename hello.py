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


bbc_feed = ArticleFeed('bbc', "bbc.png", 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk')
dailymail_feed = ArticleFeed('dailymail', "dailymail.jpeg", 'http://www.dailymail.co.uk/news/index.rss')
fox_feed = ArticleFeed('fox', "fox.png", 'http://feeds.foxnews.com/foxnews/latest')

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

@app.route('/feedlist', methods=['GET', 'POST'])
def feedlist():
	list_id = "123"
	# Get The Article Feed Object As list
	chosenfeed = eval(str(session['source'])+ "_feed")
	index_article_list = chosenfeed.articlesTitleLinkList()
	# Handle the checkboxes array
	if request.method == "POST":
		if request.form.getlist("checkboxes"):
			session['shortlistitems'] = request.form.getlist("checkboxes")
			print "lllllllllllllll"
		return redirect(url_for('shortlist'))
	else:
		print "2222222"
		return render_template('feedlist.html', list_id=list_id, index_article_list=index_article_list, session=session)

@app.route('/joke/<jokename>')
def joke(jokename):
	return render_template('joke.html', jokename=jokename)

@app.route('/shortlist')
def shortlist():
	return render_template('shortlist.html')

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


