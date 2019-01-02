from cpwrap import CFG
import database as db
from flask import request
import os.path
import htmlsnippets as html

HTML_DIR = "html_js_partials/"

def buildStartPage():
    return htlm.startPage

def buildCreatePoll(poll_name):
    return html.pollCreator

def buildPostCreatePoll(poll_name, tokens):

    # use HTML-header if there is one #
    hostname = request.url_root
    reverseProxyHostname = request.headers.get('X-REAL-HOSTNAME')
    if reverseProxyHostname:
        hostname = reverseProxyHostname

    # build links #
    hrefVote =    hostname + "vote?name="       + poll_name
    hrefResults = hostname + "results?name="    + poll_name
    hrefTokens =  hostname + "polladmin?name="  + poll_name + "&admtoken=" + db.getAdmToken(poll_name)
    
    # show tokens if nessesary #
    tokenPartial = html.buildTokenPartial(tokens)

    # build the complete page #
    body = readPartial("post-create-partial").format(tokens=tokenPartial, poll_name=poll_name, \
                            linkToVote=hrefVote, linkToResults=hrefResults, linkToTokens=hrefTokens, \
                            admToken=db.getAdmToken(poll_name))
    return readPartial("base").format(title=poll_name, body=body)


def buildVoteInPoll(poll_name, preToken=""):

    # tell javascript/user if it's multiple choice #
    multiStr = "false"
    if(db.isMultiChoice(poll_name)):
        multiStr = "true"
    script = readPartial("vote-js-partial.js") % multiStr
    info = html.infoSingleChoice
    if(db.isMultiChoice(poll_name)):
        info = html.infoMultipleChoice

    # get poll question #
    question = db.queryQuestion(poll_name)
    
    # build answer section #
    options = db.getOptions(poll_name)
    if poll_name == "" or poll_name == None:
        return html.noPollSelected
    elif options == None:
        return html.noPollWithName.format(poll_name)
    voteOptions = ""
    for opt in options:
        voteOptions += html.optionWrapper.format(opt, opt)

    # tokens #
    tokenInput = ""
    if db.tokenNeededExternal(poll_name):
        tokenInput = html.tokenInput.format(preToken)

    # combine everything #
    body = readPartial("vote-partials").format(script=script, question=question, \
                    poll_name=poll_name, info=info, voteoptions=voteOptions, tokenInput=tokenInput)
    return readPartial("base").format(title="voting", body=body)


def buildPostVote(poll_name, token, selectedOptions):
    try:
        db.vote(poll_name, selectedOptions, token)
    except PermissionError:
        return html.voteFailed
    resultsHref = html.resultsHref % poll_name
    body = readPartial("post-vote-partial").format(poll_name=poll_name, resultsHref=resultsHref)
    return readPartial("base").format(title=poll_name, body=body)


def buildTokenQuery(poll_name, admToken, newTokens=0):
    if not db.tokenNeededExternal(poll_name):
        return readPartial("base").format(title="NoTokens", html.pollHasNoTokens)
    elif not db.checkAdmTokenValid(poll_name, admToken):
        return readPartial("base").format(title="AdminVerifyFailed", html.adminTokenInvalid)
    else:
        # get current tokens #
        tokens = db.getTokensExternal(poll_name)

        # if new tokens, generate new tokens and simply reload the page #
        if len(tokens) < newTokens:
            db.genTokensExternal(poll_name, newTokens - len(tokens))
            href = "/polladmin?name=%s&admtoken=%s" % (poll_name, admToken)
            return html.redirectTo.format(href)
        
        # show the page normally #
        tokenPartial = buildTokenPartial(tokens)
        body = readPartial("token-query-partial").format(poll_name=poll_name, tokens=tokenPartial)
        return readPartial("base").format(title=poll_name, body=body)


def buildShowResults(poll_name):
    resultsDict, total = db.getResults(poll_name)
    resultWrapper = readPartial("result-wrapper-partial")
    results = resultWrapper.format(name="Answer", width="100%", ratio="Percentage", absolute="#votes") + "<hr>"
    
    # build the percentage bar #
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
