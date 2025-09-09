from mysql.connector import Error
from connections.connections import Database
from views.greske import Greske


class OsnovnoSredstvoModel:
    tablename = "osnovna_sredstva"

    def unos_novog_osnovnog_sredstva(self, inventarni_broj, naziv, nabavna_vrednost, otpisana_vrednost, status, konto, stopa, zaposleni, lokacija, faktura, aktiviran, nab_otpisana_vrednost):
        schema = "inventarni_broj, naziv, nabavna_vrednost, otpisana_vrednost, status, konto_id, stopa_id, zaposleni_id, lokacija_id, nabavka_id, aktiviran, nabavka_otpisana_vrednost"
        value = (inventarni_broj, naziv, nabavna_vrednost, otpisana_vrednost, status, konto, stopa, zaposleni, lokacija, faktura, aktiviran, nab_otpisana_vrednost)
        connection = Database()
        connection.insert(self.tablename, schema, value)

    def read(self):
        try:
            connection = Database()
            select_columns = "*"
            sva_os = connection.select(self.tablename, select_columns)
            return sva_os
        except Error as e:
            Greske("Greska citanje svih osnovnih sredstava - OsnovnoSredstvoModel-read", e)

    def sva_oprema_knjiga_os(self):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.nabavna_vrednost, osnovna_sredstva.nabavka_otpisana_vrednost,  stope.oznaka, stope.procenat, nabavka.datum_dokumenta, nabavka.broj_dokumenta"
            join1 = "stope on osnovna_sredstva.stopa_id=stope.idstope"
            join2 = "nabavka on osnovna_sredstva.nabavka_id=nabavka.idnabavka"
            order = "osnovna_sredstva.idosnovna_sredstva"
            sva_os = connection.select_two_join(self.tablename, select_columns, join1, join2, order)
            return sva_os
        except Error as e:
            Greske("Greska trazenje opreme koja pripada odredjenoj fakturi - OsnovnoSredstvoModel-pronadji_opremu_faktura_unos", e)

    def pronadji_opremu_faktura_unos(self, id_fakture):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.nabavna_vrednost, osnovna_sredstva.nabavka_otpisana_vrednost, osnovna_sredstva.status, konto.oznaka, stope.procenat, korisnici.ime, mesto.oznaka"
            join1 = "konto on osnovna_sredstva.konto_id=konto.idkonto"
            join2 = "stope on osnovna_sredstva.stopa_id=stope.idstope"
            join3 = "korisnici on osnovna_sredstva.zaposleni_id=korisnici.idkorisnici"
            join4 = "mesto on osnovna_sredstva.lokacija_id=mesto.idmesto"
            condition = "osnovna_sredstva.nabavka_id={}".format(id_fakture)
            order = "osnovna_sredstva.idosnovna_sredstva"
            sva_os = connection.select_where_four_join(select_columns, self.tablename, join1, condition, order, join2, join3, join4)
            return sva_os
        except Error as e:
            Greske("Greska trazenje opreme koja pripada odredjenoj fakturi - OsnovnoSredstvoModel-pronadji_opremu_faktura_unos", e)

    # pronalazenje u bazi poslednjeg unetog naloga
    def pronadji_poslednji(self):
        try:
            kolona = 'inventarni_broj'
            connection = Database()
            pronadjen_nalog = connection.select_last_from_table(self.tablename, kolona)
            return pronadjen_nalog
        except Error as e:
            Greske("Greška prilikom povezivanja na bazu podataka! Pronalazenje u bazi poslednjeg unetog naloga - OsnovnoSredstvoModel-pronadji_poslednji", e)

    def read_osnovna_sredstva_aktivna_amortizovana(self):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, nabavka.datum_dokumenta, osnovna_sredstva.nabavna_vrednost, osnovna_sredstva.status"
            join1 = "nabavka on osnovna_sredstva.nabavka_id=nabavka.idnabavka"
            condition = "osnovna_sredstva.status<>'rashodovano' and osnovna_sredstva.aktiviran=1"
            order = "osnovna_sredstva.inventarni_broj"
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order)
            return sva_os
        except Error as e:
            Greske(
                "Greska citanje svih osnovnih sredstava iz odredjenog naloga - OsnovnoSredstvoModel-read_osnovna_sredstva_aktivna_amortizovana", e)

    ''' za stampu popisne liste na danasnji dan '''
    def osnovna_sredstva_aktivna_amortizovana_danas(self, sort):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.nabavna_vrednost-osnovna_sredstva.otpisana_vrednost, korisnici.ime, mesto.oznaka"
            condition = "osnovna_sredstva.status<>'rashodovano' and osnovna_sredstva.aktiviran=1"
            join1 = "korisnici on osnovna_sredstva.zaposleni_id=korisnici.idkorisnici"
            join2 = "mesto on osnovna_sredstva.lokacija_id=mesto.idmesto"
            order = "osnovna_sredstva." + sort
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order, join2)
            return sva_os
        except Error as e:
            Greske(
                "Greska citanje osnovnih sredstava popisna lista na danasnji dan - OsnovnoSredstvoModel-osnovna_sredstva_aktivna_amortizovana_danas", e)

    ''' za stampu popisne liste na danasnji dan po amortizacionim grupama'''

    def osnovna_sredstva_aktivna_amortizovana_danas_amortizacione_grupe(self, sort):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.nabavna_vrednost-osnovna_sredstva.otpisana_vrednost, stope.oznaka, stope.naziv, stope.procenat"
            condition = "osnovna_sredstva.status<>'rashodovano' and osnovna_sredstva.aktiviran=1"
            join1 = "stope on osnovna_sredstva.stopa_id=stope.idstope"
            order = "osnovna_sredstva." + sort
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order)
            return sva_os
        except Error as e:
            Greske(
                "Greska citanje osnovnih sredstava popisna lista na danasnji dan - OsnovnoSredstvoModel-osnovna_sredstva_aktivna_amortizovana_danas",
                e)

    ''' za stampu popisne liste na datum amortizacije '''
    def popisna_lista_po_datumu_amortizacije(self, id_amortizacije, sort):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, izvestaj_amortizacije.nabavna_vrednost-izvestaj_amortizacije.tekuca_amortizacija-izvestaj_amortizacije.dosadasnji_otpis, korisnici.ime, mesto.oznaka"
            join1 = "izvestaj_amortizacije on osnovna_sredstva.idosnovna_sredstva=izvestaj_amortizacije.id_opreme"
            join2 = "korisnici on osnovna_sredstva.zaposleni_id=korisnici.idkorisnici"
            join3 = "mesto on osnovna_sredstva.lokacija_id=mesto.idmesto"
            condition = "izvestaj_amortizacije.id_amortizacije={}".format(id_amortizacije)
            order = "osnovna_sredstva." + sort
            sva_os = connection.select_where_tree_join(select_columns, self.tablename, join1, condition, order, join2,
                                                       join3)
            return sva_os
        except Error as e:
            Greske("Greska - OsnovnoSredstvoModel-popisna_lista_po_datumu_amortizacije",  e)

    ''' za stampu popisne liste na datum amortizacije po amortizacionim grupama'''
    def popisna_lista_po_datumu_amortizacije_amortiz_grupe(self, id_amortizacije, sort):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, izvestaj_amortizacije.nabavna_vrednost-izvestaj_amortizacije.tekuca_amortizacija-izvestaj_amortizacije.dosadasnji_otpis, stope.oznaka, stope.naziv, stope.procenat"
            join1 = "izvestaj_amortizacije on osnovna_sredstva.idosnovna_sredstva=izvestaj_amortizacije.id_opreme"
            join2 = "stope on osnovna_sredstva.stopa_id=stope.idstope"
            condition = "izvestaj_amortizacije.id_amortizacije={}".format(id_amortizacije)
            order = "osnovna_sredstva." + sort
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order, join2)
            return sva_os
        except Error as e:
            Greske("Greska - OsnovnoSredstvoModel-popisna_lista_po_datumu_amortizacije", e)

    def pronadji_osnovno_sredstvo(self, id_osnovnog_sredstva):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, nabavka.datum_dokumenta, nabavka.broj_dokumenta, dobavljaci.naziv, osnovna_sredstva.nabavna_vrednost, osnovna_sredstva.otpisana_vrednost, osnovna_sredstva.status, konto.oznaka, stope.procenat, mesto.oznaka, korisnici.ime"
            join1 = "konto on osnovna_sredstva.konto_id=konto.idkonto"
            join2 = "stope on osnovna_sredstva.stopa_id=stope.idstope"
            join3 = "mesto on osnovna_sredstva.lokacija_id=mesto.idmesto"
            join4 = "korisnici on osnovna_sredstva.zaposleni_id=korisnici.idkorisnici"
            join5 = "nabavka on osnovna_sredstva.nabavka_id=nabavka.idnabavka"
            join6 = "dobavljaci on nabavka.dobavljac_id=dobavljaci.iddobavljaci"
            condition = "osnovna_sredstva.idosnovna_sredstva='{}'".format(id_osnovnog_sredstva)
            os = connection.select_where_six_join(self.tablename, select_columns, join1, join2, join3, join4, join5, join6, condition)
            return os
        except Error as e:
            Greske("Greska pronalazenje osnovnog sredstva iz odredjenog naloga - OsnovnoSredstvoModel-pronadji_osnovno_sredstvo", e)

    def pronadji_osnovno_sredstvo_inv_broj(self, invent_broj):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.datum_nabavke, osnovna_sredstva.broj_fakture, dobavljaci.naziv, osnovna_sredstva.nabavna_vrednost, osnovna_sredstva.otpisana_vrednost, osnovna_sredstva.status, konto.oznaka, stope.procenat, mesto.oznaka, korisnici.ime"
            join1 = "konto on osnovna_sredstva.konto_id=konto.idkonto"
            join2 = "stope on osnovna_sredstva.stopa_id=stope.idstope"
            join3 = "mesto on osnovna_sredstva.lokacija_id=mesto.idmesto"
            join4 = "korisnici on osnovna_sredstva.zaposleni_id=korisnici.idkorisnici"
            join5 = "dobavljaci on osnovna_sredstva.dobavljac_id=dobavljaci.iddobavljaci"
            condition = "osnovna_sredstva.inventarni_broj='{}'".format(invent_broj)
            os = connection.select_where_five_join(self.tablename, select_columns, join1, join2, join3, join4, join5, condition)
            return os
        except Error as e:
            Greske("Greska pronalazenje osnovnog sredstva iz odredjenog naloga - OsnovnoSredstvoModel-pronadji_osnovno_sredstvo_inv_broj", e)

    '''menjanje lokacije osnovnog sredstva'''
    def update_osnovno_sredstvo(self, id_osnovnog_sredstva, lokacija, zaposleni):
        # Ažuriranje baze podataka
        try:
            set_condition = "zaposleni_id='{}'".format(zaposleni) + ", lokacija_id='{}'".format(lokacija)
            filter_condition = "idosnovna_sredstva='{}'".format(id_osnovnog_sredstva)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Greska prilikom azuriranje osnovnog sredstva - OsnovnoSredstvoModel-update_osnovno_sredstvo", e)

    def pronadji_osnovna_sredstva_amortizacija(self, datum):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.nabavna_vrednost, osnovna_sredstva.otpisana_vrednost, stope.procenat, nabavka.datum_dokumenta, osnovna_sredstva.konto_id, osnovna_sredstva.status"
            condition = "(osnovna_sredstva.status='aktivno' or osnovna_sredstva.status='amortizovano') and osnovna_sredstva.aktiviran=1 and nabavka.datum_dokumenta<'{}'".format(datum)
            join = "stope on osnovna_sredstva.stopa_id=stope.idstope"
            join2 = "nabavka on osnovna_sredstva.nabavka_id=nabavka.idnabavka"
            order = "osnovna_sredstva.inventarni_broj"
            sva_os = connection.select_where_join(select_columns, self.tablename, join, condition, order, join2)
            return sva_os
        except Error as e:
            Greske("Greska pronalazenje osnovnog sredstva iz odredjenog naloga - OsnovnoSredstvoModel-pronadji_osnovna_sredstva_amortizacija", e)

    def delete_osnovno_sredstvo(self, id_os):
        # Brisanje iz baze podataka
        try:
            delete_condition = "idosnovna_sredstva={}".format(id_os)
            connection = Database()
            connection.delete(self.tablename, delete_condition)
        except Error as e:
            Greske("Hmmmm, neka greška prilikom brisanja osnovnog sredstva - OsnovnoSredstvoModel - delete osnovno sredstvo!", e)

    def da_li_postoji_os(self, inv_broj):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.nabavna_vrednost, osnovna_sredstva.otpisana_vrednost, osnovna_sredstva.status, osnovna_sredstva.konto_id, osnovna_sredstva.stopa_id, osnovna_sredstva.zaposleni_id, osnovna_sredstva.lokacija_id, nabavka.datum_dokumenta"
            join = "nabavka on osnovna_sredstva.nabavka_id=nabavka.idnabavka"
            condition = "inventarni_broj={}".format(inv_broj) + " and status <> 'rashodovano'" + " and aktiviran=1"
            order = "osnovna_sredstva.idosnovna_sredstva"
            sva_os = connection.select_where_join(select_columns, self.tablename, join, condition, order)
            return sva_os
        except Error as e:
            Greske("Greska citanje svih osnovnih sredstava iz odredjenog naloga - OsnovnoSredstvoModel-da_li_postoji_os", e)

    def osnovno_sredstvo_za_rashod(self, id_rashoda):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.datum_aktiviranja"
            join = "rashod_opreme on osnovna_sredstva.idosnovna_sredstva=rashod_opreme.id_osnovnog_sredstva"
            condition = "rashod_opreme.id_rashoda={}".format(id_rashoda)
            order = "osnovna_sredstva.idosnovna_sredstva"
            sva_os = connection.select_where_join(select_columns, self.tablename, join, condition, order)
            return sva_os
        except Error as e:
            Greske("Greska pronalazenje osnovnog sredstva za rashod - OsnovnoSredstvoModel-osnovno_sredstvo_za_rashod", e)

    def pronadji_id_stope(self, inventarni_broj):
        try:
            connection = Database()
            select_columns = "stopa_id"
            condition = "inventarni_broj"
            value = inventarni_broj
            sva_os = connection.select_where(self.tablename, select_columns, condition, value)
            return sva_os
        except Error as e:
            Greske("Greska - OsnovnoSredstvoModel-pronadji_id_stope", e)

    def azuriraj_otpisanu_vrednost(self, id_osnovnog_sredstva, otpisana, amortizovano):
        # Ažuriranje baze podataka
        try:
            if amortizovano == 'da':
                set_condition = "status='amortizovano', otpisana_vrednost='{}'".format(otpisana)
            else:
                set_condition = "otpisana_vrednost='{}'".format(otpisana)
            filter_condition = "idosnovna_sredstva='{}'".format(id_osnovnog_sredstva)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Greska prilikom azuriranje osnovnog sredstva - OsnovnoSredstvoModel-azuriraj otpisanu vrednost", e)

    def pronadji_tekucu_amortizaciju(self, id_amortizacije, datum_amortizacije):
        try:
            connection = Database()
            select_columns = "DISTINCT konto.oznaka, konto.naziv, count(*), ifnull(sum(osnovna_sredstva.nabavna_vrednost), 0), ifnull(sum(amortizacija_opreme.obracunata_amortizacija),0)"
            join1 = "konto on osnovna_sredstva.konto_id=konto.idkonto"
            join2 = "amortizacija_opreme on osnovna_sredstva.idosnovna_sredstva=amortizacija_opreme.id_oprema and amortizacija_opreme.id_amortizacija='{}'".format(id_amortizacije)
            condition = "osnovna_sredstva.datum_nabavke<'{}'".format(datum_amortizacije)
            group = "konto.oznaka"
            order = "konto.oznaka"
            sva_os = connection.select_distinct_two_left_join(select_columns, self.tablename, join1, join2, condition, group, order)
            return sva_os
        except Error as e:
            Greske("Greska - OsnovnoSredstvoModel-pronadji_tekucu_amortizaciju", e)

    def izvestaj_amortizacije(self, id_amortizacije):
        try:
            connection = Database()
            select_columns = "konto.oznaka, konto.naziv, count(*), ifnull(sum(izvestaj_amortizacije.nabavna_vrednost), 0), ifnull(sum(izvestaj_amortizacije.tekuca_amortizacija), 0), ifnull(sum(izvestaj_amortizacije.dosadasnji_otpis),0), ifnull(sum(izvestaj_amortizacije.tekuca_amortizacija), 0) + ifnull(sum(izvestaj_amortizacije.dosadasnji_otpis),0), ifnull(sum(izvestaj_amortizacije.nabavna_vrednost), 0) - (ifnull(sum(izvestaj_amortizacije.tekuca_amortizacija), 0) + ifnull(sum(izvestaj_amortizacije.dosadasnji_otpis),0)) "
            tablename = "izvestaj_amortizacije"
            join = "konto on izvestaj_amortizacije.id_konto=konto.idkonto"
            condition = "izvestaj_amortizacije.id_amortizacije={}".format(id_amortizacije)
            group = "izvestaj_amortizacije.id_konto"
            order = "konto.oznaka"
            izvestaj = connection.select_sum_group_join(tablename, select_columns, condition, join, group, order)
            return izvestaj
        except Error as e:
            Greske("Greska izvestaj amortizacije - OsnovnoSredstvoModel-izvestaj_amortizacije", e)

    def unesi_podatke_u_izvestaj(self, konto, nabavna, amortizacija, dosadasnja_otpisana, id_amortizacije, id_opreme):
        try:
            tabela = "izvestaj_amortizacije"
            schema = "id_konto, nabavna_vrednost, tekuca_amortizacija, dosadasnji_otpis, id_amortizacije, id_opreme"
            value = (konto, nabavna, amortizacija, dosadasnja_otpisana, id_amortizacije, id_opreme)
            connection = Database()
            connection.insert(tabela, schema, value)
        except Error as e:
            Greske("Greska upisa podataka u izvestaj amortizacije - OsnovnoSredstvoModel-unesi_podatke_u_izvestaj", e)

    def azuriraj_otpisanu_vrednost_brisanje_amortizacije(self, id_opreme, otpisana, stat=None):
        # Ažuriranje baze podataka
        try:
            if stat is None:
                set_condition = "otpisana_vrednost='{}'".format(otpisana)
            else:
                set_condition = "status='aktivno', otpisana_vrednost='{}'".format(otpisana)
            filter_condition = "idosnovna_sredstva='{}'".format(id_opreme)
            connection = Database()
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Greska prilikom azuriranje osnovnog sredstva - OsnovnoSredstvoModel-azuriraj otpisanu vrednost_brisanje amortizacije", e)

    def pronadji_os_po_id(self, id_opreme):
        try:
            connection = Database()
            select_columns = "*"
            condition = "idosnovna_sredstva={}".format(id_opreme)
            sva_os = connection.select_condition(self.tablename, select_columns, condition)
            return sva_os
        except Error as e:
            Greske("Greska pronalazenje osnovnih sredstava po id - OsnovnoSredstvoModel-pronadji_os_po_id", e)

    def da_li_postoji_os_za_rashod(self, inv_broj):
        try:
            connection = Database()
            select_columns = "*"
            condition = "inventarni_broj={}".format(inv_broj) + " and status <> 'rashodovano'"
            sva_os = connection.select_condition(self.tablename, select_columns, condition)
            return sva_os
        except Error as e:
            Greske("Greska citanje da li postoji osnovna sredstva za rashod - OsnovnoSredstvoModel-da_li_postoji_os_za_rashod", e)

    def pronadji_sva_os_nalog_rashod(self, id_naloga_rashod):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.idosnovna_sredstva, osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, nabavka.datum_dokumenta"
            condition = "rashod_opreme.id_rashoda={}".format(id_naloga_rashod)
            join1 = "rashod_opreme on osnovna_sredstva.idosnovna_sredstva=rashod_opreme.id_osnovnog_sredstva"
            join2 = "nabavka on osnovna_sredstva.nabavka_id=nabavka.idnabavka"
            order = "osnovna_sredstva.inventarni_broj"
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order, join2)
            return sva_os
        except Error as e:
            Greske("Greska citanje svih osnovnih sredstava iz rashoda - OsnovnoSredstvoModel-pronadji_sva_os_nalog_rashod", e)

    def rashoduj_osnovno_sredstvo(self, id_os):
        try:
            connection = Database()
            set_condition = "status='rashodovano'"
            filter_condition = "idosnovna_sredstva={}".format(id_os)
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske("Greska rashodovanje osnovnog sredstva - OsnovnoSredstvoModel-rashoduj_osnovno_sredstvo", e)

    def pronadji_osnovno_sredstvo_iz_fakture(self, id_fakture):
        try:
            connection = Database()
            select_columns = "*"
            condition = "nabavka_id"
            value = id_fakture
            sva_os = connection.select_where(self.tablename, select_columns, condition, value)
            return sva_os
        except Error as e:
            Greske("Greska citanje osnovnih sredstava iz fakture - OsnovnoSredstvoModel-pronadji_osnovno_sredstvo_iz_fakture", e)

    def pronadji_osnovno_sredstvo_iz_fakture_po_kontima(self, id_fakture):
        try:
            connection = Database()
            select_columns = "konto.oznaka, konto.naziv, ifnull(sum(osnovna_sredstva.nabavna_vrednost), 0), ifnull(sum(osnovna_sredstva.nabavka_otpisana_vrednost), 0)"
            join = "konto on osnovna_sredstva.konto_id=konto.idkonto"
            group = "konto.oznaka"
            order = "konto.oznaka"
            condition = "nabavka_id={}".format(id_fakture)
            sva_os = connection.select_sum_group_join(self.tablename, select_columns, condition, join, group, order)
            return sva_os
        except Error as e:
            Greske("Greska citanje osnovnih sredstava iz fakture grup by konto - OsnovnoSredstvoModel-pronadji_osnovno_sredstvo_iz_fakture_po_kontima", e)

    def izmena_novog_osnovnog_sredstva(self, id_opreme, inventarni_broj, naziv, nabavna_vrednost, otpisana_vrednost, status, konto, stopa, zaposleni, lokacija, faktura, aktiviran):
        try:
            connection = Database()
            set_condition = 'inventarni_broj={}'.format(inventarni_broj) + ', naziv="{}"'.format(naziv) + ', nabavna_vrednost={}'.format(nabavna_vrednost) + ', otpisana_vrednost={}'.format(otpisana_vrednost) + ', status="{}"'.format(status) + ', konto_id={}'.format(konto) + ', stopa_id={}'.format(stopa) + ', zaposleni_id={}'.format(zaposleni) + ', lokacija_id={}'.format(lokacija) + ', nabavka_id={}'.format(faktura) + ', aktiviran={}'.format(aktiviran) + ', nabavka_otpisana_vrednost={}'.format(otpisana_vrednost)
            filter_condition = "idosnovna_sredstva={}".format(id_opreme)
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske(
                "Greska azuriranje osnovnog sredstva kod nabavke opreme u fakturi - OsnovnoSredstvoModel-izmena_novog_osnovnog_sredstva", e)

    def postoji_osnovno_sredstvo(self, inv_broj):
        try:
            connection = Database()
            select_columns = "*"
            condition = "inventarni_broj"
            value = inv_broj
            sva_os = connection.select_where(self.tablename, select_columns, condition, value)
            return sva_os
        except Error as e:
            Greske("Greska trazenje osnovnog sredstva po inv.broju, kod unosa - OsnovnoSredstvoModel-postoji_osnovno_sredstvo", e)

    def postoji_inv_broj_osim_selektovanog(self, id_oprema, inv_broj):
        try:
            connection = Database()
            select_columns = "*"
            condition = "idosnovna_sredstva !={}".format(id_oprema)+" and inventarni_broj={}".format(inv_broj)
            sva_os = connection.select_condition(self.tablename, select_columns, condition)
            return sva_os
        except Error as e:
            Greske("Greska trazenje da li je unet postojeci inventarni broj kod azuriranja - OsnovnoSredstvoModel-postoji_inv_broj_osim_selektovanog", e)

    def aktiviraj_os(self, id_os):
        try:
            connection = Database()
            set_condition = 'aktiviran=1'
            filter_condition = "idosnovna_sredstva={}".format(id_os)
            connection.update(self.tablename, set_condition, filter_condition)
        except Error as e:
            Greske(
                "Greska aktiviranje osnovnog sredstva - knjizenje fakture - OsnovnoSredstvoModel-aktiviraj_os", e)

    def nabavljena_oprema_po_datumu(self, pocetni, krajnji):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, osnovna_sredstva.nabavna_vrednost, nabavka.datum_dokumenta, nabavka.broj_dokumenta, dobavljaci.naziv"
            condition = "(nabavka.datum_dokumenta between '{}'".format(pocetni) + " and '{}')".format(krajnji)
            join1 = "nabavka on osnovna_sredstva.nabavka_id=nabavka.idnabavka"
            join2 = "dobavljaci on nabavka.dobavljac_id=dobavljaci.iddobavljaci"
            order = "osnovna_sredstva.inventarni_broj"
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order, join2)
            return sva_os
        except Error as e:
            Greske("Greska citanje nabavljene opreme izmedju datuma - OsnovnoSredstvoModel-nabavljena_oprema_po_datumu", e)

    def rashodovana_oprema_po_datumu(self, pocetni, krajnji):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, rashod_opreme.nabavna-rashod_opreme.otpisana-rashod_opreme.amortizacija_r, rashod.datum, rashod.broj_rashoda"
            condition = "(rashod.datum between '{}'".format(pocetni) + " and '{}')".format(krajnji) + " and proknjizen=1"
            join1 = "rashod_opreme on osnovna_sredstva.idosnovna_sredstva=rashod_opreme.id_osnovnog_sredstva"
            join2 = "rashod on rashod_opreme.id_rashoda=rashod.idrashod"
            order = "osnovna_sredstva.inventarni_broj"
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order, join2)
            return sva_os
        except Error as e:
            Greske("Greska citanje rashodovane opreme izmedju datuma - OsnovnoSredstvoModel-rashodovana_oprema_po_datumu", e)

    def osnovna_sredstva_za_pomocnu_knjigu(self):
        try:
            connection = Database()
            select_columns = "osnovna_sredstva.inventarni_broj, osnovna_sredstva.naziv, rashod_opreme.nabavna-rashod_opreme.otpisana-rashod_opreme.amortizacija_r, rashod.datum, rashod.broj_rashoda"
            #condition = "(rashod.datum between '{}'".format(pocetni) + " and '{}')".format(krajnji) + " and proknjizen=1"
            join1 = "rashod_opreme on osnovna_sredstva.idosnovna_sredstva=rashod_opreme.id_osnovnog_sredstva"
            join2 = "rashod on rashod_opreme.id_rashoda=rashod.idrashod"
            order = "osnovna_sredstva.inventarni_broj"
            sva_os = connection.select_where_join(select_columns, self.tablename, join1, condition, order, join2)
            return sva_os
        except Error as e:
            Greske("Greska citanje osnovnih sredstava za stampu pomocne knjige osnovnih sredstava - OsnovnoSredstvoModel-osnovna_sredstva_za_pomocnu_knjigu", e)
