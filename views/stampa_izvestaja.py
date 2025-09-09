from fpdf import FPDF
from datetime import date
import webbrowser
import locale
from models.firma_model import FirmaModel


class PDF(FPDF):

    def __init__(self, orient, mera, form):
        FPDF.__init__(self, orientation=orient, unit=mera, format=form)
        self.set_font('Helvetica', '', 9)
        # self.fontsize=fontsize

    def header(self):
        # Logo
        # x=110.9, y=16.1
        # self.image(name='logo.png', x=110.6, y=15.9, w=72.9)
        firma = FirmaModel()
        podaci_firma = firma.read()
        stampa = StampaIzvestaja()
        naziv_firme = stampa.zamena_slova(podaci_firma[0][1])
        mesto_firme = stampa.zamena_slova(podaci_firma[0][2])
        # Arial bold 15
        self.set_font('Helvetica', '', 12)
        # textcolor
        self.set_text_color(r=65, g=105, b=225)
        if self.page_no() == 1:
            # Title
            self.text(self.l_margin, 1+1, txt=naziv_firme + ", " + mesto_firme)
            self.line(1, 2.5, 28, 2.5)
            # self.line(1, 2.5, 20, 2.5)
            self.cell(20, 2, "", 0, 1)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Helvetica', 'I', 9)
        # Page number
        self.cell(0, 27, 'Strana ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')


