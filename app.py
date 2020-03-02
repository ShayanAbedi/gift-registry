#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import Resource, Api, reqparse
from flask_session import Session

from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *

import pymysql.cursors
import json

import cgitb
import cgi
import sys
cgitb.enable()

import settings 

app = Flask(__name__, static_url_path='/static')


app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)
api = Api(app)
####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { "status": "Bad request" } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { "status": "Resource not found" } ), 404)

####################################################################################
#
# Static Endpoints
#
class Root(Resource):
	def get(self):
		return make_response(jsonify({"message": "Welcome to the GiftRegistrys"}))

api.add_resource(Root,'/')

####################################################################################
#
# Authentication
#
class SignIn(Resource):
	#
	# Login, start a session and set/return a session cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "cr*ap"}'
	#  	-c cookie-jar http://info3103.cs.unb.ca:xxxxx/signin
	#
	def post(self):
		if not request.json:
			abort(400)
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400)

		if request_params['username'] in session:
			response = {'status':'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.
				session['username'] = request_params['username']
				response = {'status': 'success' }
				responseCode = 201
			except (LDAPException, error_message):
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)














#
# Users routing: GET and POST, individual user access
#
class Users(Resource):
    # GET: Return all user resources
	#
	# Example request: curl http://info3103.cs.unb.ca:xxxxx/users
	def get(self):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getUsers'
			cursor = dbConnection.cursor()
			cursor.callproc(sql) 
			rows = cursor.fetchall()
		except:
			abort(500) 
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({'users': rows}), 200)
    

	def post(self):
        #
        # Sample command line usage:
        #
        # curl -i -X POST -H "Content-Type: application/json"
        #    -d '{"email": "test@gmail.com", "user_name": "test"}'
        #         http://info3103.cs.unb.ca:xxxxx/users

		if not request.json or not 'user_name' in request.json:
			abort(400) # bad request

		# Pull the results out of the json request
		userName = request.json['user_name']
		email = request.json['email']
		if 'img_url' in request.json:
			img = request.json['img_url']
		else:
			img = ""
  
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'addUser'
			cursor = dbConnection.cursor()
			sqlArgs = (userName, email, img) 
			cursor.callproc(sql,sqlArgs) 
			row = cursor.fetchone()
			dbConnection.commit() 
		except:
			abort(500) 
		finally:
			cursor.close()
			dbConnection.close()
   
		uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+str(request.url_rule)+'/'+str(row['LAST_INSERT_ID()'])
		return make_response(jsonify( {"URI":uri} ), 201) 


class User(Resource):
    # GET: Return identified user resource
	#
	# Example request: curl http://info3103.cs.unb.ca:xxxxx/users/2
	def get(self, userId):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'getUserById'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,)
			cursor.callproc(sql,sqlArgs) 
			row = cursor.fetchone() 
			if row is None:
				abort(404)
		except:
			abort(500) 
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({"user": row}), 200)

    # PUT: Update identified user resource
    #
    # Example request: 
	# curl -X PUT -H "Content-Type: application/json" 
	# -d '{"user_name":"Shayan Abedi","email":"abedi.shayan@unb.ca"}' http://info3103.cs.unb.ca:xxxx/users/3
	def put(self, userId):
		if not request.json:
			abort(400) # bad request

		# Pull the results out of the json request
		userName = request.json['user_name']
		email = request.json['email']
		if 'img_url' in request.json:
			img = request.json['img_url']
		else:
			img = ""
  
		try:
			dbConnection = pymysql.connect(settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'updateUser'
			cursor = dbConnection.cursor()
			sqlArgs = (userId, userName, email, img) 
			cursor.callproc(sql,sqlArgs) 
			row = cursor.fetchone()
			dbConnection.commit() 
		except:
			abort(500) 
		finally:
			cursor.close()
			dbConnection.close()
   
		uri = 'http://'+settings.APP_HOST+':'+str(settings.APP_PORT)
		uri = uri+'/users/'+str(userId)
		return make_response(jsonify( {"URI":uri} ), 200) 

    # DELETE: Delete identified user resource
    #
    # Example request: curl -X DELETE http://info3103.cs.unb.ca:xxxxx/users/2
	def delete(self, userId):
		try:
			dbConnection = pymysql.connect(
				settings.DB_HOST,
				settings.DB_USER,
				settings.DB_PASSWD,
				settings.DB_DATABASE,
				charset='utf8mb4',
				cursorclass= pymysql.cursors.DictCursor)
			sql = 'deleteUserById'
			cursor = dbConnection.cursor()
			sqlArgs = (userId,)
			cursor.callproc(sql,sqlArgs)
			print("UserId to delete: "+str(userId))
			dbConnection.commit()
		except:
			abort(500)
		finally:
			cursor.close()
			dbConnection.close()
		return make_response(jsonify({"message": "The user and its present list successfully deleted"}), 200)
####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:userId>')


#############################################################################
if __name__ == "__main__":
	app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
