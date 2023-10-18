from flask import Flask
from flask import request

import FruitController
import SessionController

app = Flask(__name__, static_url_path='', static_folder='static')

app.add_url_rule('/', view_func=SessionController.login)
app.add_url_rule('/index', view_func=SessionController.login)
app.add_url_rule('/login', view_func=SessionController.login)

app.add_url_rule('/fruit', view_func=FruitController.hello)
app.add_url_rule('/fruit/<fruit_name>', view_func=FruitController.fruit_tips, methods = ['POST', 'GET'])


app.run(debug=True, port=5000)