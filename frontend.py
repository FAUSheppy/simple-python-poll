from cpwrap import CFG
import database as db
from flask import request
import os.path

HTML_DIR = "html_js_partials/"

def readPartial(name):
    if not name.endswith((".html",".js",".css")):
        name = name + ".html"
    path = os.path.join(HTML_DIR, name)
    with open(path,"r") as f:
        return f.read()

def buildStartPage():
    return readPartial("base").format(title="simple-poll", body=readPartial("start-page"))

def buildCreatePoll(poll_name):
    body = readPartial("create-poll-partial")
    return readPartial("base").format(title="poll-create", body=body)

def buildTokenPartial(tokens):
    tokenPartial = ""
    tokenWrapper = "<div class='single-token'>{}</div>"
    if tokens:
        for tk in tokens:
            tk = tk[0]
            tokenPartial += tokenWrapper.format(tk)
    return tokenPartial

def buildPostCreatePoll(poll_name, tokens):
    hostname = request.url_root
    reverseProxyHostname = request.headers.get('X-REAL-HOSTNAME')
    if reverseProxyHostname:
        hostname = reverseProxyHostname

    hrefVote =    hostname + "vote?name="    + poll_name
    hrefResults = hostname + "results?name=" + poll_name
    hrefTokens =  hostname + "tokens?name="  + poll_name

    tokenPartial = buildTokenPartial(tokens)
   
    body = readPartial("post-create-partial").format(tokens=tokenPartial, poll_name=poll_name, \
                            linkToVote=hrefVote, linkToResults=hrefResults, linkToTokens=hrefTokens)
    return readPartial("base").format(title=poll_name, body=body)

def buildVoteInPoll(poll_name):
    script = readPartial("vote-js-partial.js")
    optionWrapper = "<span><input class='vote-option' type=checkbox id={}>{}</input></span>"
    options = db.getOptions(poll_name)
    if poll_name == "" or poll_name == None:
        return "<h1>No poll selected</h1>"
    elif options == None:
        return "<h1>Poll {} not found.</h1>".format(poll_name)

    # tokens needed?
    tokenInput = ""
    if db.tokenNeededExternal(poll_name):
        tokenInput = "<input type=text id=token-field>"

    # get poll question
    question = db.queryQuestion(poll_name)

    # build options
    voteOptions = ""
    for opt in options:
        voteOptions += optionWrapper.format(opt, opt)

    body = readPartial("vote-partials").format(script=script, question=question, \
                    poll_name=poll_name, voteoptions=voteOptions, tokenInput=tokenInput)
    return readPartial("base").format(title="voting", body=body)


def buildPostVote(poll_name, token, selectedOptions):
    try:
        db.vote(poll_name, selectedOptions, token)
    except PermissionError:
        return readPartial("base").format(title="Vote Failed", \
                        body='''
                        <div class='main-container'>
                            <h1>Vote failed<h1>Token invalid, cancled or already used.</h1> :(
                        </div>
                        ''')
    resultsHref = "'/results?name=%s'" % poll_name
    body = readPartial("post-vote-partial").format(poll_name=poll_name, resultsHref=resultsHref)
    return readPartial("base").format(title=poll_name, body=body)

def buildTokenQuery(poll_name, admToken):
    if db.tokenNeededExternal(poll_name):
        return readPartial("base").format(title="AdminVerifyFailed", \
                        body='''
                        <div class='main-container'>
                            <h1>Poll does not use tokens.</h1>
                        </div>
                        ''')
    elif not db.checkAdmTokenValid(poll_name, admToken) and False:
        return readPartial("base").format(title="AdminVerifyFailed", \
                        body='''
                        <div class='main-container'>
                            <h1>Admin-Token invalid</h1>
                        </div>
                        ''')
    else:
        pass
        tokens = db.getTokensExternal(poll_name)
        tokenPartial = buildTokenPartial(tokens)
        body = readPartial("token-query-partial").format(poll_name=poll_name, tokens=tokenPartial)
        return readPartial("base").format(title=poll_name, body=body)

def buildShowResults(poll_name):
    resultsDict, total = db.getResults(poll_name)
    resultWrapper = readPartial("result-wrapper-partial")
    results = resultWrapper.format(name="Answer", width="100%", ratio="Percentage", absolute="#votes") + "<hr>"
    
    for r in resultsDict.keys():
        ratio = 0
        if not total == 0:
            ratio = resultsDict[r]/total*100
        ratioString = "{:.1f}%".format(ratio)
        width = "{:.2f}%".format(ratio)
        count = resultsDict[r]
        name  = r
        results += resultWrapper.format(name=name, width=width, ratio=ratioString, absolute=count)

    body = readPartial("results-partial").format(poll_name=poll_name, question=db.queryQuestion(poll_name),\
                    voteoptions_results=results)
    return readPartial("base").format(title=poll_name, body=body)
