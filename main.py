import sys
sys.path.append('tables')
from post_table import *
from project_config import *
from dbconnection import *
from people_table import *
from phones_table import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = PeopleTable()
        pht = PhonesTable()
        pst = PostTable()
        pt.create()
        pht.create()
        pst.create()
        return
    def db_insert_somethings(self):
        import numpy as np
        pt = PeopleTable()
        pht = PhonesTable()
        pst = PostTable()
        #[pst.insert_one([str(i), i + 1, str(i + 2)]) for i in np.random.randint(1, 10 ** 3, 300)]
        a=range(100)
        pt.insert_one(["Test", "Test", "Test"])
        pt.insert_one(["Test2", "Test2", "Test2"])
        pt.insert_one(["Test3", "Test3", "Test3"])
        [pst.insert_one([str(i), 'null', str(i),i]) for i in a]
        pht.insert_one([1, "123"])
        pht.insert_one([2, "123"])
        pht.insert_one([3, "123"])


    def db_drop(self):
        pht = PhonesTable()
        pt = PeopleTable()
        pst= PostTable()
        pst.drop()
        pht.drop()
        pt.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр людей;
    2 - сброс и инициализация таблиц;
    4 - таблица "Должности";
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        k=input("=> ").strip()
        if self.check_sql_injections(k):
            return
        return k

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9" and next_step != "4":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step
            
    def show_people(self):
        self.person_id = -1
        menu = """Просмотр списка людей!
№\tФамилия\tИмя\tОтчество"""
        print(menu)
        lst = PeopleTable().all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового человека;
    4 - удаление человека;
    5 - просмотр телефонов человека;
    9 - выход."""
        print(menu)
        return
    def add_phone(self,pers):
        k=input('Введите номер телефона: ')
        while True:
            try:
                while len(k) > 12:
                    print('Телефон должен содержать до 12 символов. Повторите попытку. ')
                    k = input('Введите номер телефона: ')
                if self.check_sql_injections(k):
                    return
                k = int(k)
                break
            except:
                print('Телефон должен содержать только цифры. Повторите попытку.')
                k = input('Введите номер телефона: ')
        pht=PhonesTable()
        pht.insert_one([pers, int(k)])
        return
    def drop_phone(self,pers):
        k=input('Введите номер телефона: ')
        while True:
            try:
                while len(k) > 12:
                    print('Телефон должен содержать до 12 символов. Повторите попытку. ')
                    k = input('Введите номер телефона: ')
                if self.check_sql_injections(k):
                    return
                int(k)
                break
            except:
                print('Телефон должен содержать только цифры. Повторите попытку.')
                k = input('Введите номер телефона: ')
        pht=PhonesTable()
        cur=self.connection.conn.cursor()
        # k="'"+k+"'"
        cur.execute(f'delete from {PhonesTable().table_name()} where person_id=%(id)s and phone = %(ph)s',
                    {'id':int(pers),'ph':k})
        self.connection.conn.commit()
        return
    def del_person(self):
        t=input('Введите id человека: ')
        if self.check_sql_injections(t):
            return
        while True:
            try:
                if self.check_sql_injections(t):
                    return
                t = int(t)
                # print(type(t))
                break
            except:
                print('ID должен содержать только цифры. Повторите попытку.')
                t = input('Введите ID человека: ')
        cur = self.connection.conn.cursor()
        cur.execute(f'delete from {PhonesTable().table_name()} where person_id=%(d)s',{'d':int(t)})
        cur.execute(f'delete from {PostTable().table_name()} where people_id=%(d)s',{'d':int(t)})
        cur.execute(f'delete from {PeopleTable().table_name()} where id=%(d)s',{'d':int(t)})
        self.connection.conn.commit()
        return
    def after_show_people(self, next_step):
        while True:
            if next_step == "4":
                self.del_person()
                return "1"
            elif next_step == "6" :
                self.add_phone(pers)
                next_step = "5"
            elif next_step == "7":
                self.drop_phone(pers)
                next_step = "5"
            elif next_step == "5":
                pers, next_step = self.show_phones_by_people()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_person(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        data = []
        data.append(input("Введите фамилию (1 - отмена): ").strip())
        if data[0] == "1":
            return
        while len(data[0].strip()) == 0 or len(data[0].strip()) >32:
            data[0] = input("Фамилия не может быть пустой и содержать более 32 символов! "
                            "Введите фамилию заново (1 - отмена):").strip()
            if data[0] == "1":
                return
        data.append(input("Введите имя (1 - отмена): ").strip())
        if data[1] == "1":
            return
        while len(data[1].strip()) == 0 or len(data[1].strip()) >32:
            data[1] = input("Имя не может быть пустым и содержать более 32 символов! Введите имя заново (1 - отмена):").strip()
            if data[1] == "1":
                return
        data.append(input("Введите отчество (1 - отмена):").strip())
        while len(data[2].strip()) >32:
            data[2] = input("Отчество не может содержать более 32 символов! Введите отчество заново (1 - отмена):").strip()
            if data[2] == "1":
                return
        for t in data:
            if self.check_sql_injections(t):
                return
        PeopleTable().insert_one(data)
        return

    def show_phones_by_people(self):
        if self.person_id == -1:
            while True:
                t = input("Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if self.check_sql_injections(t):
                    return
                while len(t.strip()) == 0:
                    t = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                    if self.check_sql_injections(t):
                        return
                if t == "0":
                    return "1"
                try:
                    person = PeopleTable().find_by_position(int(t))
                except:
                    print('ID должен быть числовым. Повторите попытку.')
                    continue
                if not person:
                    print("Введено число, неудовлетворяющее количеству людей!")
                else:
                    self.person_id = int(person[0])
                    self.person_obj = person
                    break
        print("Выбран человек: " + self.person_obj[1] + " " + self.person_obj[2] + " " + self.person_obj[3])
        print("Телефоны:")
        lst = PhonesTable().all_by_person_id(self.person_id)
        for i in lst:
            print(i[1])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    6 - добавление нового телефона;
    7 - удаление телефона;
    9 - выход."""
        print(menu)
        return self.person_id,self.read_next_step()

        return self.read_next_step()
    def add_post(self):
        data = []
        data.append(input("Введите департамент: ").strip())
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 20:
            data[0] = input("Департамент не может быть пустым или содержать более 20 символов! "
                            "Введите департамент заново:").strip()
        data.append(input("Введите id: ").strip())
        while True:
            try:
                if len(data[1].strip()) == 0:
                    data[1] = 'null'
                    break
                data[1]=int(data[1])
                break
            except:
                data[1] = input(
                        "ID должен быть "
                        "числовым. Повторите попытку").strip()
        data.append(input("Введите должность : ").strip())
        while len(data[2].strip()) == 0 or len(data[2].strip()) > 20:
            data[2] = input("Должность не может быть пустой или содержать более 20 символов! "
                            "Введите должность заново:").strip()
        data.append(input("Введите зарплату:").strip())
        while True:
            try:
                if len(data[3].strip()) == 0:
                    data[3]=0
                    break
                data[3] = int(data[3])
                break
            except:
                data[3] = input(
                    "Зарплата должна быть "
                    "числом. Повторите попытку").strip()
        for t in data:
            if self.check_sql_injections(t):
                return
        PostTable().insert_one(data)
        return

    def delete_post(self):
        data = []
        data.append(input("Введите департамент: ").strip())
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 20:
            data[0] = input("Департамент не может быть пустым или содержать более 20 символов! "
                            "Введите департамент заново:").strip()
        data.append(input("Введите должность : ").strip())
        while len(data[1].strip()) == 0 or len(data[1].strip()) > 20:
            data[1] = input("Должность не может быть пустой или содержать более 20 символов! "
                            "Введите должность заново:").strip()
        for t in data:
            if self.check_sql_injections(t):
                return
        cur = self.connection.conn.cursor()
        # data[0]="'"+data[0]+"'"
        # data[1] = "'" + data[1] + "'"
        cur.execute(f'delete from {PostTable().table_name()} where department=%(d)s and post=%(p)s'
                    ,{'d':data[0],'p':data[1]})
        self.connection.conn.commit()
        return
    def pst_connect(self):
        data = []
        data = []
        data.append(input("Введите департамент: ").strip())
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 20:
            data[0] = input("Департамент не может быть пустым или содержать более 20 символов! "
                            "Введите департамент заново:").strip()
        data.append(input("Введите id: ").strip())
        while len(data[1].strip()) == 0:
            data[1] = input("ID не может быть пустым! Введите ID заново:").strip()
            while True:
                try:
                    data[1] = int(data[1])
                    break
                except:
                    data[1] = input(
                        "ID должен быть "
                        "числовым. Повторите попытку").strip()
        data.append(input("Введите должность : ").strip())
        while len(data[2].strip()) == 0 or len(data[2].strip()) > 20:
            data[2] = input("Должность не может быть пустой или содержать более 20 символов! "
                            "Введите должность заново:").strip()
        for t in data:
            if self.check_sql_injections(t):
                return
        # data[0] = "'" + data[0] + "'"
        # data[2] = "'" + data[2] + "'"
        cur = self.connection.conn.cursor()
        cur.execute(f'update {PostTable().table_name()} set people_id=%(id)s where department=%(s1)s and post=%(s2)s',
                    {'id':int(data[1]),'s1':data[0],'s2':data[2]})
        self.connection.conn.commit()
        return

    def post_menu(self):
        print('Добавить должность: 1\nУдалить должность: 2\nПостранично посмотреть должности: 3\n'
              'Привязать должность к человеку: 4\n выход: 5')
        k=self.read_next_step()
        if k=='1':
            self.add_post()
        if k == '2':
            self.delete_post()
        if k=='3':
            PostTable().pst_read()
        if k=='4':
            self.pst_connect()
        if k=='5':
            return 1
        return
    def check_sql_injections(self,t):
        t=str(t)
        if 'select ' in t or 'union ' in t or 'order by ' in t or '=' in t or 'drop ' in t or 'delete ' in t or 'sleep ' \
                in t or 'update ' in t or 'alter ' in t or 'modify ' in t or ';' in t or 'create ' in t:
            return True
        else:
            return False
    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_people()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_person()
                current_menu = "1"
            elif current_menu == '4':
                if self.post_menu() is None:
                    current_menu = '4'
                else:
                    current_menu='0'
        print("До свидания!")    
        return
if __name__=='__main__':

    m = Main()
# m.db_init()
#
    m.main_cycle()
# m.db_drop()
# m.db_init()
# m.db_insert_somethings()
# m.pst_read()






