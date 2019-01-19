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
    useTokens = bool(int(arg("tokens")))
    question  = arg("q").strip()
    multi     = bool(int(arg("multi")))
    tokens = None
    if not question.endswith("?"):
        question += "?"
    if db.checkPollExists(getPollName()):
        return "<h1>Poll {} already exists!<h1>".format(getPollName())
    tokens = db.createPoll(getPollName(), arg("options").split(","), question, useTokens, multi)
    return frontend.buildPostCreatePoll(getPollName(), tokens)

@app.route('/polladmin')
def tokenQuery(preToken=""):

    # generate new tokens if needed
    newTokens = 0
    try:
        newTokens = int(arg("generate"))
        if newTokens > 50:
            newTokens = 50
    except (ValueError, TypeError):
        newTokens = 0
   
    name = getPollName()
    if preToken:
        token = preToken
        name  = db.pollNameFromToken(preToken)
    else:
        token = arg("admtoken")
 
    return frontend.buildTokenQuery(name, token, newTokens=newTokens, limitReached=newTokens >= 50)

@app.route('/vote')
def voteInPoll(poll_name=None, preToken=""):
    if poll_name:
        ret = frontend.buildVoteInPoll(poll_name, preToken)
    else:
        poll_name = getPollName()
        if not poll_name and preToken:
            poll_name = db.pollNameFromToken(preToken)
        ret = frontend.buildVoteInPoll(poll_name, preToken)
    return ret

@app.route('/post-vote')
def postVote():
    return frontend.buildPostVote(getPollName(), arg("token"), arg("selected"))

@app.route('/results')
def showResults():
    return frontend.buildShowResults(getPollName())

@app.route('/poll')
def multiplex():
    ident = arg("ident")
    if not ident:
        raise ValueError("no ident given")
    elif db.checkPollExists(ident):
        return voteInPoll(poll_name=ident)
    elif db.isValidAdmToken(ident):
        return tokenQuery(preToken=ident)
    elif db.isValidToken(ident):
        return voteInPoll(preToken=ident)
    else:
        return voteInPoll(poll_name=ident)

@app.route('/site.css')
def css():
    return app.send_static_file('site.css')

if __name__ == "__main__":
    db.init()
    app.run(host='0.0.0.0')
