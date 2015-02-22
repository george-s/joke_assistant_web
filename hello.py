

from flask import Flask, render_template, g

app = Flask("__name__",  static_folder = "images")
print app
app.debug = True

@app.route('/')
def hello_world_with_template():
	name = "fred"
	return render_template('hello.html', name=name,variable=variable)

@app.route('/user/<name>')
def user(name):
	return render_template('hello.html', name=name)

@app.route('/shortlist')
def shortlist():
	list_id="123"
	return render_template('shortlist.html', list_id=list_id, variable=variable)

@app.route('/joke/<jokename>')
def joke(jokename):
	return render_template('joke.html', jokename=jokename)


if __name__ == '__main__':
    app.run()


