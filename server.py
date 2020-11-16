from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
app = Flask(
    __name__,
    template_folder='views'
)

@app.route('/')
def artists():
    props = {
        'currentPage': 'artists'
    }
    results = {}
    return render_template('artists.html', props=props)

@app.route('/artists')
def root():
    return redirect('/', code=308)