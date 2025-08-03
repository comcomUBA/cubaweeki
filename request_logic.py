import requests
import json
import sqlite3
import datetime
from db import Edit, DB, LastRun

URL = "https://www.cubawiki.com.ar/api.php"
PROPS = "userid|user|title|ids|comment|timestamp"

def get_recent_edit(con, weeky_start):
    params = {
         "action": "query",
         "list": "recentchanges",
         "format": "json",
         "rcprop": PROPS,
         "rctype": "edit",
         "rcend":  weeky_start
    }
    if con:
        params.update(con)
    req = requests.get(URL, params)
    return json.loads(req.content)

def get_recent_edits(con, weeky_start):
    while True:
        # print(f"Getting edits with {con}")
        res = get_recent_edit(con, weeky_start)
        changes = res["query"]["recentchanges"]
        # print(f"Got {len(changes)} edits!!")
        yield(changes)
        con = res.get("continue", None)
        if not con:
            return

db = DB("CubaWeeki.db")
db.make_tables_if_not_exists()

def get_db_edits():
    return db.all(Edit)

def do_fetch_run():
    last = db.get_last(LastRun)
    timestamp = last.timestamp if last else "2025-03-21T12:00:00Z"
    WEEKY_START = datetime.datetime.fromisoformat(timestamp) + datetime.timedelta(seconds=1)
    print(f"fetching edits since {WEEKY_START}")

    res = []
    for e in get_recent_edits(None, WEEKY_START):
        res.extend(e)

    edits = []
    if res:
        for r in res:
            edit = Edit(**r)
            db.add(edit)
            edits.append(edit)

        last = LastRun(timestamp=res[0]["timestamp"])
        print(f"added {len(res)} edits, saving last run: {last.timestamp}")
        db.add(last)

        db.commit()

    return edits

if __name__ == "__main__":
    do_fetch_run()
