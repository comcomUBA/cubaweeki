import requests
import json
import sqlite3

URL = "https://www.cubawiki.com.ar/api.php"
PROPS = "userid|user|title|ids|comment|timestamp"
WEEKY_START = "2025-01-21T12:00:00Z"

def get_recent_edit(con):
    params = {
         "action": "query",
         "list": "recentchanges",
         "format": "json",
         "rcprop": PROPS,
         "rctype": "edit",
         "rcend":  WEEKY_START
    }
    if con:
        params.update(con)
    req = requests.get(URL, params)
    return json.loads(req.content)

def get_recent_edits(con):
    while True:
        print(f"Getting edits with {con}")
        res = get_recent_edit(con)
        changes = res["query"]["recentchanges"]
        print(f"Got {len(changes)} edits!!")
        yield(changes)
        con = res.get("continue", None)
        if not con:
            return


print(list(get_recent_edits(None)))
