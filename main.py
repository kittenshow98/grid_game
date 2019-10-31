from flask import Flask, render_template, request, jsonify, Response
import requests
import datetime
import json
import logging
import sqlalchemy
import pymysql
import jinja2

app = Flask(__name__, template_folder='template')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

_host = "127.0.0.1"
_port = 5002
_api_base = "/api"

# db = sqlalchemy.create_engine(
#     # Equivalent URL:
#     # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
#     sqlalchemy.engine.url.URL(
#         drivername='mysql+pymysql',
#         username="root",
#         password="dbuserdbuser",
#         database="colorpairs",
#         query={
#             'unix_socket': '/cloudsql/{}'.format("gridgame-257423:us-east1:gridgame")
#         }
#     )
# )

db = pymysql.connect(host='localhost',
                     user='dbuser',
                     password='dbuserdbuser',
                     db='gridgame',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)


def handle_args(args):
  """

  :param args: The dictionary form of request.args.
  :return: The values removed from lists if they are in a list. This is flask weirdness.
      Sometimes x=y gets represented as {'x': ['y']} and this converts to {'x': 'y'}
  """
  result = {}

  if args is not None:
    for k, v in args.items():
      if type(v) == list:
        v = v[0]
      result[k] = v

  return result


def log_and_extract_input(method, path_params=None):
  path = request.path
  args = dict(request.args)
  data = None
  headers = dict(request.headers)
  method = request.method
  url = request.url
  base_url = request.base_url

  try:
    if request.data is not None:
      data = request.json
    else:
      data = None
  except Exception as e:
    # This would fail the request in a more real solution.
    data = "You sent something but I could not get JSON out of it."

  log_message = str(datetime.now()) + ": Method " + method

  # Get rid of the weird way that Flask sometimes handles query parameters.
  args = handle_args(args)

  inputs = {
    "path": path,
    "method": method,
    "path_params": path_params,
    "query_params": args,
    "headers": headers,
    "body": data,
    "url": url,
    "base_url": base_url
  }

  # Pull out the fields list as a separate element.
  if args and args.get('fields', None):
    fields = args.get('fields')
    fields = fields.split(",")
    del args['fields']
    inputs['fields'] = fields

  log_message += " received: \n" + json.dumps(inputs, indent=2)
  logger.debug(log_message)

  return inputs


def log_response(path, rsp):
  """

  :param path: The path parameter received.
  :param rsp: Response object
  :return:
  """
  msg = rsp
  logger.debug(str(datetime.now()) + ": \n" + str(rsp))


def generate_error(status_code, ex=None, msg=None):
  """

  This used to be more complicated in previous semesters, but we simplified for fall 2019.
  Does not do much now.
  :param status_code:
  :param ex:
  :param msg:
  :return:
  """

  rsp = Response("Oops", status=500, content_type="text/plain")

  if status_code == 500:
    if msg is None:
      msg = "INTERNAL SERVER ERROR. Please take COMSE6156 -- Cloud Native Applications."

      rsp = Response(msg, status=status_code, content_type="text/plain")

  return rsp


@app.route('/', methods=['GET'])
def index():
  votes = []
  # with db.connect() as conn:
  if db:
    cur = db.cursor()
    # Execute the query and fetch all results
    res = cur.execute(
      "SELECT" + " * FROM color ORDER BY RAND() LIMIT 1;"
    )
    random_color = cur.fetchall()
    random_color1 = random_color[0]['deep']
    random_color2 = random_color[0]['light']
  return render_template(
    'grid.html',
    random_color1=random_color1,
    random_color2=random_color2
  )
