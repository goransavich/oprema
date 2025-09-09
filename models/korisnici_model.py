from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class KorisniciModel:

    tablename = "korisnici"

    ''' Unos novos mesta u bazu '''
    def insert_korisnika(self, oznaka):
        try:
            schema = "ime"
            value = (oznaka,)
            connection = Database()
            connection.insert(self.tablename, schema, value)
        except Error as e:
            Greske("Problem unosa zaposlenog - KorisnikModel.insert_korisnika", e)

    def pronadji_korisnika(self, id_korisnika):
        select_columns = "*"
        condition = 'idkorisnici'
        value = id_korisnika
        connection = Database()
        pronadjene_stavke = connection.select_where(self.tablename, select_columns, condition, value)
        return pronadjene_stavke


    ''' Citanje svih zaposlenih iz baze '''
    def read(self):
        try:
            connection = Database()
            order = "idkorisnici"
            select_columns = "*"
            svi_zaposleni = connection.select(self.tablename, select_columns, order)
            return svi_zaposleni
        except Error as e:
            Greske("Greska citanje svih zaposlenih - KorisniciModel.read", e)

    ''' Azuriranje zaposlenih '''
    def update_korisnika(self, ime, idzaposlenog):
        # Ažuriranje baze podataka
        try:
            set_condition = 'ime="{}"'.format(ime)
            filter_condition = ' idkorisnici={}'.format(idzaposlenog)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Problem prilikom izmene zaposlenog - KorisniciModel.update_model", e)

    ''' provera da li korisnik postoji u osnovnom sredstvu, zbog brisanja '''
    def korisnik_postoji_u_osnovnom_sredstvu(self, id_korisnika):
        try:
            tabela = 'osnovna_sredstva'
            connection = Database()
            select_columns = "*"
            condition = 'zaposleni_id'
            value = id_korisnika
            svi_nalozi = connection.select_where(tabela, select_columns, condition, value)
            return svi_nalozi
        except Error as e:
            Greske("Greska pronalazenje korisnika po ID u tabeli osnovna sredstva- MestoModel.korisnik_postoji_u_osnovnom_sredstvu", e)

    ''' Brisanje zaposlenih '''
    def delete_korisnik(self, idzaposlenog):
        # Brisanje iz baze podataka
        try:
            delete_condition = "idkorisnici={}".format(idzaposlenog)
            connection = Database()
            connection.delete(self.tablename, delete_condition)
        except Error as e:
            Greske("Greska prilikom brisanja zaposlenog - KorisniciModel.delete_korisnik", e)