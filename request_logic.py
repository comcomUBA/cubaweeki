import requests
import json
import sqlite3
import datetime
from db import Edit, DB, LastRun

db = DB("CubaWeeki.db")
db.make_tables_if_not_exists()
URL = "https://www.cubawiki.com.ar/api.php"
PROPS = "userid|user|title|ids|comment|timestamp"
last = db.get_last(LastRun)
timestamp = last.timestamp if last else "2025-03-21T12:00:00Z"
WEEKY_START = datetime.datetime.fromisoformat(timestamp) + datetime.timedelta(seconds=1)
print(f"FETCHING ALL EDITS FROM {WEEKY_START} TAKE CARE!!!")

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

res = []
for e in get_recent_edits(None):
    res.extend(e)

if res:
    for r in e:
        db.add(Edit(**r))
    last = LastRun(timestamp=res[0]["timestamp"])
    print(f"Added {len(res)} EDITS, last timestamp : {last.timestamp}")
    db.add(last)
    db.commit()
else:
    "No data found!"
