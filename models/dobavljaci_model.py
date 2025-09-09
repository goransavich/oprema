from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class DobavljaciModel:

    tablename = "dobavljaci"

    ''' Unos novog dobavljaca u bazu '''
    def insert_dobavljac(self, naziv, mesto):
        try:
            schema = "naziv, mesto"
            value = (naziv, mesto)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Problem unosa dobavljaca - DobavljaciModel.insert_dobavljac", e)

    ''' Citanje svih dobavljaca iz baze '''
    def read(self):
        try:
            connection = Database()
            select_columns = "*"
            order = "naziv"
            svi_nalozi = connection.select(self.tablename, select_columns, order)
            return svi_nalozi
        except Error as e:
            Greske("Greska citanje svih dobavljaca - DobavljaciModel.read", e)

    ''' Pronalazenje dobavljaca po ID'''
    def find_dobavljac(self, iddobavljaca):
        try:
            connection = Database()
            select_columns = "*"
            condition = 'iddobavljaci'
            value = iddobavljaca
            svi_nalozi = connection.select_where(self.tablename, select_columns, condition, value)
            return svi_nalozi
        except Error as e:
            Greske("Greska pronalazenje dobavljaca po ID - DobavljaciModel.find_dobavljac", e)

    ''' Azuriranje naziva i mesta dobavljaca '''
    def update_dobavljac(self, naziv, mesto, iddobavljaca):
        # Ažuriranje baze podataka
        try:
            set_condition = 'naziv="{}"'.format(naziv) + ', mesto="{}"'.format(mesto)
            filter_condition = ' iddobavljaci={}'.format(iddobavljaca)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Problem prilikom izmena dobavljaca - DobavljaciModel.update_dobavljac", e)

    ''' trazenje dobavljaca u tabeli nabavka, da se proveri da li moze da se brise izabrani dobavljac. Ako postoji u ovoj tabeli onda ne moze da se brise'''
    def dobavljac_postoji_u_nabavci(self, id_dobavljaca):
        try:
            tabela = 'nabavka'
            connection = Database()
            select_columns = "*"
            condition = 'dobavljac_id'
            value = id_dobavljaca
            svi_nalozi = connection.select_where(tabela, select_columns, condition, value)
            return svi_nalozi
        except Error as e:
            Greske("Greska pronalazenje dobavljaca po ID u tabeli nabavka- DobavljaciModel.dobavljac_postoji_u_nabavci", e)

    ''' Brisanje dobavljaca '''
    def delete_dobavljac(self, iddobavljaca):
        # Brisanje iz baze podataka
        try:
            delete_condition = "iddobavljaci={}".format(iddobavljaca)
            connection = Database()
            connection.delete(self.tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja dobavljaca - DobavljaciModel.delete_dobavljac", e)