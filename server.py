#!/usr/bin/python3
import flask

from   utils.cpwrap      import CFG

import database.database as db

###### HTML Snippets #########
tokenWrapper   = "<div class='single-token'>{}</div>"
optionWrapper  = "<span><input class='vote-option' type=checkbox id={}>{}</input></span>"
noPollSelected = "<h1>No poll selected</h1>"
noPollWithName = "<h1>Poll {} not found.</h1>"
tokenInput     = "Token: <input class=vote-token-field type=text value='{token}' id=token-field>"

infoSingleChoice = "SINGLE CHOICE"
infoMultipleChoice  = "MULTIPLE CHOICE"
resultsHref      = "'/results?name=%s'"

pollHasNoTokens   = "<div class='main-container'><h1>Poll does not use tokens.</h1></div>"
adminTokenInvalid = "<div class='main-container'><h1>Admin token invalid.</h1></div>"
redirectTo = '<html><meta http-equiv="refresh" content="0"; url="{}"></html>'

app = flask.Flask(CFG("appName"))

##### FRONTEND PATHS ########

def getHostname():
    # check for header (reverse proxy support or use request host otherwise #
    hostname  = flask.request.headers.get("X-REAL-HOSTNAME")
    if not hostname:
        hostname  = flask.request.url_root
    return hostname

@app.route('/')
def rootPage():
    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html", websiteTitle="SimplePoll"))
    return flask.render_template("startpage.html", header=header, footer=footer)

@app.route("/tokeninputview")
def tokenInputView():
    '''This path displays a creation dialog for new poll'''
    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html", websiteTitle="Token"))
    return flask.render_template("stringinput.html", header=header, footer=footer)

@app.route("/viewcreate")
def viewCreate():
    '''This path displays a creation dialog for new poll'''
    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html", websiteTitle="Create"))
    return flask.render_template("viewcreate.html", header=header, footer=footer)

@app.route('/pollinfoadmin')
@app.route('/viewpostcreate')
def viewPostCreate():
    '''Page for managing polls'''

    pollIdent = flask.request.args.get("pollIdent")
    admToken  = flask.request.args.get("admToken")
    
    voteOptions = db.getVoteOptions(pollIdent)
    question    = db.getPollQuestion(pollIdent)
    tokens      = db.getTokensExternal(pollIdent)
    hostname    = getHostname()

    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html", websiteTitle="SimplePoll"))
    return flask.render_template("postcreate.html", header=header, footer=footer, \
                                    pollName=question, tokens=tokens, admToken=admToken, \
                                    pollIdent=pollIdent, hostname=hostname)

@app.route("/viewvote")
def viewVote():
    '''This path displays the actual options to vote'''
    
    token       = flask.request.args.get("token")
    pollIdent   = flask.request.args.get("ident")

    if db.tokenNeededExternal(pollIdent):
        if not token:
            return "403 NO TOKEN GIVEN"
        if not db.checkTokenValid(pollIdent, token):
            return "403 TOKEN INVALID"

    pollType    = db.getPollType(pollIdent)
    voteOptions = db.getVoteOptions(pollIdent)
    question    = db.queryQuestion(pollIdent)

    footer      = flask.Markup(flask.render_template("partials/footer.html"))
    header      = flask.Markup(flask.render_template("partials/header.html", websiteTitle="Vote"))
    tokenField  = flask.Markup(tokenInput.format(token=token))

    return flask.render_template("viewvote.html", header=header, footer=footer, \
                                    pollName=pollIdent, pollType=pollType, \
                                    question=question, \
                                    tokenNeeded=db.tokenNeededExternal(pollIdent), \
                                    voteOptions=voteOptions, tokenInput=tokenField)

