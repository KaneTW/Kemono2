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
        query += "WHERE name ILIKE %s "
        params = ('%' + request.args.get('q') + '%',)
        if request.args.get('service'):
            query += "AND service = %s "
            params += (request.args.get('service'),)
        query += "AND service != 'discord-channel' "
        if request.args.get('sort_by') == 'indexed':
            query += 'ORDER BY indexed '
        elif request.args.get('sort_by') == 'name':
            query += 'ORDER BY name '
        elif request.args.get('sort_by') == 'service':
            query += 'ORDER BY service '
        if request.args.get('order') == 'asc':
            query += 'asc '
        elif request.args.get('order') == 'desc':
            query += 'desc '
        query += "OFFSET %s "
        offset = request.args.get('o') if request.args.get('o') else 0
        params += (offset,)
        query += "LIMIT 25"
        cursor.execute(query, params)
        results = cursor.fetchall()
    return render_template(
        'artists.html',
        props = props,
        results = results
    )

@app.route('/artists')
def root():
    return redirect('/', code=308)