class StampaIzvestaja:


    def zamena_slova(self, rec):
        return rec.replace('č', 'c').replace('ž', 'z').replace('ć', 'c').replace('š', 's').replace('Č', 'C').replace(
            'Ž', 'Z').replace('Ć', 'C').replace('Š', 'S').replace('đ', 'dj').replace('Đ', 'Dj')

    def stampa_izvestaja_amortizacije(self, podaci_za_stampu, podaci_amortizacija):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        # firma = FirmaModel()
        # podaci_firma = firma.read()

        pdf = PDF('landscape', 'cm', 'A4')
        # pdf.accept_page_break()
        pdf.add_page()
        pdf.set_font('Helvetica', '', 8)
        #pdf.line(1, 2.5, 28, 2.5)
        # pdf.cell(20, 2, "", 0, 1)
        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y")

        datum_amortizacije = podaci_amortizacija[0][1].strftime("%d.%m.%Y")

        pdf.cell(24, 1, 'Datum izvestaja:', 0, 0, 'R')
        pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
        # pdf.cell(27, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(27, 2, 'Izvestaj amortizacije: ' + self.zamena_slova(podaci_amortizacija[0][2].capitalize()) + '  ' + datum_amortizacije, 0, 1, 'C')

        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 1, 'Konto', 0, 0, 'C', fill=True)
        pdf.cell(7, 1, 'Naziv', 0, 0, 'C', fill=True)
        pdf.cell(1, 1, 'Broj OS', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Nabavna vrednost', 0, 0, 'C', fill=True)
        pdf.cell(3, 1, 'Tekuca amortizacija', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Dosadasnji otpis', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Ukupan otpis', 0, 0, 'C', fill=True)
        pdf.cell(3, 1, 'Sadasnja vrednost', 0, 1, 'C', fill=True)

        pdf.set_font('Helvetica', '', 8)

        ukupno_broj_os = 0
        ukupno_nabavna = 0
        ukupno_tek_amortizacija = 0
        ukupno_dosadasnji_otpis = 0
        ukupno_ukupni_otpis = 0
        ukupno_sadasnja = 0

        for red in podaci_za_stampu:

            ukupno_broj_os += red[2]
            ukupno_nabavna += red[3]
            ukupno_tek_amortizacija += red[4]
            ukupno_dosadasnji_otpis += red[5]
            ukupno_ukupni_otpis += red[6]
            ukupno_sadasnja += red[7]

            konto_n = self.zamena_slova(red[1])
            nabavna = locale.format_string('%10.2f', red[3], grouping=True)
            tekuca_am = locale.format_string('%10.2f', red[4], grouping=True)
            dosadasnji_o = locale.format_string('%10.2f', red[5], grouping=True)
            ukupan_o = locale.format_string('%10.2f', red[6], grouping=True)
            sadasnja = locale.format_string('%10.2f', red[7], grouping=True)

            pdf.cell(1, 0.6, red[0], 0, 0, 'C')
            pdf.cell(7, 0.6, konto_n, 0, 0, 'L')
            pdf.cell(1, 0.6, str(red[2]), 0, 0, 'R')
            pdf.cell(4, 0.6, nabavna, 0, 0, 'R')
            pdf.cell(3, 0.6, tekuca_am, 0, 0, 'R')
            pdf.cell(4, 0.6, dosadasnji_o, 0, 0, 'R')
            pdf.cell(4, 0.6, ukupan_o, 0, 0, 'R')
            pdf.cell(3, 0.6, sadasnja, 0, 1, 'R')
            '''
            if redovi_po_strani > 21:

                pdf.add_page()
                pdf.cell(19, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
                redovi_po_strani = 0

            redovi_po_strani += 1
            '''
        ''' ovo mora zbog prikaza naseg formata brojeva na pdf izvestaju '''
        format_ukupno_nabavna = locale.format_string('%10.2f', ukupno_nabavna, grouping=True)
        format_ukupno_tek_amortizacija = locale.format_string('%10.2f', ukupno_tek_amortizacija, grouping=True)
        format_ukupno_dosadasnji_otpis = locale.format_string('%10.2f', ukupno_dosadasnji_otpis, grouping=True)
        format_ukupno_ukupni_otpis = locale.format_string('%10.2f', ukupno_ukupni_otpis, grouping=True)
        format_ukupno_sadasnja = locale.format_string('%10.2f', ukupno_sadasnja, grouping=True)

        # UKUPNO ZA DOKUMENT
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 1, '', 0, 0, 'C', fill=True)
        pdf.cell(7, 1, 'UKUPNO', 0, 0, 'L', fill=True)
        pdf.cell(1, 1, str(ukupno_broj_os), 0, 0, 'R', fill=True)
        pdf.cell(4, 1, format_ukupno_nabavna, 0, 0, 'R', fill=True)
        pdf.cell(3, 1, format_ukupno_tek_amortizacija, 0, 0, 'R', fill=True)
        pdf.cell(4, 1, format_ukupno_dosadasnji_otpis, 0, 0, 'R', fill=True)
        pdf.cell(4, 1, format_ukupno_ukupni_otpis, 0, 0, 'R', fill=True)
        pdf.cell(3, 1, format_ukupno_sadasnja, 0, 1, 'R', fill=True)

        pdf.set_fill_color(224, 224, 224)
        # PRIMER KNJIZENJA AMORTIZACIJE
        pdf.cell(27, 1, '', 0, 1, 'C')
        pdf.cell(16, 1, "Knjizenje amortizacije", 0, 1, "L")
        pdf.cell(8, 1, 'DUGUJE ', 0, 0, 'L', fill=True)
        pdf.cell(8, 1, 'POTRAZUJE ', 0, 1, 'L', fill=True)
        pdf.cell(8, 1, '3111__ Nefinansijska imovina: ' + format_ukupno_tek_amortizacija, 0, 0, 'L')
        pdf.cell(8, 1, '0112__ Ispravka vrednosti: ' + format_ukupno_tek_amortizacija, 0, 1, 'L')

        pdf.output('izvestaj.pdf', 'F')
        webbrowser.open_new(r'izvestaj.pdf')

    def stampa_izvestaja_rashod(self, spisak, grupisani_spisak, rashod_podaci):
        locale.setlocale(locale.LC_ALL, 'de_DE')

        pdf = PDF('landscape', 'cm', 'A4')
        # pdf = FPDF('landscape', 'cm', 'A4')
        # pdf.accept_page_break()
        pdf.add_page()
        pdf.set_font('Helvetica', '', 8)
        #pdf.line(1, 2.5, 28, 2.5)

        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y")

        datum_rashoda = rashod_podaci[0][1].strftime("%d.%m.%Y")

        pdf.cell(24, 1, 'Datum izvestaja:', 0, 0, 'R')
        pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
        # pdf.cell(27, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(27, 2, 'Izvestaj rashoda: ' + self.zamena_slova(
            rashod_podaci[0][2].capitalize()) + '  ' + datum_rashoda, 0, 1, 'C')

        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
        pdf.cell(1, 1, 'Inv.broj', 0, 0, 'C', fill=True)
        pdf.cell(7, 1, 'Naziv', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Nabavna vrednost', 0, 0, 'C', fill=True)
        pdf.cell(3, 1, 'Amortizacija rashoda', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Dosadasnji otpis', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Ukupan otpis', 0, 0, 'C', fill=True)
        pdf.cell(3, 1, 'Sadasnja vrednost', 0, 1, 'C', fill=True)

        pdf.set_font('Helvetica', '', 8)

        ukupno_nabavna = 0
        ukupno_amortizacija = 0
        ukupno_dosadasnji_otpis = 0
        ukupno_ukupni_otpis = 0
        ukupno_sadasnja = 0
        brojac = 0

        for red in spisak:
            brojac += 1
            ukupno_nabavna += red[2]
            ukupno_amortizacija += red[3]
            ukupno_dosadasnji_otpis += red[4]
            otpisana_dosad = red[3]+red[4]
            ukupno_ukupni_otpis += otpisana_dosad
            sadasnja_vrednost = red[2] - otpisana_dosad
            ukupno_sadasnja += sadasnja_vrednost

            nabavna = locale.format_string('%10.2f', red[2], grouping=True)
            tekuca_am = locale.format_string('%10.2f', red[3], grouping=True)
            dosadasnji_o = locale.format_string('%10.2f', red[4], grouping=True)
            ukupan_o = locale.format_string('%10.2f', otpisana_dosad, grouping=True)
            sadasnja = locale.format_string('%10.2f', sadasnja_vrednost, grouping=True)

            pdf.cell(1, 0.6, str(brojac), 0, 0, 'C')
            pdf.cell(1, 0.6, str(red[0]), 0, 0, 'C')
            pdf.cell(7, 0.6, self.zamena_slova(red[1]), 0, 0, 'L')

            pdf.cell(4, 0.6, nabavna, 0, 0, 'R')
            pdf.cell(3, 0.6, tekuca_am, 0, 0, 'R')
            pdf.cell(4, 0.6, dosadasnji_o, 0, 0, 'R')
            pdf.cell(4, 0.6, ukupan_o, 0, 0, 'R')
            pdf.cell(3, 0.6, sadasnja, 0, 1, 'R')
            '''
            if redovi_po_strani > 21:
                pdf.add_page()
                pdf.cell(19, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
                redovi_po_strani = 0

            redovi_po_strani += 1
            '''
        # ovo mora zbog prikaza naseg formata brojeva na pdf izvestaju
        format_ukupno_nabavna = locale.format_string('%10.2f', ukupno_nabavna, grouping=True)
        format_ukupno_tek_amortizacija = locale.format_string('%10.2f', ukupno_amortizacija, grouping=True)
        format_ukupno_dosadasnji_otpis = locale.format_string('%10.2f', ukupno_dosadasnji_otpis, grouping=True)
        format_ukupno_ukupni_otpis = locale.format_string('%10.2f', ukupno_ukupni_otpis, grouping=True)
        format_ukupno_sadasnja = locale.format_string('%10.2f', ukupno_sadasnja, grouping=True)

        # UKUPNO ZA DOKUMENT
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 0.6, '', 0, 0, 'C', fill=True)
        pdf.cell(1, 0.6, '', 0, 0, 'C', fill=True)
        pdf.cell(7, 0.6, 'UKUPNO:', 0, 0, 'L', fill=True)
        pdf.cell(4, 0.6, format_ukupno_nabavna, 0, 0, 'R', fill=True)
        pdf.cell(3, 0.6, format_ukupno_tek_amortizacija, 0, 0, 'R', fill=True)
        pdf.cell(4, 0.6, format_ukupno_dosadasnji_otpis, 0, 0, 'R', fill=True)
        pdf.cell(4, 0.6, format_ukupno_ukupni_otpis, 0, 0, 'R', fill=True)
        pdf.cell(3, 0.6, format_ukupno_sadasnja, 0, 1, 'R', fill=True)

        pdf.cell(27, 0.6, '', 0, 1, 'C')
        pdf.cell(27, 0.6, '', 0, 1, 'C')

        # TABELA ZBIRNO PO KONTIMA ZBOG KNJIZENJA
        # zaglavlje
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(27, 1, 'Rekapitulacija rashoda po kontima ', 0, 1, 'C')
        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(4, 1, 'Konto', 0, 0, 'C', fill=True)
        pdf.cell(6, 1, 'Nabavna vrednost', 0, 0, 'R', fill=True)
        pdf.cell(5, 1, 'Amortizacija rashoda', 0, 0, 'R', fill=True)
        pdf.cell(6, 1, 'Ukupan otpis', 0, 0, 'R', fill=True)
        pdf.cell(6, 1, 'Sadasnja vrednost', 0, 1, 'R', fill=True)
        pdf.set_font('Helvetica', '', 8)

        ukupno_nabavna_rekap = 0
        ukupno_amortizacija_rekap = 0
        ukupno_ukupni_otpis_rekap = 0
        ukupno_sadasnja_rekap = 0

        # podaci u tabeli
        for red in grupisani_spisak:
            ukupno_nabavna_rekap += red[1]
            ukupno_amortizacija_rekap += red[2]
            otpisana_dosad_rekap = red[2] + red[3]
            ukupno_ukupni_otpis_rekap += otpisana_dosad_rekap
            sadasnja_vrednost_rekap = red[1] - otpisana_dosad_rekap
            ukupno_sadasnja_rekap += sadasnja_vrednost_rekap

            nabavna_rekap = locale.format_string('%10.2f', red[1], grouping=True)
            tekuca_am_rekap = locale.format_string('%10.2f', red[2], grouping=True)
            ukupan_o_rekap = locale.format_string('%10.2f', otpisana_dosad_rekap, grouping=True)
            sadasnja_rekap = locale.format_string('%10.2f', sadasnja_vrednost_rekap, grouping=True)

            pdf.cell(4, 0.6, red[0], 0, 0, 'C')
            pdf.cell(6, 0.6, nabavna_rekap, 0, 0, 'R')
            pdf.cell(5, 0.6, tekuca_am_rekap, 0, 0, 'R')
            pdf.cell(6, 0.6, ukupan_o_rekap, 0, 0, 'R')
            pdf.cell(6, 0.6, sadasnja_rekap, 0, 1, 'R')
            '''
            if redovi_po_strani > 21:
                pdf.add_page()
                pdf.cell(19, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
                redovi_po_strani = 0

            redovi_po_strani += 1
            '''
        # donje zaglavlje tabele - Ukupno
        # ovo mora zbog prikaza naseg formata brojeva na pdf izvestaju
        format_ukupno_nabavna_rekap = locale.format_string('%10.2f', ukupno_nabavna_rekap, grouping=True)
        format_ukupno_tek_amortizacija_rekap = locale.format_string('%10.2f', ukupno_amortizacija_rekap, grouping=True)
        format_ukupno_ukupni_otpis_rekap = locale.format_string('%10.2f', ukupno_ukupni_otpis_rekap, grouping=True)
        format_ukupno_sadasnja_rekap = locale.format_string('%10.2f', ukupno_sadasnja_rekap, grouping=True)

        # UKUPNO ZA DOKUMENT
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(4, 1, 'UKUPNO:', 0, 0, 'C', fill=True)
        pdf.cell(6, 1, format_ukupno_nabavna_rekap, 0, 0, 'R', fill=True)
        pdf.cell(5, 1, format_ukupno_tek_amortizacija_rekap, 0, 0, 'R', fill=True)
        pdf.cell(6, 1, format_ukupno_ukupni_otpis_rekap, 0, 0, 'R', fill=True)
        pdf.cell(6, 1, format_ukupno_sadasnja_rekap, 0, 1, 'R', fill=True)

        pdf.set_fill_color(224, 224, 224)
        # PRIMER KNJIZENJA AMORTIZACIJE RASHODA
        pdf.cell(27, 1, '', 0, 1, 'C')
        pdf.cell(16, 1, "Knjizenje amortizacije rashoda", 0, 1, "L")
        pdf.cell(8, 1, 'DUGUJE ', 0, 0, 'L', fill=True)
        pdf.cell(8, 1, 'POTRAZUJE ', 0, 1, 'L', fill=True)
        pdf.cell(8, 1, '3111__ Nefinansijska imovina: ' + format_ukupno_tek_amortizacija_rekap, 0, 0, 'L')
        pdf.cell(8, 1, '0112__ Ispravka vrednosti: ' + format_ukupno_tek_amortizacija_rekap, 0, 1, 'L')

        # PRIMER KNJIZENJA OTPISA OPREME
        pdf.cell(27, 1, '', 0, 1, 'C')
        pdf.cell(16, 1, "Knjizenje otpisa opreme", 0, 1, "L")
        pdf.cell(8, 1, 'DUGUJE ', 0, 0, 'L', fill=True)
        pdf.cell(8, 1, 'POTRAZUJE ', 0, 1, 'L', fill=True)
        pdf.cell(8, 1, '3111__ Nefinansijska imovina: ' + format_ukupno_sadasnja_rekap, 0, 1, 'L')
        pdf.cell(8, 1, '0112__ Ispravka vrednosti: ' + format_ukupno_ukupni_otpis_rekap, 0, 0, 'L')
        pdf.cell(8, 1, '0112__ Oprema: ' + format_ukupno_nabavna_rekap, 0, 1, 'L')

        pdf.output('izvestaj_rashod.pdf', 'F')

        webbrowser.open_new(r'izvestaj_rashod.pdf')

    def stampa_ulazne_fakture(self, faktura_podaci, podaci_za_stampu, rekapitulacija):
        locale.setlocale(locale.LC_ALL, 'de_DE')

        pdf = PDF('portrait', 'cm', 'A4')
        pdf.add_page()
        pdf.set_font('Helvetica', '', 8)
        #pdf.line(1, 2.5, 20, 2.5)
        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y.")

        pdf.cell(19, 1, 'Datum stampe: ' + danasnji_datum, 0, 1, 'R')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(20, 2, 'Prijem od dobavljaca', 0, 1, 'C')
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(20, 1, 'Naziv dobavljaca: ' + self.zamena_slova(faktura_podaci[0][3]), 0, 1, 'L')
        pdf.cell(20, 1, 'Broj dokumenta: ' + self.zamena_slova(faktura_podaci[0][0]), 0, 1, 'L')
        pdf.cell(20, 1, 'Datum dokumenta: ' + faktura_podaci[0][1].strftime("%d.%m.%Y."), 0, 1, 'L')

        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
        pdf.cell(2, 1, 'Inv.broj', 0, 0, 'C', fill=True)
        pdf.cell(8, 1, 'Naziv osnovnog sredstva', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Nabavna vrednost', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Otpisana vrednost', 0, 1, 'C', fill=True)

        pdf.set_font('Helvetica', '', 9)

        ukupno_nabavna = 0
        ukupno_otpisana = 0
        redni_broj = 0
        for red in podaci_za_stampu:
            ukupno_nabavna += red[3]
            ukupno_otpisana += red[12]
            redni_broj += 1

            naziv = self.zamena_slova(red[2])
            nabavna = locale.format_string('%10.2f', red[3], grouping=True)
            otpisana = locale.format_string('%10.2f', red[12], grouping=True)

            pdf.cell(1, 1, str(redni_broj), 0, 0, 'C')
            pdf.cell(2, 1, str(red[1]), 0, 0, 'C')
            pdf.cell(8, 1, naziv, 0, 0, 'L')
            pdf.cell(4, 1, nabavna, 0, 0, 'R')
            pdf.cell(4, 1, otpisana, 0, 1, 'R')

        # ovo mora zbog prikaza naseg formata brojeva na pdf izvestaju 
        format_ukupno_nabavna = locale.format_string('%10.2f', ukupno_nabavna, grouping=True)
        format_ukupno_otpisana = locale.format_string('%10.2f', ukupno_otpisana, grouping=True)

        # UKUPNO ZA DOKUMENT
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(1, 1, '', 0, 0, 'C', fill=True)
        pdf.cell(2, 1, '', 0, 0, 'C', fill=True)
        pdf.cell(8, 1, 'UKUPNO:', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, format_ukupno_nabavna, 0, 0, 'R', fill=True)
        pdf.cell(4, 1, format_ukupno_otpisana, 0, 1, 'R', fill=True)

        pdf.cell(20, 2, '', 0, 1, 'C')
        pdf.cell(20, 1, 'Rekapitulacija po kontima:', 0, 1, 'C')
        # rekapitulacija po kontima
        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(3, 1, 'Konto', 0, 0, 'C', fill=True)
        pdf.cell(8, 1, 'Naziv', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Nabavna vrednost', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Otpisana vrednost', 0, 1, 'C', fill=True)
        pdf.set_font('Helvetica', '', 9)

        ukupno_rekapitulacija_nabavna = 0
        ukupno_rekapitulacija_otpisana = 0

        for red in rekapitulacija:
            ukupno_rekapitulacija_nabavna += red[2]
            ukupno_rekapitulacija_otpisana += red[3]

            naziv = self.zamena_slova(red[1])
            rek_nabavna = locale.format_string('%10.2f', red[2], grouping=True)
            rek_otpisana = locale.format_string('%10.2f', red[3], grouping=True)

            pdf.cell(3, 1, red[0], 0, 0, 'C')
            pdf.cell(8, 1, naziv, 0, 0, 'L')
            pdf.cell(4, 1, rek_nabavna, 0, 0, 'R')
            pdf.cell(4, 1, rek_otpisana, 0, 1, 'R')

        # ovo mora zbog prikaza naseg formata brojeva na pdf izvestaju
        format_ukupno_rekapitulacija_nabavna = locale.format_string('%10.2f', ukupno_rekapitulacija_nabavna, grouping=True)
        format_ukupno_rekapitulacija_otpisana = locale.format_string('%10.2f', ukupno_rekapitulacija_otpisana, grouping=True)

        # UKUPNO ZA DOKUMENT
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(3, 1, '', 0, 0, 'C', fill=True)
        pdf.cell(8, 1, 'UKUPNO:', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, format_ukupno_rekapitulacija_nabavna, 0, 0, 'R', fill=True)
        pdf.cell(4, 1, format_ukupno_rekapitulacija_otpisana, 0, 1, 'R', fill=True)

        pdf.output('faktura.pdf', 'F')

        webbrowser.open_new(r'faktura.pdf')

    def stampa_popisne_liste_za_popisivanje(self, podaci_za_stampu, datum):
        locale.setlocale(locale.LC_ALL, 'de_DE')

        pdf = PDF('portrait', 'cm', 'A4')
        pdf.add_page()
        pdf.set_font('Helvetica', '', 8)
        #pdf.line(1, 2.5, 20, 2.5)
        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y.")

        pdf.cell(17, 1, 'Datum izvestaja:', 0, 0, 'R')
        pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
        # pdf.cell(27, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(20, 2, 'Popisna lista na dan: ' + datum, 0, 1, 'C')

        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
        pdf.cell(2, 1, 'Inv.broj', 0, 0, 'C', fill=True)
        pdf.cell(9, 1, 'Naziv', 0, 0, 'L', fill=True)
        pdf.cell(3, 1, 'Sadasnja vrednost', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Napomena', 0, 1, 'C', fill=True)

        pdf.set_font('Helvetica', '', 10)
        brojac = 0
        for red in podaci_za_stampu:
            brojac += 1
            naziv_os = self.zamena_slova(red[1])
            sadasnja = locale.format_string('%10.2f', red[2], grouping=True)

            pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
            pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
            pdf.cell(9, 0.5, naziv_os, 0, 0, 'L')
            pdf.cell(3, 0.5, sadasnja, 0, 0, 'R')
            pdf.cell(4, 0.5, "________________", 0, 1, 'C')

        pdf.cell(3, 2, "Popisna komisija:", 0, 1, 'C')
        pdf.cell(9, 1, "1. _____________________________", 0, 1, 'L')
        pdf.cell(9, 1, "2. _____________________________", 0, 1, 'L')
        pdf.cell(9, 1, "3. _____________________________", 0, 1, 'L')

        pdf.output('popisna_lista.pdf', 'F')
        webbrowser.open_new(r'popisna_lista.pdf')

    def stampa_popisne_liste_sortirano(self, podaci_za_stampu, datum):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        pdf = PDF('landscape', 'cm', 'A4')
        pdf.add_page()
        pdf.set_font('Helvetica', '', 8)
        #pdf.line(1, 2.5, 28, 2.5)
        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y.")

        pdf.cell(24, 1, 'Datum izvestaja:', 0, 0, 'R')
        pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
        # pdf.cell(27, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(20, 2, 'Popisna lista na dan: ' + datum, 0, 1, 'C')

        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
        pdf.cell(2, 1, 'Inv.broj', 0, 0, 'C', fill=True)
        pdf.cell(9, 1, 'Naziv', 0, 0, 'L', fill=True)
        pdf.cell(3, 1, 'Sadasnja vrednost', 0, 0, 'C', fill=True)
        pdf.cell(5, 1, 'Korisnik', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Lokacija', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Napomena', 0, 1, 'C', fill=True)

        pdf.set_font('Helvetica', '', 10)
        brojac = 0
        for red in podaci_za_stampu:
            brojac += 1
            naziv_os = self.zamena_slova(red[1])
            sadasnja = locale.format_string('%10.2f', red[2], grouping=True)
            korisnik_os = self.zamena_slova(red[3])
            lokacija_os = self.zamena_slova(red[4])

            pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
            pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
            pdf.cell(9, 0.5, naziv_os, 0, 0, 'L')
            pdf.cell(3, 0.5, sadasnja, 0, 0, 'R')
            pdf.cell(5, 0.5, korisnik_os, 0, 0, 'R')
            pdf.cell(4, 0.5, lokacija_os, 0, 0, 'R')
            pdf.cell(4, 0.5, "________________", 0, 1, 'C')

        pdf.cell(3, 2, "Popisna komisija:", 0, 1, 'C')
        pdf.cell(9, 1, "1. _____________________________", 0, 1, 'L')
        pdf.cell(9, 1, "2. _____________________________", 0, 1, 'L')
        pdf.cell(9, 1, "3. _____________________________", 0, 1, 'L')

        pdf.output('popisna_lista_sortirano.pdf', 'F')
        webbrowser.open_new(r'popisna_lista_sortirano.pdf')

    def stampa_popisne_liste_po_kancelarijama(self, podaci_za_stampu, datum):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        pdf = PDF('landscape', 'cm', 'A4')

        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y.")
        brojac = 0
        lokacija = ""
        for red in podaci_za_stampu:
            if lokacija != red[4]:
                pdf.add_page()
                pdf.set_font('Helvetica', '', 8)
                #pdf.line(1, 2.5, 28, 2.5)
                lokacija_os = self.zamena_slova(red[4])
                pdf.cell(24, 1, 'Datum izvestaja:', 0, 0, 'R')
                pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
                # pdf.cell(27, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
                pdf.set_font('Helvetica', 'B', 12)
                pdf.cell(20, 2, 'Popisna lista u kancelariji ' + lokacija_os + ' na dan: ' + datum, 0, 1, 'C')

                pdf.set_fill_color(206, 206, 206)
                pdf.set_font('Helvetica', 'B', 8)
                pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
                pdf.cell(2, 1, 'Inv.broj', 0, 0, 'C', fill=True)
                pdf.cell(13, 1, 'Naziv', 0, 0, 'L', fill=True)
                pdf.cell(3, 1, 'Sadasnja vrednost', 0, 0, 'C', fill=True)
                pdf.cell(5, 1, 'Korisnik', 0, 0, 'C', fill=True)
                #pdf.cell(4, 1, 'Lokacija', 0, 0, 'C', fill=True)
                pdf.cell(4, 1, 'Napomena', 0, 1, 'C', fill=True)
                brojac = 0
                pdf.set_font('Helvetica', '', 10)
                brojac += 1
                naziv_os = self.zamena_slova(red[1])
                sadasnja = locale.format_string('%10.2f', red[2], grouping=True)
                korisnik_os = self.zamena_slova(red[3])

                pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
                pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
                pdf.cell(13, 0.5, naziv_os, 0, 0, 'L')
                pdf.cell(3, 0.5, sadasnja, 0, 0, 'R')
                pdf.cell(5, 0.5, korisnik_os, 0, 0, 'R')
                #pdf.cell(4, 0.5, lokacija_os, 0, 0, 'R')
                pdf.cell(4, 0.5, "________________", 0, 1, 'C')

            else:
                pdf.set_font('Helvetica', '', 10)
                brojac += 1
                naziv_os = self.zamena_slova(red[1])
                sadasnja = locale.format_string('%10.2f', red[2], grouping=True)
                korisnik_os = self.zamena_slova(red[3])

                pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
                pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
                pdf.cell(13, 0.5, naziv_os, 0, 0, 'L')
                pdf.cell(3, 0.5, sadasnja, 0, 0, 'R')
                pdf.cell(5, 0.5, korisnik_os, 0, 0, 'R')
                # pdf.cell(4, 0.5, lokacija_os, 0, 0, 'R')
                pdf.cell(4, 0.5, "________________", 0, 1, 'C')
            lokacija = red[4]

        pdf.output('popisna_lista_kancelarije.pdf', 'F')
        webbrowser.open_new(r'popisna_lista_kancelarije.pdf')

    def stampa_popisne_liste_po_amortizacionim_grupama(self, podaci_za_stampu, datum):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        pdf = PDF('portrait', 'cm', 'A4')

        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y.")
        brojac = 0
        grupa = ""
        for red in podaci_za_stampu:
            if grupa != red[3]:
                pdf.add_page()
                pdf.set_font('Helvetica', '', 10)
                #pdf.line(1, 2.5, 28, 2.5)
                sifra_grupe = self.zamena_slova(red[3])
                naziv_grupe = self.zamena_slova(red[4])
                pdf.cell(17, 1, 'Datum izvestaja:', 0, 0, 'R')
                pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
                # pdf.cell(27, 1, 'Strana: ' + str(pdf.page_no()), 0, 1, 'R')
                pdf.set_font('Helvetica', 'B', 12)
                pdf.cell(20, 1, 'Popisna lista amortizacione grupe ' + sifra_grupe + ' na dan: ' + datum, 0, 1, 'C')
                pdf.cell(20, 1, naziv_grupe, 0, 1, 'C')
                pdf.cell(20, 1, 'Stopa: ' + str(red[5]) + '%', 0, 1, 'C')

                pdf.set_fill_color(206, 206, 206)
                pdf.set_font('Helvetica', 'B', 8)
                pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
                pdf.cell(2, 1, 'Inv.broj', 0, 0, 'C', fill=True)
                pdf.cell(9, 1, 'Naziv', 0, 0, 'L', fill=True)
                pdf.cell(3, 1, 'Sadasnja vrednost', 0, 0, 'C', fill=True)
                #pdf.cell(5, 1, 'Korisnik', 0, 0, 'C', fill=True)
                #pdf.cell(4, 1, 'Lokacija', 0, 0, 'C', fill=True)
                pdf.cell(4, 1, 'Napomena', 0, 1, 'C', fill=True)
                brojac = 0
                pdf.set_font('Helvetica', '', 10)
                brojac += 1
                naziv_os = self.zamena_slova(red[1])
                sadasnja = locale.format_string('%10.2f', red[2], grouping=True)
                #korisnik_os = self.zamena_slova(red[3])

                pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
                pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
                pdf.cell(9, 0.5, naziv_os, 0, 0, 'L')
                pdf.cell(3, 0.5, sadasnja, 0, 0, 'R')
                #pdf.cell(5, 0.5, korisnik_os, 0, 0, 'R')
                #pdf.cell(4, 0.5, lokacija_os, 0, 0, 'R')
                pdf.cell(4, 0.5, "________________", 0, 1, 'C')

            else:
                pdf.set_font('Helvetica', '', 10)
                brojac += 1
                naziv_os = self.zamena_slova(red[1])
                sadasnja = locale.format_string('%10.2f', red[2], grouping=True)
                #korisnik_os = self.zamena_slova(red[3])

                pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
                pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
                pdf.cell(9, 0.5, naziv_os, 0, 0, 'L')
                pdf.cell(3, 0.5, sadasnja, 0, 0, 'R')
                #pdf.cell(5, 0.5, korisnik_os, 0, 0, 'R')
                # pdf.cell(4, 0.5, lokacija_os, 0, 0, 'R')
                pdf.cell(4, 0.5, "________________", 0, 1, 'C')
            grupa = red[3]

        pdf.output('popisna_lista_amortizacione_grupe.pdf', 'F')
        webbrowser.open_new(r'popisna_lista_amortizacione_grupe.pdf')

    def stampa_popisa_nabavljene_opreme(self, podaci_za_stampu, pocetni, krajnji):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        pdf = PDF('landscape', 'cm', 'A4')
        pdf.add_page()
        pdf.set_font('Helvetica', '', 10)
        #pdf.line(1, 2.5, 28, 2.5)
        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y.")

        pdf.cell(24, 1, 'Datum izvestaja:', 0, 0, 'R')
        pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(27, 2, 'Nabavljena oprema u periodu od ' + pocetni.strftime("%d.%m.%Y.") + ' do ' + krajnji.strftime("%d.%m.%Y."), 0, 1, 'C')

        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
        pdf.cell(2, 1, 'Inv.broj', 0, 0, 'C', fill=True)
        pdf.cell(9, 1, 'Naziv', 0, 0, 'L', fill=True)
        pdf.cell(3, 1, 'Nabavna vrednost', 0, 0, 'C', fill=True)
        pdf.cell(5, 1, 'Datum nabavke', 0, 0, 'C', fill=True)
        pdf.cell(4, 1, 'Broj dokumenta', 0, 0, 'L', fill=True)
        pdf.cell(4, 1, 'Dobavljac', 0, 1, 'L', fill=True)

        pdf.set_font('Helvetica', '', 10)
        brojac = 0
        ukupno_vrednost = 0
        for red in podaci_za_stampu:
            brojac += 1
            ukupno_vrednost += red[2]
            naziv_os = self.zamena_slova(red[1])
            nabavna = locale.format_string('%10.2f', red[2], grouping=True)
            datum_nabavke = red[3].strftime("%d.%m.%Y.")
            broj = self.zamena_slova(red[4])
            dobavljac = self.zamena_slova(red[5])

            pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
            pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
            pdf.cell(9, 0.5, naziv_os, 0, 0, 'L')
            pdf.cell(3, 0.5, nabavna, 0, 0, 'R')
            pdf.cell(5, 0.5, datum_nabavke, 0, 0, 'C')
            pdf.cell(4, 0.5, broj, 0, 0, 'L')
            pdf.cell(4, 0.5, dobavljac, 0, 1, 'L')

        ukupno = locale.format_string('%10.2f', ukupno_vrednost, grouping=True)
        # UKUPNO ZA DOKUMENT
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(1, 0.5, '', 0, 0, 'C', fill=True)
        pdf.cell(2, 0.5, '', 0, 0, 'C', fill=True)
        pdf.cell(9, 0.5, 'UKUPNO:', 0, 0, 'L', fill=True)
        pdf.cell(3, 0.5, ukupno, 0, 0, 'R', fill=True)
        pdf.cell(5, 0.5, '', 0, 0, 'R', fill=True)
        pdf.cell(4, 0.5, '', 0, 0, 'C', fill=True)
        pdf.cell(4, 0.5, '', 0, 1, 'R', fill=True)

        pdf.output('lista_nabavljene_opreme.pdf', 'F')
        webbrowser.open_new(r'lista_nabavljene_opreme.pdf')

    def stampa_popisa_rashodovane_opreme(self, podaci_za_stampu, pocetni, krajnji):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        pdf = PDF('landscape', 'cm', 'A4')
        pdf.add_page()
        pdf.set_font('Helvetica', '', 10)
        #pdf.line(1, 2.5, 28, 2.5)
        today = date.today()
        danasnji_datum = today.strftime("%d.%m.%Y.")

        pdf.cell(24, 1, 'Datum izvestaja:', 0, 0, 'R')
        pdf.cell(3, 1, danasnji_datum, 0, 1, 'L')
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(27, 2, 'Rashodovana oprema u periodu od ' + pocetni.strftime("%d.%m.%Y.") + ' do ' + krajnji.strftime("%d.%m.%Y."), 0, 1, 'C')

        pdf.set_fill_color(206, 206, 206)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(1, 1, 'R.br.', 0, 0, 'C', fill=True)
        pdf.cell(2, 1, 'Inv.broj', 0, 0, 'C', fill=True)
        pdf.cell(12, 1, 'Naziv', 0, 0, 'L', fill=True)
        pdf.cell(3, 1, 'Preostala vrednost', 0, 0, 'C', fill=True)
        pdf.cell(5, 1, 'Datum rashoda', 0, 0, 'C', fill=True)
        pdf.cell(5, 1, 'Broj dokumenta', 0, 1, 'L', fill=True)

        pdf.set_font('Helvetica', '', 10)
        brojac = 0
        ukupno_vrednost = 0
        for red in podaci_za_stampu:
            brojac += 1
            ukupno_vrednost += red[2]
            naziv_os = self.zamena_slova(red[1])
            nabavna = locale.format_string('%10.2f', red[2], grouping=True)
            datum_rashoda = red[3].strftime("%d.%m.%Y.")
            broj = self.zamena_slova(red[4])

            pdf.cell(1, 0.5, str(brojac) + ".", 0, 0, 'C')
            pdf.cell(2, 0.5, str(red[0]), 0, 0, 'C')
            pdf.cell(12, 0.5, naziv_os, 0, 0, 'L')
            pdf.cell(3, 0.5, nabavna, 0, 0, 'R')
            pdf.cell(5, 0.5, datum_rashoda, 0, 0, 'C')
            pdf.cell(5, 0.5, broj, 0, 1, 'L')

        ukupno = locale.format_string('%10.2f', ukupno_vrednost, grouping=True)
        # UKUPNO ZA DOKUMENT
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(1, 0.5, '', 0, 0, 'C', fill=True)
        pdf.cell(2, 0.5, '', 0, 0, 'C', fill=True)
        pdf.cell(12, 0.5, 'UKUPNO:', 0, 0, 'L', fill=True)
        pdf.cell(3, 0.5, ukupno, 0, 0, 'R', fill=True)
        pdf.cell(5, 0.5, '', 0, 0, 'R', fill=True)
        pdf.cell(5, 0.5, '', 0, 1, 'C', fill=True)

        pdf.output('lista_rashodovane_opreme.pdf', 'F')
        webbrowser.open_new(r'lista_rashodovane_opreme.pdf')


