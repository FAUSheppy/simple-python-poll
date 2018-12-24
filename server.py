from flask import Flask, requests
from cpwrap import CFG

app = Flask(CFG("appName"))

def getParam(param):
    return requests.args.get(param)

########################################################

@app.route('/')
def startPage():
    return frontend.buildStartPage()

@app.route('/create')
def createPoll():
    poll_name = getParam(dd"name") 
    return frontend.buildCreatePoll(poll_name)

@app.route('/post-create')
def postCreatePoll():
    poll_name = getParam("name") 
    return frontend.buildPostCreatePoll(poll_name)

@app.route('/ask-token')
def askToken():
    poll_name = getParam("name") 
    return frontend.buildAskToken(poll_name)

@app.route('/vote')
def voteInPoll():
    poll_name = getParam("name") 
    return frontend.buildVoteInPoll(poll_name)

@app.route('/post-vote')
def postVote():
    poll_name = getParam("name") 
    return frontend.buildPostVote(poll_name)

@app.route('/results')
def showResults():
    poll_name = getParam("name") 
    return frontend.buildShowResults(poll_name)

if __name__ == "__main__":
    app.run(host='127.0.0.1')
