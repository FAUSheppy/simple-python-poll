# main page
#    center: new poll
# create poll page:
#    - options already added - delete button -
#    - new option -
#    - cancle --------------------- submitt --
#    - use tokens [ ]
# post create page:
#    center: link to poll (copyable)
# ask token page:
#    center: enter token
# poll page:
#    - option 1 [ ]
#    - option n [ ]
#    - ok button ---- cancle button -
# post poll page:
#    - vote counted!
#    - if openresults link to results page -
# results-page
#    - option 1 [count] percent
#    - option n [count] percent

from cpwrap import CFG
import database as db
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
    body = readPartial("create-poll-partial") % poll_name
    return readPartial("base").format(title="poll-create", body=body)

def buildPostCreatePoll(poll_name, tokens):
    return "<h1>Poll Created!</h1>"

def buildVoteInPoll(poll_name):
    script = readPartial("vote-js-partial.js")
    optionWrapper = "<span><input class='vote-option' type=checkbox id={}>{}</input></span>"
    options = db.getOptions(poll_name)
    if poll_name == "" or poll_name == None:
        return "<h1>No poll selected</h1>"
    elif options == None:
        return "<h1>Poll {} not found.</h1>".format(poll_name)
    voteOptions = ""
    for opt in options:
        voteOptions += optionWrapper.format(opt, opt)
    body = readPartial("vote-partials").format(script=script, poll_name=poll_name, voteoptions=voteOptions)
    return readPartial("base").format(title="voting", body=body)


def buildPostVote(poll_name, token, selectedOptions):
    try:
        db.vote(poll_name, selectedOptions, token)
    except PermissionError:
        return "<h1>Vote failed, token invalid</h1>"
    body = "<h1>Vote Done {}<h1>".format(poll_name)
    return readPartial("base").format(title=poll_name, body=body)

def buildShowResults(poll_name):
    pass
