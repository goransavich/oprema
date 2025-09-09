from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class StopeModel:

    tablename = "stope"

    ''' Unos novoe stope u bazu '''
    def insert_stopa(self, oznaka, naziv, procenat):
        try:
            schema = "oznaka, naziv, procenat"
            value = (oznaka, naziv, procenat)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Problem unosa stope - StopaModel.insert_stopa", e)

    ''' Citanje svih stopa iz baze '''
    def read(self):
        try:
            connection = Database()
            select_columns = "*"
            sve_stope = connection.select(self.tablename, select_columns)
            return sve_stope
        except Error as e:
            Greske("Greska citanje svih stopa - StopeModel.read", e)

    ''' Azuriranje oznake, naziva i procenta stope '''
    def update_stopa(self, oznaka, naziv, procenat, idstopa):
        # Ažuriranje baze podataka
        try:
            set_condition = 'oznaka="{}"'.format(oznaka) + ', naziv="{}"'.format(naziv) + ', procenat="{}"'.format(procenat)
            filter_condition = ' idstope={}'.format(idstopa)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Problem prilikom izmena stope - StopaModel.update_stopa", e)

    ''' ovde ide provera da li je stopa dodeljena nekom osnovnom sredstvu, ako jeste, ne moze da se brise '''
    def stopa_postoji_u_osnovnom_sredstvu(self, id_stope):
        try:
            tabela = 'osnovna_sredstva'
            connection = Database()
            select_columns = "*"
            condition = 'stopa_id'
            value = id_stope
            svi_nalozi = connection.select_where(tabela, select_columns, condition, value)
            return svi_nalozi
        except Error as e:
            Greske("Greska pronalazenje stope po ID u tabeli osnovna sredstva- StopeModel.stopa_postoji_u_osnovnom_sredstvu", e)

    ''' Brisanje stope '''
    def delete_stopa(self, idstopa):
        # Brisanje iz baze podataka
        try:
            delete_condition = "idstope={}".format(idstopa)
            connection = Database()
            connection.delete(self.tablename, delete_condition)
        except Error as e:
            Greske("Greska prilikom brisanja stope - StopaModel.delete_stopa", e)

    def find_stopa(self, idstope):
        # Pronalazenje stope po id u baze podataka
        try:
            select_columns = "procenat"
            condition = "idstope"
            value = idstope
            connection = Database()
            pronadjena_stopa = connection.select_where(self.tablename, select_columns, condition, value)
            return pronadjena_stopa
        except Error as e:
            Greske("Greska prilikom trazenja stope po ID stope - StopaModel.find_stopa", e)