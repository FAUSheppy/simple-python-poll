from flask import Flask
from configparse_wrapper.cpwrap import CFG

app = Flask(CFG("appName"))

@app.route('/')
def main(env, start_response):
    return "<span style='color:red'>I am app 1</span>"
