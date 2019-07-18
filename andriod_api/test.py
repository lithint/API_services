from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
import db_connection as db
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from passlib.hash import pbkdf2_sha256
import passlib.context

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


DEFAULT_CRYPT_CONTEXT = passlib.context.CryptContext(
    # kdf which can be verified by the context. The default encryption kdf is
    # the first of the list
    ['pbkdf2_sha512', 'plaintext'],
    # deprecated algorithms are still verified as usual, but ``needs_update``
    # will indicate that the stored hash should be replaced by a more recent
    # algorithm. Passlib 1.6 supports an `auto` value which deprecates any
    # algorithm but the default, but Ubuntu LTS only provides 1.5 so far.
    deprecated=['plaintext'],
)

def _crypt_context():
    return DEFAULT_CRYPT_CONTEXT

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.verify_password
def verify_password(username, password):
    print (username, password)
    conn,cr = db.create_db_connection()
    qry = "select COALESCE(password, '') from res_users where login = '%s'" %(username)
    cr.execute(qry)
    [hashed] = cr.fetchone()
    db.close_db_connection(conn,cr)
    valid, replacement = _crypt_context().verify_and_update(password, hashed)
    return valid

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/', methods=['GET'])
def index():
    return "Andriod API Services"

class Products(Resource):
     @auth.login_required
     def get(self):
         conn,cr = db.create_db_connection() # connect to database
         cr.execute("select * from product_product") # This line performs query and returns json result
         data = {'product': [i[0] for i in cr.fetchall()]}  # Fetches first column that is Product
         db.close_db_connection(conn,cr)
         return jsonify(data)

class Customer(Resource):
     @auth.login_required
     def get(self):
         conn,cr = db.create_db_connection() # connect to database
         cr.execute("select id,name,email from res_partner") # This line performs query and returns json result
         result = {'data': cr.fetchall()}  # Fetches first column that is customer
         db.close_db_connection(conn,cr)
         return jsonify(result)


class Customer_Name(Resource):
     @auth.login_required
     def get(self, cust_id):
         conn,cr = db.create_db_connection()
         cr.execute("select id,name,email from res_partner where id=%d " %int(cust_id))
         result = {'data': cr.fetchall()}
         return jsonify(result)

api.add_resource(Products, '/api/v1/products',methods=['GET'])
api.add_resource(Customer, '/api/v1/customer',methods=['GET'])
api.add_resource(Customer_Name,'/api/v1/customer/<cust_id>',methods=['GET'])

if __name__ == '__main__':
     app.run(port='5002')
