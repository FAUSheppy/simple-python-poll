import os
HTML_DIR = "html_js_partials/"

def readPartial(name):
    if not name.endswith((".html",".js",".css")):
        name = name + ".html"
    path = os.path.join(HTML_DIR, name)
    with open(path,"r") as f:
        return f.read()

def buildTokenPartial(tokens):
    tokenPartial = ""
    if tokens:
        for tk in tokens:
            if type(tk) == tuple:
                tk = tk[0]
            tokenPartial += tokenWrapper.format(tk)
    return tokenPartial

startPage      = readPartial("base").format(title="simple-poll", body=readPartial("start-page"))
pollCreator    = readPartial("base").format(title="poll-create", body=readPartial("create-poll-partial"))

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

voteFailed = readPartial("base").format(title="Vote Failed", body=readPartial("vote-failed"))

redirectTo = '<html><meta http-equiv="refresh" content="0"; url="{}"></html>'
