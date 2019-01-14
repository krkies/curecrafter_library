from flask import Flask

def createApp(database):
    app = Flask(__name__)
    app.config['DATABASE'] = database
    return app
    
