from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class AmortizacijaModel:

    def pronadji_amortizovanu_vrednost(self, id_os):
        tablename = 'amortizacija_opreme'
        try:
            connection = Database()
            select_columns = "SUM(iznos)"
            condition = "id_oprema"
            value = id_os
            pronadji = connection.select_sum(tablename, select_columns, condition, value)
            return pronadji
        except Error as e:
            Greske("Greska pronalazenje amortizovane vrednosti iz odredjenog naloga - AmortizacijaModel-pronadji_amortizovanu_vrednost", e)

    def da_li_postoji_amortizacija_posle_datuma(self, datum, mesec, godina):
        tablename = 'amortizacija'
        try:
            connection = Database()
            select_columns = "*"
            condition = "datum_amortizacije > '{}'".format(datum) + " or MONTH(datum_amortizacije) = '{}'".format(mesec) + " and YEAR(datum_amortizacije) = '{}'".format(godina) + " and broj_naloga like 'amortizacija%'"
            order = "idamortizacija"
            postoji = connection.select_condition(tablename, select_columns, condition, order)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje da li postoji amortizacija - AmortizacijaModel-da_li_postoji_armotizacija_posle_datuma", e)

    '''ovo je zbog provere prilikom unosa novog osnovnog sredstva da li postoji amortizacija posle datuma nabavke'''
    def amortizacija_posle_datuma(self, datum):
        tablename = 'amortizacija'
        try:
            connection = Database()
            select_columns = "*"
            condition = "datum_amortizacije >= '{}'".format(datum)
            order = "idamortizacija"
            postoji = connection.select_condition(tablename, select_columns, condition, order)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje da li postoji amortizacija - AmortizacijaModel-armotizacija_posle_datuma", e)

    def kreiraj_amortizaciju(self, datum, broj_naloga, kreirano):
        tablename = 'amortizacija'
        try:
            connection = Database()
            schema = "datum_amortizacije, broj_naloga, created_at"
            value = (datum, broj_naloga, kreirano)
            amortizacija = connection.insert(tablename, schema, value)
            return amortizacija
        except Error as e:
            Greske("Greska kreiranja amortizacije - AmortizacijaModel-kreiraj_amortizaciju",  e)

    ''' kao rezultat se dobija id poslednje amortizacije'''
    def pronadji_poslednji_zapis_amortizacije_u_tabeli(self):
        tablename = 'amortizacija'
        try:
            connection = Database()
            kolona = 'idamortizacija'
            amortizacija = connection.select_last_from_table(tablename, kolona)
            return amortizacija
        except Error as e:
            Greske("Greska trazenje poslednje amortizacije id - AmortizacijaModel-pronadji_poslednji_zapis_amortizacije_u_tabeli", e)

    ''' kao rezultat se dobija ceo zapis poslednje amortizacije u tabeli'''
    def pronadji_poslednju_amortizaciju(self):
        tablename = 'amortizacija'
        try:
            connection = Database()
            kolona = 'idamortizacija'
            amortizacija = connection.select_last_record_from_table(tablename, kolona)
            return amortizacija
        except Error as e:
            Greske("Greska trazenje poslednje amortizacije - AmortizacijaModel-pronadji_poslednji_zapis_amortizacije_u_tabeli", e)

    def pronadji_pretposlednji_zapis_amortizacije_u_tabeli(self):
        tablename = 'amortizacija'
        try:
            connection = Database()
            kolona = 'idamortizacija'
            amortizacija = connection.select_before_last_from_table(tablename, kolona)
            return amortizacija
        except Error as e:
            Greske("Greska trazenje poslednje amortizacije - AmortizacijaModel-pronadji_pretposlednji_zapis_amortizacije_u_tabeli", e)

    def unesi_u_tabelu_amortizacija_opreme(self, id_amortizacije, id_opreme, obracunata, stvarna):
        tablename = 'amortizacija_opreme'
        try:
            connection = Database()
            schema = "id_amortizacija, id_oprema, obracunata_amortizacija, stvarna_amortizacija"
            value = (id_amortizacije, id_opreme, obracunata, stvarna)
            connection.insert(tablename, schema, value)
        except Error as e:
            Greske("Greska kreiranja amortizacije opreme- AmortizacijaModel-unesi u tabelu amortizacija_opreme", e)

    def pronadji_amortizaciju(self, id_amortizacije):
        tablename = 'amortizacija'
        try:
            connection = Database()
            select_columns = "*"
            condition = "idamortizacija='{}'".format(id_amortizacije)
            order = "idamortizacija"
            postoji = connection.select_condition(tablename, select_columns, condition, order)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje da li postoji amortizacija - AmortizacijaModel-pronadji_amortizaciju", e)

    def pronadji_sve_uradjene_amortizacije(self):
        tablename = "amortizacija"
        try:
            connection = Database()
            select_columns = "*"
            order = "idamortizacija"
            postoji = connection.select(tablename, select_columns, order)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje svih amortizacija - AmortizacijaModel-pronadji_sve_uradjene_amortizacije)", e)

    def obrisi_izvestaj_amortizacije(self, idamortizacije):
        tablename = "izvestaj_amortizacije"
        # Brisanje iz baze podataka
        try:
            delete_condition = "id_amortizacije={}".format(idamortizacije)
            connection = Database()
            connection.delete(tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja izvestaja amortizacije - AmortizacijaModel - obrisi_izvestaj_amortizacije!", e)

    def obrisi_amortizacija_opreme(self, idamortizacije):
        tablename = "amortizacija_opreme"
        try:
            delete_condition = "id_amortizacija={}".format(idamortizacije)
            connection = Database()
            connection.delete(tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja amortizacija opreme - AmortizacijaModel - obrisi_amortizacija_opreme!", e)

    def obrisi_amortizacija(self, idamortizacije):
        tablename = "amortizacija"
        try:
            delete_condition = "idamortizacija={}".format(idamortizacije)
            connection = Database()
            connection.delete(tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja amortizacija - AmortizacijaModel - obrisi_amortizacija!", e)

    def pronadji_otpisane_vrednosti(self, idamortizacije):
        tablename = "amortizacija_opreme"
        try:
            connection = Database()
            select_columns = "id_oprema, obracunata_amortizacija"
            condition = "id_amortizacija={}".format(idamortizacije)
            order = "id_oprema"
            postoji = connection.select_condition(tablename, select_columns, condition, order)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje otpisane vrednosti - AmortizacijaModel-pronadji_otpisane_vrednosti", e)

    def pronadji_amortizaciju_po_datumu(self, datum):
        tablename = "amortizacija"
        try:
            connection = Database()
            select_columns = "idamortizacija"
            condition = "datum_amortizacije='{}'".format(datum)
            postoji = connection.select_condition(tablename, select_columns, condition)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje id amortizacije po datumu - AmortizacijaModel-pronadji_amortizaciju_po_datumu", e)

    def pronadji_amortizaciju_za_os(self, id_os):
        tablename = 'izvestaj_amortizacije'
        try:
            connection = Database()
            kolona = 'izvestaj_amortizacije.id_opreme, amortizacija.datum_amortizacije, amortizacija.broj_naloga, izvestaj_amortizacije.nabavna_vrednost, izvestaj_amortizacije.dosadasnji_otpis, izvestaj_amortizacije.tekuca_amortizacija'
            join = "amortizacija on izvestaj_amortizacije.id_amortizacije=amortizacija.idamortizacija"
            condition = "id_opreme='{}'".format(id_os)
            order = 'id_opreme'
            amortizacija = connection.select_where_join(kolona, tablename, join, condition, order)
            return amortizacija
        except Error as e:
            Greske("Greska trazenje amortizacije po id osnovnog sredstva- AmortizacijaModel-pronadji_amortizaciju_za_os", e)