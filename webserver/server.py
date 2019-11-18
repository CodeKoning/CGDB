"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://rjk2153:1749@35.243.220.243/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)

  cursor = g.conn.execute("SELECT name FROM executives ORDER BY eid")
  names = []
  for result in cursor:
    names.append(result['name'])
  cursor.close()

  cursor = g.conn.execute("SELECT name FROM companies ORDER BY cid")
  cnames = []
  for result in cursor:
    cnames.append(result['name'])
  cursor.close()

  cursor = g.conn.execute("SELECT name FROM universities ORDER BY uid")
  uNames = []
  for result in cursor:
    uNames.append(result['name'])
  cursor.close()

  context = dict(data = names, udata = uNames, cdata = cnames)

  return render_template("index.html", **context)

@app.route('/search', methods=['POST'])
def search():
  query = request.form['search_query']
  print(query)
  cursor = g.conn.execute("SELECT name FROM executives ORDER BY eid")
  eindex = []
  for entry in cursor:
    eindex.append(entry['name'])

  cursor = g.conn.execute("SELECT name FROM companies ORDER BY cid")
  cindex = []
  for entry in cursor:
    cindex.append(entry['name'])

  cursor = g.conn.execute("SELECT name FROM universities ORDER BY uid")
  uindex = []
  for entry in cursor:
    uindex.append(entry['name'])
  print(uindex)

  if query in eindex:
    cursor = g.conn.execute("SELECT e.eid from executives e where e.name = %s", (query))
    eid = cursor.fetchone()['eid']
    cursor.close()
    return redirect(url_for('show_exec', eid=eid))
  elif query in cindex:
    cursor = g.conn.execute("SELECT c.cid from companies c where c.name = %s", (query))
    cid = cursor.fetchone()['cid']
    cursor.close()
    return redirect(url_for('show_comp', cid=cid))
  elif query in uindex:
    cursor = g.conn.execute("SELECT u.uid from universities u where u.name = %s", (query))
    uid = cursor.fetchone()['uid']
    cursor.close()
    return redirect(url_for('show_uni', uid=uid))
  else:
    cursor.close()
#   flash('Search query is not in the database') - Does not work without app secrets, will just redirect to index and annotate the README.
    return redirect(url_for('index'))

@app.route('/university/<int:uid>')
def show_uni(uid=None):
  uni_id = uid
  cursor = g.conn.execute("SELECT * FROM universities WHERE universities.uid = %s", (uni_id))
  uname = cursor.fetchone()

  cursor = g.conn.execute("SELECT * FROM executives e, education ed WHERE ed.uid = %s AND e.eid = ed.eid", (uni_id))
  alums = []
  for result in cursor:
    alums.append(result)

  cursor.close()
  context = dict(udata = uname, alum_arr = alums)

  return render_template("university.html", **context)

@app.route('/executive/<int:eid>')
def show_exec(eid=None):
  exec_id = eid
  cursor = g.conn.execute("SELECT * FROM executives WHERE executives.eid = %s", (exec_id))
  ename = cursor.fetchone()

  cursor = g.conn.execute("SELECT c.name FROM executives e, companies c, founded_by f WHERE e.eid = %s AND e.eid = f.eid AND c.cid = f.cid", (exec_id))
  founded = []
  for result in cursor:
      founded.append(result)

  cursor.close()
  context = dict(edata = ename, founded_arr = founded)

  return render_template("executive.html", **context)

@app.route('/company/<int:cid>')
def show_comp(cid=None):
  comp_id = cid
  cursor = g.conn.execute("SELECT name FROM companies WHERE companies.cid = %s", (comp_id))
  cname = cursor.fetchone()

  cursor = g.conn.execute("SELECT e.name, f.inception_year FROM executives e, companies c, founded_by f WHERE c.cid = %s AND e.eid = f.eid AND c.cid = f.cid", (comp_id))
  founded = []
  for result in cursor:
      founded.append(result)

  cursor = g.conn.execute("SELECT DISTINCT e.name, o.officer_title FROM executives e, officers o, companies c, works_in w WHERE e.eid = o.eid AND o.eid =  w.eid AND w.cid = %s ORDER BY o.officer_title", (comp_id))
  officers = []
  for officer in cursor:
      officers.append(officer)

  cursor = g.conn.execute("SELECT DISTINCT e.name, d.dir_title FROM executives e, directors d, companies c, member_of m, governed_board g WHERE e.eid = d.eid AND d.eid = m.eid AND m.bid = g.bid AND g.cid = %s", (comp_id))
  board_mems = []
  for member in cursor:
      board_mems.append(member)

  cursor.close()
  context = dict(cdata = cname, off_arr = officers, board_arr = board_mems, founded_arr = founded)

  return render_template("company.html", **context)

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO executives(name) VALUES (%s)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
