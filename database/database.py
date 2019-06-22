import sqlite3
import os.path
import random
import string

from utils.cpwrap import CFG

def connectDB():
    conn = sqlite3.connect(CFG("dbname"))
    return (conn, conn.cursor())

def closeDB(conn, cursor=None):
    conn.commit()
    conn.close()

def queryAll(cursor, reqString, *args):
    try:
        if len(args) > 0:
            cursor.execute(reqString, *args)
        else:
            cursor.execute(reqString)
        ret = cursor.fetchall()
        if ret:
            return ret
    except IndexError:
        return []

def queryOne(cursor, reqString, *args):
    try:
        if len(args) > 0:
            cursor.execute(reqString, *args)
        else:
            cursor.execute(reqString)
        ret = cursor.fetchone()
        if ret:
            return ret[0]
    except IndexError:
        return None

def queryQuestion(pollIdent):
    conn, c = connectDB()
    req = "SELECT question from {} WHERE name = ?".format(CFG("poll_table_name"))
    tmp = queryOne(c, req, (pollIdent,))
    conn.close()
    return tmp

def tokenNeededExternal(pollIdent):
    conn, c = connectDB()
    tmp = checkTokenNeeded(c, pollIdent)
    conn.close()
    return tmp

def markTokenUsedExternal(pollIdent, token, optStr=""):
    conn, c = connectDB()
    tname = CFG("tokens_table_name")
    req = "UPDATE {} SET \"options_selected\"=? WHERE token=? AND name=?".format(tname)
    c.execute(req, (optStr, token, pollIdent))
    closeDB(conn)

def init():
    if os.path.isfile(CFG("dbname")):
        return
    conn, c = connectDB()
    c.execute("CREATE TABLE " + CFG("poll_table_name") + "(\
                    name text,\
                    options text,\
                    has_tokens integer,\
                    show_results integer,\
                    question text,\
                    multi integer, \
                    date text)"\
                    )
    c.execute("CREATE TABLE {}(name_option text, count integer)".format(CFG("options_table_name")))
    c.execute("CREATE TABLE {}(token text, name text, options_selected text)".format(CFG("tokens_table_name")))
    c.execute("CREATE TABLE {}(adm_token text, pollIdent text)".format(CFG("admintoken_table_name")))
    closeDB(conn)

def checkTokenValid(pollIdent, token):
    conn, c = connectDB()
    req = "SELECT name, options_selected from {} where token=?".format(CFG("tokens_table_name"))
    answer = queryAll(c, req, (token,))
    closeDB(conn)
    return answer and answer[0][0] == pollIdent

def checkAdmTokenValid(pollIdent, adm_token):
    conn, c = connectDB()
    req = "SELECT pollIdent from {} where adm_token=?".format(CFG("admintoken_table_name"))
    answer = queryOne(c, req, (adm_token,))
    closeDB(conn)
    return answer == pollIdent

def isValidAdmToken(adm_token):
    conn, c = connectDB()
    req = "SELECT *  from {} where adm_token=?".format(CFG("admintoken_table_name"))
    answer = bool(queryOne(c, req, (adm_token,)))
    closeDB(conn)
    return answer

def isValidToken(token):
    conn, c = connectDB()
    req = "SELECT * from {} where token=?".format(CFG("tokens_table_name"))
    answer = bool(queryOne(c, req, (token,)))
    closeDB(conn)
    return answer

def pollNameFromToken(token):
    conn, c = connectDB()
    req = "SELECT name from {} where token=?".format(CFG("tokens_table_name"))
    answer = queryOne(c, req, (token,))
    if not answer:
        req = "SELECT pollIdent from {} where adm_token=?".format(CFG("admintoken_table_name"))
        answer = queryOne(c, req, (token,))
    closeDB(conn)
    return answer

def getPollType(ident):
    if isMultiChoice(ident):
        return "MULTIPLE CHOICE"
    else:
        return "SINGLE CHOICE"

def getPollQuestion(ident):
    return "TODOpollquestion"

def getPollStartingTokens(ident):
    raise NotImplementedError()

def getPollAdmToken(ident):
    raise NotImplementedError()
    
def checkTokenNeeded(cursor, pollIdent):
    req = "SELECT has_tokens FROM {} WHERE name=?".format(CFG("poll_table_name"))
    return queryOne(cursor, req, (pollIdent,)) == 1

def incrementOption(cursor, pollIdent, option):
    key = pollIdent+"-"+option
    req = "UPDATE {} SET count=count+1 WHERE name_option=?".format(CFG("options_table_name"))
    cursor.execute(req, (key,))

def decrementOption(cursor, pollIdent, option):
    key = pollIdent+"-"+option
    req = "UPDATE {} SET count=count-1 WHERE name_option=?".format(CFG("options_table_name"))
    cursor.execute(req, (key,))

def isMultiChoice(pollIdent):
    conn, c = connectDB()
    req = "SELECT multi FROM {} WHERE name=?".format(CFG("poll_table_name"))
    print(pollIdent)
    print(type(queryOne(c, req, (pollIdent,))))
    #  TODO WTF IS GOING ON HERE
    ret = queryOne(c, req, (pollIdent,)) == 1
    closeDB(conn)
    return ret

