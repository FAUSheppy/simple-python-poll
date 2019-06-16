### CHECK FOR SOMETHING ###
def voteTokenNeeded(poll_name):
    '''must return true if the give poll requires tokens'''

def markTokenUsed(token, optStr=""):
    '''mark a token as read and save the answer given'''

def checkVoteTokenValid(token, poll_name):
    '''return true if a token is valid and unused for this poll'''

def checkAdmTokenValid(poll_name, adm_token):
    '''check if an admin token is valid for this poll'''

def checkPollExists(poll_name):
    '''return true if the given poll exists''' 

def isValidAdmToken(adm_token):
    '''check if tkoken is an admin token for any poll'''

def isValidToken(token):
    '''check if tkoken is an used token for any poll'''

def isMultiChoice(poll_name):
    '''return true if the poll is multiple choice'''


### ADD STUFF TO DATABASE ###
def init():
    '''called at every startup, muse initialize the DB if nessesary'''

def insertOption(poll_name, option):
    '''add an options so it can later be incremented, functin must not commit changes'''

def insertToken(poll_name, token):
    '''add a single normal token to a poll, function must not commit changes'''

def insertAdminToken(c, poll_name, token):
    '''add a admin normal token to a poll, function must not commit changes'''

def incrementOption(poll_name, option):
    '''increment a given answer in a poll by one'''

def savePoll(poll_name, options, hasTokens, showResults, question, multi, date):
    '''save a single poll and all of it's parameters, function must not commit changes'''


### QUERY INFORMATION ###
def getTokensForPoll(poll_name):
    '''return all tokens for a given poll as a list'''

def getAdmTokenForPoll(poll_name):
    '''query a single admin token for the given poll, if there is more than one return any one of them return None if no admin tokens exists for the given poll'''

def getOptionsForPoll(poll_name, option):
    '''return the options for a given poll as a list'''

def getOptionCount(poll_name, option):
    '''return the amount of answer-options for a given poll'''

def pollNameFromToken(token):
    '''return the poll corresponding to a token or None if there is none'''