@app.route('/viewresults')
def viewResults():
    '''Show results for a poll'''
    
    pollIdent    = flask.request.args.get("ident")
    pollType     = db.getPollType(pollIdent)
    voteOptions  = db.getVoteOptions(pollIdent)
    question     = db.queryQuestion(pollIdent)
    optionCounts = db.getPollOptionCounts(pollIdent)
    count        = sum(optionCounts)

    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html", websiteTitle="Results"))
    return flask.render_template("viewresults.html", header=header, footer=footer, \
                                    pollType=pollType, \
                                    pollName=pollIdent, \
                                    question=question, \
                                    totalCount=count, \
                                    optionsCountTupel=zip(voteOptions, optionCounts))

#@app.route('/pollinfoadmin')
#def viewInfoAdmin():
#    '''Page for managing polls'''
#    
#    pollIdent = flask.request.args.get("name")
#    
#
#    footer = flask.Markup(flask.render_template("partials/footer.html"))
#    header = flask.Markup(flask.render_template("partials/header.html"))
#    return flask.render_template("admin.html", footer=footer, header=header)


###### API PATHS #######

@app.route('/create')
def createPoll():
    '''This path is intended to be called from javascript'''
    
    # parse arguments #
    useTokens = bool(int(flask.request.args.get("tokens")))
    multi     = bool(int(flask.request.args.get("multi")))
    options   = flask.request.args.get("options").strip()
    question  = flask.request.args.get("q").strip()

    question = question.rstrip("?")

    # prevent identical options #
    options = ",".join(set(options.split(",")))

    # create poll in database #
    pollIdent, admToken = db.createPoll(options, question, useTokens, multi)

    return "{},{}".format(pollIdent, admToken)

@app.route('/checktoken')
def tokenCheck():
    '''This path is intended to be called from javascript'''

    # parse arguments #
    token = flask.request.args.get("token")
    pollIdent = db.pollNameFromToken(token)

    if not pollIdent:
        return ("", 214)
    elif db.checkAdmTokenValid(pollIdent, token):
        return "/pollinfoadmin?token={}&ident={}".format(token, pollIdent)
    elif db.checkTokenValid(pollIdent, token):
        return "/viewvote?token={}&ident={}".format(token, pollIdent)
    else:
        return ("", 213)

@app.route('/tokenget')
def tokenQuery():
    '''This path is intended to be called from javascript'''

    # parse arguments #
    pollIdent = flask.request.args.get("ident")
    admtoken  = flask.request.args.get("admToken")
    hostname  = getHostname()

    if not db.checkAdmTokenValid(pollIdent, admtoken):
        return "401 ADMTOKENINVALID"

    return "{host}viewvote?token={token}&ident={ident}".format( \
                                    token=db.genTokensExternal(pollIdent, count=1)[0], \
                                    ident=pollIdent, host=hostname)

@app.route('/vote')
def voteInPoll():
    pollIdent = flask.request.args.get("ident")
    token     = flask.request.args.get("token")
    options   = flask.request.args.get("selected")

    # check if multiple #
    if "," in options:
        options = list(filter(lambda x: x, options.split(",")))
        if len(options) > 1 and not db.isMultiChoice(pollIdent):
            raise ValueError("Cannot have more than one option in multiple choice")
    
    # try to infer poll from token if needed #
    if not pollIdent:
        pollIdent = db.pollNameFromToken(token)

    # check if poll exists #
    if not db.checkPollExists(pollIdent):
        raise AssertionError("PollIdent returned fron token doesn't exist")

    # check if auth need and/or valid #
    if not db.checkTokenValid(pollIdent, token) and db.tokenNeededExternal(pollIdent):
        return ("401 TOKEN INVALID", 403)
    
    # register vote #
    db.voteInPoll(pollIdent, options, token)

    # ack #
    return ("OK", 200)

##### STATIC FILES #####

@app.route('/static/<path:path>')
def staticFiles():
    send_from_directory('static', path)

@app.route('/defaultFavicon.ico')
def icon():
    return app.send_static_file('defaultFavicon.ico')

if __name__ == "__main__":
    db.init()
    app.run(host='0.0.0.0')
