from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class NalogRashodModel:
    tablename = "rashod"

    ''' Unos novog naloga za rashod opreme u bazu '''

    def insert_nalog_rashod(self, broj_rashoda, datum):
        try:
            schema = "datum, broj_rashoda"
            value = (datum, broj_rashoda)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Problem unosa naloga rashoda - NalogRashodModel - insert_nalog_rashod", e)

    def poslednji_nalog_rashod(self):
        try:
            kolona = "idrashod"
            connection = Database()
            rezultat = connection.select_last_from_table(self.tablename, kolona)
            return rezultat
        except Error as e:
            Greske("Problem pronalaska poslednjeg naloga rashoda - NalogRashodModel - poslednji_nalog_rashod", e)

    def pronadji_naloge_rashod(self, od, do):
        try:
            select_columns = "*"
            column = 'datum'
            start_date = od
            end_date = do
            order = 'datum'
            connection = Database()
            pronadjen_nalog = connection.select_between(self.tablename, select_columns, column, start_date, end_date, order)
            return pronadjen_nalog
        except Error as e:
            Greske("Pronalazenje u bazi naloga pomocu ID kako bi se uzeli podaci za taj nalog i stavke naloga koje se unose u njega NalogRashodModel ", e)

    ''' Pronadji nalog po id '''

    def find_nalog(self, id_naloga):
        try:
            select_columns = "*"
            condition = 'idrashod'
            value = id_naloga
            connection = Database()
            pronadjen_nalog = connection.select_where(self.tablename, select_columns, condition, value)
            return pronadjen_nalog
        except Error as e:
            Greske("Pronalazenje u bazi naloga pomocu ID kako bi se uzeli podaci za taj nalog i stavke naloga koje se unose u njega NalogUnosModel", e)

