from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class SistemModel:
    tablename = "bekap"

    def insert_bekap(self, datum):
        try:
            schema = "datum_bekapa"
            value = (datum,)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Greska prilikom unosa datuma bekapa - SistemModel", e)

    def find_last(self):
        try:
            select_columns = "*"
            order = "datum_bekapa DESC"
            connection = Database()
            pronadjen_korisnik = connection.select(self.tablename, select_columns, order)
            return pronadjen_korisnik
        except Error as e:
            Greske("Greska prilikom trazenja poselednjeg bekapa - SistemModel", e)