from flask import Flask
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key='secret_key'
# index.py 불러오기
from app.main.index import main as main

# index.py를 main page로 연동해줌
app.register_blueprint(main)
