def init():
    '''called at every startup, muse initialize the DB if nessesary'''
    
def tokenNeededExternal(poll_name):
    '''must return true if the give poll requires tokens'''

def markTokenUsedExternal(token, optStr=""):
    '''mark a token as read and save the answer given'''

def checkTokenValid(cursor, token, poll_name):
    '''return true if a token is valid and unused for this poll'''

def checkAdmTokenValid(poll_name, adm_token):
    '''check if an admin token is valid for this poll'''

def isValidAdmToken(adm_token):
    '''check if tkoken is an admin token for any poll'''

def isValidToken(token):
    '''check if tkoken is an used token for any poll'''

def pollNameFromToken(token):
    '''return the poll corresponding to a token or None if there is none'''

def getOptionsForPoll(c, poll_name, option):
    '''return the options for a given poll as a list'''

def incrementOption(cursor, poll_name, option):
    '''increment a given answer in a poll by one'''

def getOptionCount(c, poll_name, option):
    '''return the amount of answer-options for a given poll'''

def isMultiChoice(poll_name):
    '''return true if the poll is multiple choice'''

def insertOption(c, poll_name, option):
    '''add an options so it can later be incremented, functin must not commit changes'''

def insertToken(c, poll_name, token):
    '''add a single normal token to a poll, function must not commit changes'''

def insertAdminToken(c, poll_name, token):
    '''add a admin normal token to a poll, function must not commit changes'''

def getTokensExternal(poll_name):
    '''return all tokens for a given poll as a list'''

def getAdmToken(poll_name):
    '''query a single admin token for the given poll, if there is more than one return any one of them
       return None if no admin tokens exists for the given poll'''

def checkPollExists(poll_name):
    '''return true if the given poll exists''' 

def savePoll(poll_name, options, hasTokens, showResults, question, multi, date):
    '''save a single poll and all of it's parameters, function must not commit changes'''
