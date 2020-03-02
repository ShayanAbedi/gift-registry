#!/usr/bin/env python3

from flask import Flask, jsonify, abort, request, make_response
from flask_restful import Resource, Api
import pymysql.cursors
import json

import cgitb
import cgi
import sys
cgitb.enable()

import settings 

app = Flask(__name__, static_url_path='/static')
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
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:userId>')


#############################################################################
if __name__ == "__main__":
	app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.APP_DEBUG)
