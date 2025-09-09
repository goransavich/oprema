from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class RashodModel:
    def kreiraj_rashod(self, datum_naloga, broj, danasnji_datum):
        tablename = 'rashod'
        try:
            connection = Database()
            schema = "datum, broj_rashoda, proknjizen, datum_rada"
            value = (datum_naloga, broj, 0, danasnji_datum)
            connection.insert(tablename, schema, value)
        except Error as e:
            Greske("Greska kreiranja naloga rashoda - RashodModel-kreiraj_rashod_nalog", e)

    # pronalazenje u bazi poslednjeg unetog naloga
    def pronadji_poslednji(self):
        tablename = 'rashod'
        try:
            select_columns = "*"
            condition = 'idrashod'
            value = '(SELECT max(idrashod) FROM rashod)'
            connection = Database()
            pronadjen_nalog = connection.select_last(tablename, select_columns, condition, value)
            return pronadjen_nalog
        except Error as e:
            Greske(
                "Greška prilikom povezivanja na bazu podataka! Pronalazenje u bazi poslednjeg unetog naloga rashoda - RashodController pronadji_poslednji",
                e)

    def pronadji_sve_uradjene_rashode(self):
        tablename = "rashod"
        try:
            connection = Database()
            select_columns = "*"
            order = "idrashod"
            postoji = connection.select(tablename, select_columns, order)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje svih rashoda - RashodModel-pronadji_sve_uradjene_rashode)", e)

    def pronadji_nalog_rashoda(self, id_rashoda):
        tablename = "rashod"
        try:
            connection = Database()
            select_columns = "*"
            condition = 'idrashod'
            value = id_rashoda
            postoji = connection.select_where(tablename, select_columns, condition, value)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje naloga rashoda - RashodModel-pronadji_nalog_rashoda)", e)

    def unesi_rashod_opreme(self, rashod_id, id_osn_sredstvo, nabavna, otpisana, amortizovana):
        tablename = "rashod_opreme"
        try:
            connection = Database()
            schema = "id_rashoda, id_osnovnog_sredstva, nabavna, otpisana, amortizacija_r"
            value = (rashod_id, id_osn_sredstvo, nabavna, otpisana, amortizovana)
            connection.insert(tablename, schema, value)
        except Error as e:
            Greske("Greska kreiranja rashoda opreme - RashodModel-unesi_rashod_opreme", e)

    def os_postoji_u_tabeli_rashod(self, id_os):
        tablename = 'rashod_opreme'
        try:
            connection = Database()
            select_columns = "*"
            condition = 'id_osnovnog_sredstva'
            value = id_os
            postoji = connection.select_where(tablename, select_columns, condition, value)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje da li postoji osnovno sredstvo u tabeli rashod opreme - RashodModel-os_postoji_u_tabeli_rashod)", e)

    def obrisi_os_rashod_opreme(self, id_os):
        tablename="rashod_opreme"
        try:
            delete_condition = "id_osnovnog_sredstva={}".format(id_os)
            connection = Database()
            connection.delete(tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja osnovnog sredstva iz tabele rashod_opreme - RashodModel - obrisi_os_rashod_opreme!", e)

    def azuriraj_tabela_rashod_proknjizen(self, nalog_id):
        tablename="rashod"
        try:
            connection = Database()
            set_condition = "proknjizen=1"
            filter_condition = "idrashod={}".format(nalog_id)
            connection.update(tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Greska rashodovanje osnovnog sredstva - RashodModel-rashoduj_osnovno_sredstvo", e)

    def obrisi_nalog_rashoda(self, nalog_id):
        tablename = "rashod"
        try:
            delete_condition = "idrashod={}".format(nalog_id)
            connection = Database()
            connection.delete(tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja naloga iz tabele rashod - RashodModel - obrisi_nalog_rashoda", e)

    def obrisi_stavke_rashod_opreme(self, nalog_id):
        tablename = "rashod_opreme"
        try:
            delete_condition = "id_rashoda={}".format(nalog_id)
            connection = Database()
            connection.delete(tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja stavki rashoda iz tabele rashod_opreme - RashodModel - obrisi_sravke_rashod_opreme", e)

    def proveri_oprema_u_nalogu_rashoda(self, nalog_id):
        tablename = 'rashod_opreme'
        try:
            connection = Database()
            select_columns = "*"
            condition = 'id_rashoda'
            value = nalog_id
            postoji = connection.select_where(tablename, select_columns, condition, value)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje da li postoji osnovno sredstvo u tabeli rashod opreme - RashodModel-os_postoji_u_tabeli_rashod)", e)

    def podaci_rashod_opreme(self, nalog_id):
        tablename = 'rashod_opreme'
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, rashod_opreme.nabavna, rashod_opreme.amortizacija_r, rashod_opreme.otpisana, konto.oznaka"
            where_condition = "id_rashoda={}".format(nalog_id)
            join1 = "osnovna_sredstva on rashod_opreme.id_osnovnog_sredstva=osnovna_sredstva.idosnovna_sredstva"
            join2 = "konto on  osnovna_sredstva.konto_id=konto.idkonto"
            order = "osnovna_sredstva.inventarni_broj"
            postoji = connection.select_where_join(select_columns,tablename, join1, where_condition, order, join2)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje svih osnovnih sredstava za rashod po id rashoda u tabeli rashod_opreme - RashodModel-podaci_rashod_opreme)", e)

    def podaci_rashod_opreme_grupisani(self, nalog_id):
        tablename = 'rashod_opreme'
        try:
            connection = Database()
            select_columns = "konto.oznaka, sum(rashod_opreme.nabavna), sum(rashod_opreme.amortizacija_r), sum(rashod_opreme.otpisana)"
            where_condition = "id_rashoda={}".format(nalog_id)
            join1 = "osnovna_sredstva on rashod_opreme.id_osnovnog_sredstva=osnovna_sredstva.idosnovna_sredstva"
            join2 = "konto on  osnovna_sredstva.konto_id=konto.idkonto"
            order = "konto.oznaka"
            #order = "osnovna_sredstva.inventarni_broj"
            group = "konto.oznaka"
            postoji = connection.select_where_join_group(select_columns,tablename, join1, where_condition, order, group, join2)
            return postoji
        except Error as e:
            Greske("Greska pronalazenje svih osnovnih sredstava za rashod po id rashoda grupisano po kontu u tabeli rashod_opreme - RashodModel-podaci_rashod_opreme_grupisani)", e)

    def trazenje_rashoda_po_os(self, id_os):
        tablename = 'rashod_opreme'
        try:
            connection = Database()
            select_columns = "rashod_opreme.id_osnovnog_sredstva, rashod.datum, rashod.broj_rashoda, rashod_opreme.nabavna, rashod_opreme.otpisana, rashod_opreme.amortizacija_r"
            where_condition = "id_osnovnog_sredstva={}".format(id_os)
            join1 = "rashod on rashod_opreme.id_rashoda=rashod.idrashod"
            order = "rashod_opreme.id_osnovnog_sredstva"
            # order = "osnovna_sredstva.inventarni_broj"
            #group = "konto.oznaka"
            postoji = connection.select_where_join(select_columns, tablename, join1, where_condition, order)
            return postoji
        except Error as e:
            Greske(
                "Greska pronalazenje rashoda po osnovnom sredstvu - RashodModel-trazenje_rashoda_po_os)",
                e)
