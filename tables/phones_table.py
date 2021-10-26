from dbtable import *

class PhonesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "phones"

    def columns(self):
        return {"person_id": ["integer", f"REFERENCES {self.dbconn.prefix}people(id)"],
                "phone": ["varchar(12)", "NOT NULL"]}
    
    def primary_key(self):
        return ['person_id', 'phone']    

    def table_constraints(self):
        return ["PRIMARY KEY(person_id, phone)"]

    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += f" WHERE person_id = {str(pid)}"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()           

