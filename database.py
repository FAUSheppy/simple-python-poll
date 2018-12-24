import sqlite3
from cpwrap import CFG

# DB-structure:
# db-poll:    name | options | tokens? | openresults? | date
# db-options: name+option | count
# db-tokens   token | name | used | option(s)

def connectDB():
    conn = sqlite3.connect(CFG("dbname"))
    return (conn, conn.cursor())

def closeDB(conn, cursor=None):
    conn.commit()
    conn.close()

def queryOne(cursor, reqString):
    try:
        cursor.execute(reqString)
        return cursor.fetchone()[0]
    except IndexError:
        return None

def init():
    conn, c = connectDB()
    c.execute("CREATE TABLE" + CFG("poll_table_name") + '''(\
                    name text,\
                    options text,\
                    has_tokens integer,\
                    show_results integer,\
                    date text)'''
                    )
    c.execute("CREATE TABLE {}(name_option text, count)".format(CFG("options_table_name"))
    c.execute("CREATE TABLE {}(token text, name text, options_selected text)".format(CFG("tokens_table_name"))
    closeDB(conn)

def checkTokenValid(cursor, token, poll_name):
    req = "SELECT name from {} where token={}".format(CFG("tokens_table_name"),token)
    answer = queryOne(cursor, req)
    return answer and answer == poll_name

def checkTokenNeeded(cursor, poll_name):
    req = "SELECT has_tokens from {} where name={}".format(CFG("poll_table_name"),poll_name)
    return queryOne(cursor, req) == "1";

def incrementOption(cursor, poll_name, option):
    key = poll_name+"-"+opt
    req = "UPDATE {} SET count = count + 1 WHERE name_option={}".format(CFG("options_table_name"), key)
    c.execute(req)

def vote(poll_name, options_string, token_used="DUMMY_INVALID_TOKEN")
    conn, c = connectDB()
    # check token
    token_valid = checkTokenValid(c, token_used, poll_name)
    if not token_valid and checkTokenNeeded():
        raise PermissionError("Poll requires valid token.")

    # save changes
    options = options_string.split(",")
    for opt in options:
        incrementOption(cursor, poll_name, opt)

    closeDB(conn)

def getOptionCount(c, poll_name, option)
    key = poll_name + "-" + option
    req = "SELECT count WHERE name_option={}".format(CFG("options_table_name"), key)
    return queryOne(c, req)

def getResults(poll_name):
    conn, c = connectDB()
    req = "SELECT options from {} where name={}".format(CFG("poll_table_name"), poll_name)
    options_str = queryOne(c, req)

    if not options_str:
        raise LookupError("Poll '{}' not found in DB".format(poll_name))

    total = 0
    options = options_str.split(",")
    results = dict()
    for opt in options:
        count = getOptionCount()
        total += count
        ret.update({opt:count})

    conn.close()
    return results

def insertOption(c, poll_name, option):
    key = poll_name + option
    count = 0
    req = "INSERT INTO {} VALUE ({}, {})".format(CFG("options_table_name"), key, count)
    c.execute(req)

def genSingleToken(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def genTokens(c, poll_name, count=5):
    tokens = [ genSingleToken() for x in range(0,5) ]
    for token in tokens:
        req = "INSERT INTO {} VALUE ({}, {}, {})".format(CFG("tokens_table_name"), poll_name, token , "NONE")
        c.execute(req)

def createPoll(poll_name, options_arr, has_tokens, openresults=True):
    conn, c = connectDB()

    # actual poll
    req = "INSERT INTO {} VALUE ({}, {}, {}, {})".format(CFG("poll_table_name")\
                    poll_name,\
                    ",".join(options_arr),\
                    str(int(has_tokens)),\
                    str(int(openresults)),\
                    "NONE")
    c.execute(r)

    # tokens if needed
    if has_tokens:
        genTokens(c, poll_name)

    # update options
    for opt in options_arr:
        insertOption(c, poll_name, opt)
    
    closeDB(conn)
