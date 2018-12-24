#!/usr/bin/python3
from flask import Flask, request
from cpwrap import CFG
import frontend

app = Flask(CFG("appName"))

def getPollName():
    return request.args.get("name")

########################################################

@app.route('/')
def startPage():
    return frontend.buildStartPage()

@app.route('/create')
def createPoll():
    return frontend.buildCreatePoll(getPollName())

@app.route('/post-create')
def postCreatePoll():
    return frontend.buildPostCreatePoll(getPollName())

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
    app.run(host='127.0.0.1')
