## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album:', validators =[Required()])
	ranking = RadioField('How much do you like this album?', choices = [('1','1'), ('2', '2'), ('3','3')])
	submit = SubmitField()



####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


####################
###### PART 1 ######
####################

@app.route('/artistform')
def queryForm():
	return render_template('artistform.html')


@app.route('/artistinfo', methods = ['GET', 'POST'])
def queryResult():
	if request.method == 'GET':
		# Get the artist name from the user's form
		query = request.args.get('artist')
		# Prepare to make a request to the iTunes API
		baseurl = 'https://itunes.apple.com/search'
		params = {'term':query}
		# Make a request to the iTunes API
		resp = requests.get(baseurl, params = params)
		text = json.loads(resp.text)
		results = text['results']
		return render_template('artist_info.html', objects = results)
	return redirect(url_for('queryForm'))

@app.route('/artistlinks')
def links():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def songDisplay(artist_name):
	# Prepare to make a request to the iTunes API
	baseurl = 'https://itunes.apple.com/search'
	params = {'term':artist_name}
	# Make a request to the iTunes API
	resp = requests.get(baseurl, params = params)
	text = json.loads(resp.text)
	results = text['results']
	return render_template('specific_artist.html', results = results)


####################
###### PART 2 ######
####################

@app.route('/album_entry')
def albumForm():
	album_form = AlbumEntryForm()
	return render_template('album_entry.html', form = album_form)

@app.route('/album_data', methods = ['GET', 'POST'])
def albumData():
	data_form = AlbumEntryForm(request.form)
	if request.method =='POST':
		album_name = data_form.album_name.data
		rank = data_form.ranking.data
	

	return render_template('album_data.html', album = album_name, stars = rank)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
