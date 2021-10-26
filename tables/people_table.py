from dbtable import *

class PeopleTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "people"

    def columns(self):
        return {"id": [ "SERIAL", "PRIMARY KEY"],
                "last_name": ["varchar(32)", "NOT NULL"],
                "first_name": ["varchar(32)", "NOT NULL"],
                "second_name": ["varchar(32)"],
                }

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += f" LIMIT 1 OFFSET {num - 1}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()       
    
