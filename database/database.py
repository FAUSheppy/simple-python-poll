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

def queryQuestion(poll_name):
    conn, c = connectDB()
    req = "SELECT question from {} WHERE name = ?".format(CFG("poll_table_name"))
    tmp = queryOne(c, req, (poll_name,))
    conn.close()
    return tmp

def tokenNeededExternal(poll_name):
    conn, c = connectDB()
    tmp = checkTokenNeeded(c, poll_name)
    conn.close()
    return tmp

def markTokenUsedExternal(token, optStr=""):
    conn, c = connectDB()
    req = "UPDATE {} SET \"options_selected\"=? WHERE token=?".format(CFG("tokens_table_name"))
    c.execute(req, (optStr, token,))
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
    c.execute("CREATE TABLE {}(adm_token text, poll_name text)".format(CFG("admintoken_table_name")))
    closeDB(conn)

def checkTokenValid(cursor, token, poll_name):
    req = "SELECT name, options_selected from {} where token=?".format(CFG("tokens_table_name"))
    answer = queryAll(cursor, req, (token,))
    return answer and answer[0][0] == poll_name and answer[0][1] == 'NONE'

def checkAdmTokenValid(poll_name, adm_token):
    conn, c = connectDB()
    req = "SELECT poll_name from {} where adm_token=?".format(CFG("admintoken_table_name"))
    answer = queryOne(c, req, (adm_token,))
    closeDB(conn)
    return answer == poll_name

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
        req = "SELECT poll_name from {} where adm_token=?".format(CFG("admintoken_table_name"))
        answer = queryOne(c, req, (token,))
    closeDB(conn)
    return answer

def getPollName(ident):
    return "TODOpollname"

def getPollType(ident):
    return "TODOpolltype"

def getPollQuestion(ident):
    return "TODOpollquestion"

def getPollOptionCounts(ident):
    return [1,3,4]

def getPollStartingTokens(ident):
    return ["lol","lol"]

def getPollAdmToken(ident):
    return "admtoken"
    
def checkTokenNeeded(cursor, poll_name):
    req = "SELECT has_tokens FROM {} WHERE name=?".format(CFG("poll_table_name"))
    return queryOne(cursor, req, (poll_name,)) == 1

def incrementOption(cursor, poll_name, option):
    key = poll_name+"-"+option
    req = "UPDATE {} SET count=count+1 WHERE name_option=?".format(CFG("options_table_name"))
    cursor.execute(req, (key,))

def isMultiChoice(poll_name):
    conn, c = connectDB()
    req = "SELECT multi FROM {} WHERE name=?".format(CFG("poll_table_name"))
    ret = queryOne(c, req, (poll_name,)) == 1
    closeDB(conn)
    return ret

def vote(poll_name, options_string, token_used="DUMMY_INVALID_TOKEN"):
    conn, c = connectDB()

    # check token
    token_valid = checkTokenValid(c, token_used, poll_name)
    if not token_valid and checkTokenNeeded(c, poll_name):
        raise PermissionError("Poll requires valid token.")
    markTokenUsedExternal(token_used, options_string)

    # save changes
    # lambda x: x -> röfl :D
    options = list(filter(lambda x: x, options_string.split(",")))
    # check if multi-choice
    if len(options) > 1:
        if not isMultiChoice(poll_name):
            raise ValueError("multiple options for single choice")

    for opt in options:
        incrementOption(c, poll_name, opt)

    closeDB(conn)

def getOptionCount(c, poll_name, option):
    key = poll_name + "-" + option
    req = "SELECT count FROM {table} WHERE name_option=?".format(table=CFG("options_table_name"))
    count = queryOne(c, req, (key,))
    if count == None:
        raise AssertionError("Unknown answer for poll. WTF?")
    return count;

def getResults(poll_name):
    conn, c = connectDB()
    req = "SELECT options from {} where name=?".format(CFG("poll_table_name"))
    options_str = queryOne(c, req, (poll_name,))

    if not options_str:
        raise LookupError("Poll '{}' not found in DB".format(poll_name))

    total = 0
    options = options_str.split(",")
    results = dict()
    for opt in options:
        count = getOptionCount(c, poll_name, opt)
        total += int(count)
        results.update({opt:count})

    conn.close()
    return (results, total)

def insertOption(c, poll_name, option):
    key = poll_name + "-" + option
    count = 0
    params = (key, count)
    req = "INSERT INTO {} VALUES (?, ?)".format(CFG("options_table_name"))
    c.execute(req, params)

def getTokensExternal(poll_name):
    req = "SELECT token FROM {} WHERE name=?".format(CFG("tokens_table_name"))
    conn, c = connectDB()
    tmp = queryAll(c, req, (poll_name,))
    conn.close()
    return tmp

def genSingleToken(length=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def genTokens(c, poll_name, count=1):
    tokens = [ genSingleToken() for x in range(0,count) ]
    for token in tokens:
        name = poll_name 
        options_selected = "NONE"
        params = (token, name, options_selected)
        req = "INSERT INTO {} VALUES (?, ?, ?)".format(CFG("tokens_table_name"))
        c.execute(req, params)
    return tokens

def genTokensExternal(poll_name, count=1):
    conn, c = connectDB()
    tok = genTokens(c, poll_name, count)
    closeDB(conn)
    return tok

def createAdminToken(c, poll_name):
    adm_token = genSingleToken()
    params = (adm_token, poll_name)
    req = "INSERT INTO {} VALUES (?, ?)".format(CFG("admintoken_table_name"))
    c.execute(req, params)

def getAdmToken(poll_name):
    conn, c = connectDB()
    req = "SELECT adm_token FROM {} WHERE poll_name=?".format(CFG("admintoken_table_name"))
    admtok = queryOne(c, req, (poll_name,))
    closeDB(conn)
    return admtok

def checkPollExists(poll_name):
    conn, c = connectDB()
    req = "SELECT EXISTS( SELECT 1 FROM {} WHERE name=?)".format(CFG("poll_table_name"))
    tmp = queryOne(c, req, (poll_name,))
    conn.close()
    return tmp

def createPoll(options_arr, question, has_tokens, multi, openresults=True):

    # create random poll id #
    poll_name = genSingleToken(10)

    if checkPollExists(poll_name):
        raise RuntimeError("Cannot create poll, because the poll already exists.")
    conn, c = connectDB()

    # actual poll
    name = poll_name
    options = ",".join(options_arr)
    date = "NONE"
    show_results = openresults
    params = (name, options, has_tokens, show_results, question, multi, date) 
    req = "INSERT INTO {} VALUES (?,?,?,?,?,?,?)".format(CFG("poll_table_name"))
    c.execute(req, params)

    # tokens if needed
    tokens = []
    if has_tokens:
        tokens = genTokens(c, poll_name)

    # adminAccessToken
    createAdminToken(c, poll_name)

    # update options
    for opt in options_arr:
        insertOption(c, poll_name, opt)
    
    closeDB(conn)
    return poll_name

def getVoteOptions(poll_name):
    conn, c = connectDB()
    req = "SELECT options FROM {} WHERE name=?".format(CFG("poll_table_name"))
    options_str = queryOne(c, req, (poll_name,))
    if options_str == None:
        return None
    options = options_str.split(",")
    closeDB(conn)
    return options
