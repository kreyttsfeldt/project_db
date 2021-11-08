from dbtable import *
import re
class PeopleTable(DbTable):

    def table_name(self):
        if re.search(r'^([a-zA-Z]|_)*$', self.dbconn.prefix):
            return self.dbconn.prefix + "people"
        else:
            raise Exception('Myerror')

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
        sql += f" LIMIT 1 OFFSET %(d)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {'d':num-1})
        return cur.fetchone()       
    
