import datetime
from flask import Flask, request, render_template, g
from peewee import SqliteDatabase, PostgresqlDatabase, Model, CharField, TextField, DateTimeField, OperationalError
import psycopg2

## CONFIG
DEBUG = False

## MODELS
user = 'postgres'
host = 'postgres'
database = 'flask_app'

# Check if database already exists
try:
	con = psycopg2.connect(host=host, user=user, database="postgres")
	con.set_isolation_level(0)
	cur = con.cursor()
	cur.execute('CREATE DATABASE %s' % database)
except psycopg2.ProgrammingError as error:
	print("Database already exists")
finally:
	cur.close()


print("Database already exists")

An alternative using EXISTS is better in that it doesn't require that all rows be retrieved, but merely that at least one such row exists:

>>> cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('mytable',))
>>> cur.fetchone()[0]

#database = SqliteDatabase(DATABASE)
psql_db = PostgresqlDatabase(database, user=user, host=host)

class Comment(Model):
    title = CharField()
    body = TextField()
    date = DateTimeField()
    author = CharField()

    class Meta:
        database = psql_db

## APP
app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
	g.db = psql_db
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
    	title = request.form['title']
    	author = request.form['author']
    	body = request.form['text']

    	comment = Comment.create(
    		title=title,
    		body=body,
    		author=author,
    		date=datetime.datetime.now())
    	comment.save()

    comments = Comment.select().order_by(Comment.date.desc())
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
	try:
		Comment.create_table()
	except OperationalError:
		print("Comment table already exists!")
	app.run()
