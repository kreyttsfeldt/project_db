from dbtable import *
from main import Main
from people_table import *
import re
class PostTable(DbTable):
    def table_name(self):
        if re.search(r'^([a-zA-Z]|_)*$', self.dbconn.prefix):
            return self.dbconn.prefix + 'post_table'
        else:
            raise Exception('Myerror')

    def columns(self):
        return {"department": ["varchar(20)"],
                "salary": ["integer", "NOT NULL"],
                "post": ["varchar(20)", "NOT NULL"],
                'people_id': ['integer', f"REFERENCES {PeopleTable().table_name()}(id)"]}

    def primary_key(self):
        return ['department', "post"]
    def pst_read(self):
        cur_page = 0
        print(f'Я страница {cur_page+1} таблицы {self.table_name()}')
        [print(i) for i in self.all()[:20]]
        k = input('Если хотите:\nввести номер страницы, введите 1;\nполучить следущую страницу, введите 2;'
                      '\nполучить предыдущую страницу, введите 3;\n')
        if Main().check_sql_injections(k):
            return
        k=int(k)
        while True:
            if k==1:
                t=input('Введите номер страницы:\n ')
                if Main().check_sql_injections(t):
                    return
                t=int(t)
                cur_page = t-1
                print(f'Я страница {cur_page+1} таблицы {self.table_name()}')
                [print(i) for i in self.all()[cur_page*20:(cur_page+1)*20]]
            elif k==2:
                cur_page = cur_page + 1
                print(f'Я страница {cur_page+1} таблицы {self.table_name()}')
                [print(i) for i in self.all()[cur_page*20:(cur_page+1)*20]]
            elif k==3:
                print(f'Я страница {cur_page+1} таблицы {self.table_name()}')
                cur_page = cur_page - 1
                [print(i) for i in self.all()[cur_page*20:(cur_page+1)*20]]
            else: return
            k = input('Если хотите:\nввести номер страницы, введите 1;\nполучить следущую страницу, введите 2;'
                          '\nполучить предыдущую страницу, введите 3;\n')
            if Main().check_sql_injections(k):
                return
            k = int(k)
