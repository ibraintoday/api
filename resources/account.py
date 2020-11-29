from flask_restful import Resource,reqparse
from flask import jsonify
import pymysql


parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')

class Accounts(Resource):
    def db_init(self):
      db = pymysql.connect('192.168.56.103',
                      'duke','admin123','usres')
      cursor = db.cursor(pymysql.cursors.DictCursor)
      return db, cursor
    def get(self):
      db = pymysql.connect('192.168.56.103',
                      'duke','admin123','usres')
      cursor = db.cursor(pymysql.cursors.DictCursor)
      sql = """Select * From usres.accounts where `deleted` =False"""
      cursor.execute(sql)
      users = cursor.fetchall()
      db.close()
      response = {
        'data': users
      }
      return jsonify(response)

    def post(self):
      db, cursor = self.db_init()
      arg = parser.parse_args()
      user = {
          'balance':arg['balance'],
          'account_number':arg['account_number'],
      }
      sql = """
        Insert into usres.accounts
        (balance, account_number)
        values('{}','{}')
      """.format(user['balance'],user['account_number'],
                )
      result = cursor.execute(sql)
      db.commit()
      db.close()
      response = {
          'result':True
      }
    def patch(self, id):
      db, cursor = self.db_init()
      arg = parser.parse_args()
      account = {
          'balance':arg['balance'],
          'account_number':arg['account_number'],
      }
      query = []
      for key,value in account.items():
        if value != None:
          query.append(key + ' = ' + " '{}' ".format(value))
      query = ",".join(query)
      sql = """ Update usres.accounts Set {} where id = "{}"
      """.format(query, id)
      #print(sql)
      cursor.execute(sql)
      db.commit()
      db.close()
      response = {
          'result': True
      }
      return jsonify(response)
    def delete(self,id):
      db, cursor = self.db_init()
      sql = """Update usres.accounts Set `deleted` = True where id = '{}'
      """.format(id)
      print(sql)
      cursor.execute(sql)
      db.commit()
      db.close()
      response = {
        'result': True
      }
      return jsonify(response)