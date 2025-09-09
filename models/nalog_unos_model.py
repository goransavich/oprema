from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class NalogUnosModel:
    tablename = "nabavka"

    ''' Unos novog naloga unosa OS u bazu '''

    def insert_unos(self, dobavljac, broj_fakture, datum_fakture, datum_kreiranja):
        try:
            schema = "dobavljac_id, broj_dokumenta, datum_dokumenta, datum_kreiranja, proknjizen"
            proknjizen = 0
            value = (dobavljac, broj_fakture, datum_fakture, datum_kreiranja, proknjizen)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Problem unosa naloga unosa OS - NalogUnosModel", e)

    def pronadji_sve_nabavke(self):
        try:
            select_columns = "nabavka.idnabavka, dobavljaci.naziv, nabavka.broj_dokumenta, nabavka.datum_dokumenta, nabavka.proknjizen"
            join = "dobavljaci on nabavka.dobavljac_id=dobavljaci.iddobavljaci"
            order_by = "datum_dokumenta"
            connection = Database()
            pronadjen_nalog = connection.select_join(self.tablename, select_columns, join, order_by)
            return pronadjen_nalog
        except Error as e:
            Greske("Pronalazenje u bazi naloga pomocu ID kako bi se uzeli podaci za taj nalog i stavke naloga koje se unose u njega NalogUnosModel", e)

    ''' Pronadji nalog po id '''
    def find_nalog(self, id_naloga):
        try:
            select_columns = "nabavka.broj_dokumenta, nabavka.datum_dokumenta, nabavka.proknjizen, dobavljaci.naziv, dobavljaci.mesto "
            condition = 'idnabavka={}'.format(id_naloga)
            join = "dobavljaci on nabavka.dobavljac_id=dobavljaci.iddobavljaci"
            order_by = "idnabavka"
            connection = Database()
            pronadjen_nalog = connection.select_where_join(select_columns, self.tablename, join, condition, order_by)
            return pronadjen_nalog
        except Error as e:
            Greske("Pronalazenje u bazi naloga pomocu ID kako bi se uzeli podaci za taj nalog i stavke naloga koje se unose u njega NalogUnosModel", e)

    def pronadji_naloge(self, od, do):
        try:
            select_columns = "*"
            column = 'datum_naloga'
            start_date = od
            end_date = do
            order = 'datum_naloga'
            connection = Database()
            pronadjen_nalog = connection.select_between(self.tablename, select_columns, column, start_date, end_date, order)
            return pronadjen_nalog
        except Error as e:
            Greske("Pronalazenje u bazi naloga pomocu ID kako bi se uzeli podaci za taj nalog i stavke naloga koje se unose u njega NalogUnosModel ", e)

    # pronalazenje u bazi poslednjeg unetog naloga
    def pronadji_poslednji(self):
        try:
            select_columns = "*"
            condition = 'idnabavka'
            value = '(SELECT max(idnabavka) FROM nabavka)'
            connection = Database()
            pronadjen_nalog = connection.select_last(self.tablename, select_columns, condition, value)
            return pronadjen_nalog
        except Error as e:
            Greske("Greška prilikom povezivanja na bazu podataka! Pronalazenje u bazi poslednjeg unetog naloga - NalogUnosModel", e)

    def delete_nalog(self, id_fakture):
        # Brisanje iz baze podataka
        try:
            delete_condition = "idnabavka='{}'".format(id_fakture)
            connection = Database()
            connection.delete(self.tablename, delete_condition)
        except Error as e:
            Greske("Greška prilikom brisanja naloga unosa! - NalogUnosModel delete_nalog", e)

    def proknjizi_nabavku(self, id_fakture):
        # Ažuriranje baze podataka
        try:
            set_condition = 'proknjizen=1'
            filter_condition = 'idnabavka={}'.format(id_fakture)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Greska prilikom azuriranje fakture - NalogUnosModel update_nalog", e)