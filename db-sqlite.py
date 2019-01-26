### CHECK FOR SOMETHING ###
def voteTokenNeeded(poll_name):
    req = "SELECT has_tokens FROM ? WHERE name = ?"
    params = (CFG("poll_table_name"), poll_name)

def markTokenUsed(token, optStr=""):
    req = "UPDATE ? SET options_selected = ? WHERE token = ?"
    params = (CFG("tokens_table_name"), optStr, token)

def checkVoteTokenValid(token, poll_name):
    req = "SELECT name, options_selected from ?0 where token=?"
    params = (CFG("tokens_table_name"), token)

def checkAdmTokenValid(poll_name, adm_token):
    req = "SELECT poll_name from ? where adm_token = ?"
    params = (CFG("admintoken_table_name"), adm_token)

def checkPollExists(poll_name):


def isValidAdmToken(adm_token):
    req = "SELECT *  from ? where adm_token = ?"
    params = (CFG("admintoken_table_name"), adm_token)


def isValidToken(token):

def isMultiChoice(poll_name):


### ADD STUFF TO DATABASE ###
def init():

def insertOption(poll_name, option):

def insertToken(poll_name, token):

def insertAdminToken(c, poll_name, token):

def incrementOption(poll_name, option):

def savePoll(poll_name, options, hasTokens, showResults, question, multi, date):


### QUERY INFORMATION ###
def getTokensForPoll(poll_name):

def getAdmTokenForPoll(poll_name):

def getOptionsForPoll(poll_name, option):

def getQuestionForPoll(pollname):
    req     = "SELECT question from ? WHERE name = ?"
    params  = (CFG("poll_table_name"), poll_name)

def getOptionCount(poll_name, option):

def pollNameFromToken(token):
