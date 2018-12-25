#!/usr/bin/python3
from flask import Flask, request
from cpwrap import CFG
import frontend
import database as db

app = Flask(CFG("appName"))

def getPollName():
    return request.args.get("name")
def arg(param):
    return request.args.get(param)

########################################################

@app.route('/')
def startPage():
    return frontend.buildStartPage()

@app.route('/create')
def createPoll():
    return frontend.buildCreatePoll(getPollName())

@app.route('/post-create')
def postCreatePoll():
    useTokens = arg("tokens") == "0"
    tokens = db.createPoll(getPollName(), arg("options").split(","), useTokens)
    return frontend.buildPostCreatePoll(getPollName(), tokens)

@app.route('/ask-token')
def askToken():
    return frontend.buildAskToken(getPollName())

@app.route('/vote')
def voteInPoll():
    return frontend.buildVoteInPoll(getPollName())

@app.route('/post-vote')
def postVote():
    return frontend.buildPostVote(getPollName())

@app.route('/results')
def showResults():
    return frontend.buildShowResults(getPollName())

if __name__ == "__main__":
    db.init()
    app.run(host='127.0.0.1')
