import flask
from flask import request, jsonify

from flask_restful import Api, Resource
from resources.user import Users, User
from resources.account import Accounts
from flask import request, jsonify
import pymysql
app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Ａccounts, '/bank-accounts')
#api.add_resource(User, '/bank-account/<id>')

@app.route('/', methods=['GET'])
def home():
    return "Hello World"

@app.before_request
def auth():
  token = request.headers.get('auth')
  if token == '567':
    pass
  else:
    response = {'msg': 'invalid token'}
    return response, 401

@app.errorhandler(Exception)
def handle_error(error):
  status_code = 500
  if(type(error).__name__ == 'NotFound'):
    status_code = 404
  else:
    pass
  return {'msg': type(error).__name__}, status_code

@app.route('/account/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
  db, cursor, account = get_account(account_number)
  money = request.values['money']
  balance = account['balance'] + int(money)
  sql = """
  Update usres.accounts Set balance = {}
  where account_number = '{}'
  """.format(balance, account_number)
  cursor.execute(sql)
  db.commit()
  db.close()
  response = {
    'result': True
  }
  return jsonify(response)

@app.route('/account/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
  db, cursor, account = get_account(account_number)
  money = request.values['money']
  balance = account['balance'] - int(money)
  if balance < 0:
    response = {
        'result': False,
        'msg': '餘額不足'
    }
    code = 400
  else:
    sql = """
    Update usres.accounts Set balance = {}
    where account_number = '{}'
    """.format(balance, account_number)
    cursor.execute(sql)
    db.commit()
    db.close()
    response = {
      'result': True
    }
    code = 200
  return jsonify(response), code

def get_account(account_number):
    db = pymysql.connect('192.168.56.103',
                      'duke','admin123','usres')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
    Select * From usres.accounts
    where account_number ='{}'
    """.format(account_number)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()

if __name__ == "__main__":
     app.run(port=5000)