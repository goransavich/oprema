from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class FirmaModel:

    tablename = "firma"

    ''' Citanje firme iz baze '''
    def read(self):
        try:
            connection = Database()
            select_columns = "*"
            podaci_firma = connection.select(self.tablename, select_columns)
            return podaci_firma
        except Error as e:
            Greske("Greska citanje svih firmi - FirmaModel", e)
