from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
import psycopg2
app = Flask(
    __name__,
    template_folder='views'
)
try:
    connection = psycopg2.connect(
        host = 'localhost',
        dbname = 'kemonodb',
        user = 'nano',
        password = 'shinonome'
    )
    cursor = connection.cursor()
except Exception as error:
    print("Failed to connect to the database: ",error)

@app.route('/')
def artists():
    props = {
        'currentPage': 'artists'
    }
    if not request.args.get('commit'):
        results = {}
    else:
        query = "SELECT * FROM lookup "
        query += "WHERE name ILIKE '%{}%' ".format(request.args.get('q'))
        if request.args.get('service'):
            query += "AND service = '{}' ".format(request.args.get('service'))
        query += "AND service != 'discord-channel' "
        query += "ORDER BY {0} {1} ".format(request.args.get('sort_by'), request.args.get('order'))
        query += "OFFSET {} ".format(request.args.get('o') if request.args.get('o') else 0)
        query += "LIMIT 25"
        cursor.execute(query)
        results = cursor.fetchall()
    return render_template(
        'artists.html',
        props = props,
        results = results
    )

@app.route('/artists')
def root():
    return redirect('/', code=308)