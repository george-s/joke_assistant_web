# We'll need the session object to manage session variables
# render_template to render html content from templates
# url_for to extract the url for a given view/route
# request to access the GET data request for the form view
# redirect to perform redirects to different routes
from flask import Flask, session, render_template, url_for, request, redirect

app = Flask("__name__",  static_folder = "images")
print app
app.debug = True
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# def sumSessionCounter():
#   try:
#     session['counter'] += 1
#   except KeyError:
#     session['counter'] = 1


@app.route('/')
def index():
	name = "fred"
	return render_template('index.html', name=name)

@app.route('/user/<name>')
def user(name):
	return render_template('hello.html', name=name)

@app.route('/shortlist')
def shortlist():
	list_id="123"
	return render_template('shortlist.html', list_id=list_id)

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
    return redirect(url_for('index'))
  else:
    # If no name has been sent, show the form
    return render_template('form.html', session=session)


if __name__ == '__main__':
    app.run()


