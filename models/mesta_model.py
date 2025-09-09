from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class MestaModel:

    tablename = "mesto"

    ''' Unos novos mesta u bazu '''
    def insert_mesto(self, oznaka):
        try:
            schema = "oznaka"
            value = (oznaka,)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Problem unosa mesta - MestaModel.insert_mesto", e)

    def pronadji_mesto(self, id_lokacije):
        select_columns = "*"
        condition = 'idmesto'
        value = id_lokacije
        connection = Database()
        pronadjene_stavke = connection.select_where(self.tablename, select_columns, condition, value)
        return pronadjene_stavke

    ''' Citanje svih mesta iz baze '''
    def read(self):
        try:
            connection = Database()
            order = "idmesto"
            select_columns = "*"
            sva_mesta = connection.select(self.tablename, select_columns, order)
            return sva_mesta
        except Error as e:
            Greske("Greska citanje svih mesta - MestaModel.read", e)

    ''' Azuriranje oznake mesta '''
    def update_mesto(self, oznaka, idmesto):
        # Ažuriranje baze podataka
        try:
            set_condition = 'oznaka="{}"'.format(oznaka)
            filter_condition = ' idmesto={}'.format(idmesto)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Problem prilikom izmena mesta - MestoModel.update_mesto", e)

    '''ovde ide provera da li je lokacija dodeljena nekom osnovnom sredstvu, ako jeste - onda ne moze da se brise'''
    def lokacija_postoji_u_osnovnom_sredstvu(self, id_lokacije):
        try:
            tabela = 'osnovna_sredstva'
            connection = Database()
            select_columns = "*"
            condition = 'lokacija_id'
            value = id_lokacije
            svi_nalozi = connection.select_where(tabela, select_columns, condition, value)
            return svi_nalozi
        except Error as e:
            Greske("Greska pronalazenje lokacije po ID u tabeli osnovna sredstva- MestoModel.lokacija_postoji_u_osnovnom_sredstvu", e)

    ''' Brisanje mesta '''
    def delete_mesto(self, idmesto):
        # Brisanje iz baze podataka
        try:
            delete_condition = "idmesto={}".format(idmesto)
            connection = Database()
            connection.delete(self.tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja mesta - MestoModel.delete_mesto", e)
