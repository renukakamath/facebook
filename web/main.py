from flask import *
from admin import admin
from public import public
from api import api


app=Flask(__name__)
app.secret_key="hello"
app.register_blueprint(public)
app.register_blueprint(api,url_prefix='/api')
app.register_blueprint(admin,url_prefix='/admin')


app.run(debug=True,port=5675,host="0.0.0.0")