from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class KontoModel:

    tablename = "konto"

    ''' Unos novog konta u bazu '''
    def insert_konto(self, oznaka, naziv):
        try:
            schema = "oznaka, naziv"
            value = (oznaka, naziv)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Problem unosa konta - KontoModel.insert_konto", e)

    ''' Citanje svih konta iz baze '''
    def read(self):
        try:
            connection = Database()
            select_columns = "*"
            order = "oznaka"
            sva_konta = connection.select(self.tablename, select_columns, order)
            return sva_konta
        except Error as e:
            Greske("Greska citanje svih konta - KontoModel.read", e)

    ''' Azuriranje oznake i naziva konta '''
    def update_konto(self, oznaka, naziv, idkonto):
        # Ažuriranje baze podataka
        try:
            set_condition = 'oznaka="{}"'.format(oznaka) + ', naziv="{}"'.format(naziv)
            filter_condition = ' idkonto={}'.format(idkonto)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Problem prilikom izmena konta - KontoModel.update_konto", e)

    ''' provera da li postoji kontu u nekom osnovnom sredstvu, ako postoji - ne moze da se brise '''
    def konto_postoji_u_osnovnom_sredstvu(self, id_konta):
        try:
            tabela = 'osnovna_sredstva'
            connection = Database()
            select_columns = "*"
            condition = 'konto_id'
            value = id_konta
            svi_nalozi = connection.select_where(tabela, select_columns, condition, value)
            return svi_nalozi
        except Error as e:
            Greske("Greska pronalazenje konta po ID u tabeli osnovna sredstva- KontoModel.konto_postoji_u_osnovnom_sredstvu", e)

    ''' Brisanje konta '''
    def delete_konto(self, idkonto):
        # Brisanje iz baze podataka
        try:
            delete_condition = "idkonto={}".format(idkonto)
            connection = Database()
            connection.delete(self.tablename, delete_condition)
        except Error as e:
            Greske("Greska brisanja konta - KontoModel.delete_konto!", e)
