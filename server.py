#!/usr/bin/python3
import flask

from   utils.cpwrap      import CFG

import utils.pollutils   as pollutils
import database.database as db

###### HTML Snippets #########
tokenWrapper   = "<div class='single-token'>{}</div>"
optionWrapper  = "<span><input class='vote-option' type=checkbox id={}>{}</input></span>"
noPollSelected = "<h1>No poll selected</h1>"
noPollWithName = "<h1>Poll {} not found.</h1>"
tokenInput     = "Token: <input type=text value='{}' id=token-field>"

infoSingleChoice = "SINGLE CHOICE"
infoMultipleChoice  = "MULTIPLE CHOICE"
resultsHref      = "'/results?name=%s'"

pollHasNoTokens   = "<div class='main-container'><h1>Poll does not use tokens.</h1></div>"
adminTokenInvalid = "<div class='main-container'><h1>Admin token invalid.</h1></div>"
redirectTo = '<html><meta http-equiv="refresh" content="0"; url="{}"></html>'

app = flask.Flask(CFG("appName"))

##### FRONTEND PATHS ########

@app.route('/')
def rootPage():
    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html"))
    return flask.render_template("startpage.html", header=header, footer=footer)

@app.route("/tokeninputview")
def tokenInputView():
    '''This path displays a creation dialog for new poll'''
    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html"))
    return flask.render_template("stringinput.html", header=header, footer=footer)

@app.route("/viewcreate")
def viewCreate():
    '''This path displays a creation dialog for new poll'''
    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html"))
    return flask.render_template("viewcreate.html")

@app.route('/viewpostcreate')
def viewPostCreate():
    '''Page for managing polls'''
    pollIdent  = flask.request.args.get("name")

    pollName    = db.getPollName(pollIdent)
    voteOptions = db.getVoteOptions(pollIdent)
    question    = db.getPollQuestion(pollIdent)
    tokens      = db.getPollStartingTokens(pollIdent)
    admToken    = db.getPollAdmToken(pollIdent)

    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html"))
    return flask.render_template("postcreate.html", header=header, footer=footer,
                                    pollName=pollName, tokens=tokens, admToken=admToken)

@app.route("/viewvote")
def viewVote():
    '''This path displays the actual options to vote'''
    
    inputToken = flask.request.args.get("token")
    pollIdent  = flask.request.args.get("name")

    pollName    = db.getPollName(pollIdent)
    pollType    = db.getPollType(pollIdent)
    voteOptions = db.getVoteOptions(pollIdent)

    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html"))
    return flask.render_template("vote.html", header=header, footer=footer, \
                                    pollName=pollName, pollType=pollType, \
                                    voteOptions=voteOptions, tokenInput=tokenInput)

@app.route('/viewresults')
def viewResults():
    '''Show results for a poll'''
    
    pollIdent  = flask.request.args.get("name")

    pollName    = db.getPollName(pollIdent)
    voteOptions = db.getVoteOptions(pollIdent)
    question    = db.getPollQuestion(pollIdent)
    count       = sum(db.getPollOptionCounts(pollIdent))

    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html"))
    return flask.render_template("results.html", header=header, footer=footer, \
                                    pollName=pollName, question=question, \
                                    totalVoteCount=count, voteOptions=voteOptions
                                    hostname=hostname, pollIdent=pollIdent)
@app.route('/pollinfoadmin')
def viewInfoAdmin():
    '''Page for managing polls'''
    
    pollIdent = flask.request.args.get("name")
    

    footer = flask.Markup(flask.render_template("partials/footer.html"))
    header = flask.Markup(flask.render_template("partials/header.html"))
    return flask.render_template("admin.html", footer=footer, header=header)


###### API PATHS #######

@app.route('/create')
def postCreatePoll():
    '''This path is intended to be called from javascript'''
    
    # parse arguments #
    useTokens = bool(int(arg("tokens")))
    multi     = bool(int(arg("multi")))
    question  = arg("q").strip()

    # sanatize input #
    if not question.endswith("?"):
        question += "?"

    # create poll in database #
    pollIdent = db.createPoll(getPollName(), arg("options").split(","), question, useTokens, multi)
    return pollIdent

@app.route('/tokenget')
def tokenQuery():
    '''This path is intended to be called from javascript'''

    # parse arguments #
    pollIdent = request.args.get("name")
    admtoken  = arg("admtoken")

    if not db.checkAdmTokenValid(admtoken):
        return "401 ADMTOKENINVALID"

    return db.genTokensExternal(pollIdent, count=1)

@app.route('/vote')
def voteInPoll():
    pollIdent = request.args.get("name")
    token     = request.args.get("token")
    
    # try to infer poll from token if needed #
    if not pollIdent:
        pollIdent = db.getPollFromToke(token)

    # check if poll exists #
    if not db.pollExists(pollIdent):
        return "404 POLLDOESNOTEXIST"


    # check if auth need and/or valid #
    if not db.checkTokenValidExternal(pollIdent, token):
        return "401 TOKEN INVALID"

    return "200 OK"

##### STATIC FILES #####

@app.route('/static/<path:path>')
def staticFiles():
    send_from_directory('static', path)

if __name__ == "__main__":
    db.init()
    app.run(host='0.0.0.0')
