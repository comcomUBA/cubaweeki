import sqlite3
import unittest
from collections import defaultdict

class Base:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    @classmethod
    def _from_db(cls, *args):
        kwargs = {k: v for k, v in zip(cls.__annotations__, args)}
        obj = cls(**kwargs)
        return obj

    def __repr__(self):
        keys = self.__class__().__annotations__.keys()
        d = self.__dict__
        annotations = ', '.join([f"{key}:{d[key]}" for key in keys if key in d.keys()])
        return annotations
        

class Edit(Base):
    id: int = None
    userid: int
    user: str
    title: str
    pageid: int
    revid: int
    timestamp: str
    comment: str

class LastRun(Base):
    id: int = None
    timestamp: str


class DB:
    def __init__(self, url):
        self.conn = sqlite3.connect(url)
        self.tables = list(Base.__subclasses__())
        self.annotations = defaultdict(dict)

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def add(self, obj):
        cur = self.conn.cursor()
        c = obj.__class__
        table = c.__name__
        annotations = [key for key, v in c.__annotations__.items()
            if key in obj.__dict__.keys()]
        fields = ', '.join(annotations)
        placeholders = ', '.join([f":{a}" for a in annotations])
        cmd = f"INSERT INTO {table} ({fields}) VALUES ({placeholders})"
        cur.execute(cmd, obj.__dict__)
        cur.close()

    def all(self, clss):
        cur = self.conn.cursor()
        cmd = f"SELECT * FROM {clss.__name__}"
        rows = cur.execute(cmd).fetchall()
        objs = [clss._from_db(*row) for row in rows]
        cur.close()
        return objs

    def get(self, clss, id):
        cur = self.conn.cursor()
        cmd = f"SELECT * FROM {clss.__name__} WHERE id = ?"
        res = cur.execute(cmd, (id,)).fetchone()
        if res:
            res = clss._from_db(*res)
        cur.close()
        return res
    
    def get_last(self, clss):
        cur = self.conn.cursor()
        cmd = (f"SELECT * FROM {clss.__name__} WHERE id in"
            f" (SELECT max(id) FROM {clss.__name__})"
        )
        res = cur.execute(cmd).fetchone()
        if res:
            res = clss._from_db(*res)
        cur.close()
        return res
            
    def make_tables(self):
        self._make_table("CREATE TABLE")

    def make_tables_if_not_exists(self):
        self._make_table("CREATE TABLE IF NOT EXISTS")

    def _make_table(self, cmd):
        cur = self.conn.cursor()
        for c in self.tables:
            cur.execute(self.create_table_cmd_from(c, cmd))
        cur.close()

    def create_table_cmd_from(self, c, cmd):
        translations = {
            str: "TEXT",
            int: "INTEGER"
        }
        fields = ', '.join([
                f"{key} {translations[type]} "
                f"{'primary key' if key == 'id' else ''}"
            for key, type in c.__annotations__.items()])
        return f"{cmd} {c.__name__} ({fields})"

        
class TestDB(unittest.TestCase):
    def test_table_creation(self):
        d = DB("tst.db")
        d.make_tables()
        e = Edit(userId = 10, user = "fran")
        d.add(e)
        
    def test_table_creation(self):
        d = DB("tst1.db")
        e = d.get(Edit, 1)
        self.assertEqual(e.user, "Fran")