def tokenUndoVote(pollIdent, options, token):
    conn, c = connectDB()
    tname = CFG("tokens_table_name")
    req = "SELECT options_selected FROM {} WHERE token=? AND name=?".format(tname)
    ret = queryOne(c, req, (token, pollIdent))
    print(ret)
    if ret == "NONE":
        return
    else:
        for opt in ret.split(","):
            decrementOption(c, pollIdent, opt)

    closeDB(conn)

def voteInPoll(pollIdent, options, token="DUMMY_INVALID_TOKEN"):
    conn, c = connectDB()

    # normalize input #
    if type(options) != list:
        options = [options]

    # if token already has a vote undo it #
    tokenUndoVote(pollIdent, options, token)

    # remember answer for token #
    markTokenUsedExternal(pollIdent, token, ",".join(options))

    # increment relevant options #
    for opt in options:
        incrementOption(c, pollIdent, opt)

    closeDB(conn)

def getPollOptionCounts(ident):
    options = getVoteOptions(ident)
    optionCounts = []

    for opt in options:
        print(opt)
        optionCounts += [getOptionCount(ident, opt)]

    return optionCounts
    

def getOptionCount(pollIdent, option):
    conn, c = connectDB()
    key = pollIdent + "-" + option
    req = "SELECT count FROM {table} WHERE name_option=?".format(table=CFG("options_table_name"))
    count = queryOne(c, req, (key,))

    if count == None:
        raise AssertionError("Unknown answer for poll. WTF?")

    conn.close()
    return count

#def getResults(pollIdent):
#    conn, c = connectDB()
#    req = "SELECT options from {} where name=?".format(CFG("poll_table_name"))
#    options = queryOne(c, req, (pollIdent,))
#
#    if not options:
#        raise LookupError("Poll '{}' not found in DB".format(pollIdent))
#
#    total = 0
#    options = options.split(",")
#    results = dict()
#    for opt in options:
#        count = getOptionCount(c, pollIdent, opt)
#        total += int(count)
#        results.update({opt:count})
#
#    conn.close()
#    return (results, total)

def insertOption(c, pollIdent, option):
    key = pollIdent + "-" + option
    count = 0
    params = (key, count)
    req = "INSERT INTO {} VALUES (?, ?)".format(CFG("options_table_name"))
    c.execute(req, params)

def getTokensExternal(pollIdent):
    req = "SELECT token FROM {} WHERE name=?".format(CFG("tokens_table_name"))
    conn, c = connectDB()
    tmp = queryAll(c, req, (pollIdent,))
    conn.close()
    if not tmp:
        return None
    else:
        return map(lambda s: s[0], tmp)

def genSingleToken(length=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def genTokens(c, pollIdent, count=10):
    tokens = [ genSingleToken() for x in range(0,count) ]
    for token in tokens:
        name = pollIdent 
        options_selected = "NONE"
        params = (token, name, options_selected)
        req = "INSERT INTO {} VALUES (?, ?, ?)".format(CFG("tokens_table_name"))
        c.execute(req, params)
    return tokens

def genTokensExternal(pollIdent, count=1):
    conn, c = connectDB()
    tok = genTokens(c, pollIdent, count)
    closeDB(conn)
    return tok

def createAdminToken(c, pollIdent):
    adm_token = genSingleToken()
    params = (adm_token, pollIdent)
    req = "INSERT INTO {} VALUES (?, ?)".format(CFG("admintoken_table_name"))
    c.execute(req, params)
    return adm_token

def getAdmToken(pollIdent):
    conn, c = connectDB()
    req = "SELECT adm_token FROM {} WHERE pollIdent=?".format(CFG("admintoken_table_name"))
    admtok = queryOne(c, req, (pollIdent,))
    closeDB(conn)
    return admtok

def checkPollExists(pollIdent):
    conn, c = connectDB()
    req = "SELECT EXISTS( SELECT 1 FROM {} WHERE name=?)".format(CFG("poll_table_name"))
    tmp = queryOne(c, req, (pollIdent,))
    conn.close()
    return tmp

def createPoll(options, question, has_tokens, multi, openresults=True):

    # create random poll id #
    maxAttempts = 5
    for i in range(0, maxAttempts + 1):
        pollIdent = genSingleToken(10)
        if not checkPollExists(pollIdent):
            break
        if i == maxAttempts:
            raise AssertionError("Unable to find random token, wtf!?")

    # open db connection #
    conn, c = connectDB()

    # actual poll #
    pollIdent   = genSingleToken(length=8)
    date        = "NONE"
    showResults = openresults
    params      = (pollIdent, options, has_tokens, showResults, question, multi, date)

    # build database query #
    req = "INSERT INTO {} VALUES (?,?,?,?,?,?,?)".format(CFG("poll_table_name"))
    c.execute(req, params)

    # tokens if needed #
    tokens = []
    if has_tokens:
        tokens = genTokens(c, pollIdent)

    # adminAccessToken #
    admToken = createAdminToken(c, pollIdent)

    # update options #
    for opt in options.split(","):
        insertOption(c, pollIdent, opt)
    
    closeDB(conn)
    return (pollIdent, admToken)

def getVoteOptions(pollIdent):
    conn, c = connectDB()
    req = "SELECT options FROM {} WHERE name=?".format(CFG("poll_table_name"))
    options = queryOne(c, req, (pollIdent,))
    if options == None:
        return None
    options = options.split(",")
    closeDB(conn)
    return options
