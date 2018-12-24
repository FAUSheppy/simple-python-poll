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

def buildPostCreatePoll(poll_name):
    pass

def buildAskToken(poll_name):
    pass

def buildVoteInPoll(poll_name):
    pass

def buildPostVote(poll_name):
    pass

def buildShowResults(poll_name):
    pass
