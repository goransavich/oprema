
class DimenzijeProzora:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    # Sirina prozora podesavanja - unos dobavljaca, unos konta
    def odredi_sirinu_prozori_podesavanja(self):
        if self.screen_width < 1400:
            return self.screen_width - 200
        else:
            return self.screen_width - 1000

    # Visina prozora podesavanja - unos dobavljaca, unos konta...
    def odredi_visinu_prozori_podesavanja(self):
        if self.screen_height < 800:
            return self.screen_height - 180
        else:
            return self.screen_height - 500

    # Sirina prozora Unos opreme
    def odredi_sirinu_unos_opreme(self):
        if self.screen_width < 1400:
            return self.screen_width - 300
        else:
            return self.screen_width - 850

    # Visina prozora Unos opreme
    def odredi_visinu_unos_opreme(self):
        if self.screen_height < 800:
            return self.screen_height - 120
        else:
            return self.screen_height - 200

    # Sirina prozor amortizacije
    def odredi_sirinu_amortizacija(self):
        if self.screen_width < 1400:
            return self.screen_width - 100
        else:
            return self.screen_width - 600

    # Visina prozor amortizacije
    def odredi_visinu_amortizacija(self):
        if self.screen_height < 800:
            return self.screen_height - 80
        elif 800 < self.screen_height < 1000:
            return self.screen_height - 300
        else:
            return self.screen_height - 600

    # Sirina prozor izmena osnovnog sredstva
    def odredi_sirinu_izmena(self):
        if self.screen_width < 1100:
            return self.screen_width - 100
        elif 1100 < self.screen_width < 1500:
            return self.screen_width - 500
        else:
            return self.screen_width - 900

    # Visina prozor izmena osnovnog sredstva
    def odredi_visinu_izmena(self):
        if self.screen_height < 800:
            return self.screen_height - 80
        elif 800 < self.screen_height < 1000:
            return self.screen_height - 200
        else:
            return self.screen_height - 450

    # Sirina prozora Rashod opreme
    def odredi_sirinu_rashod_opreme(self):
        if self.screen_width < 1400:
            return self.screen_width - 100
        else:
            return self.screen_width - 400

    # Visina prozora Rashod opreme
    def odredi_visinu_rashod_opreme(self):
        if self.screen_height < 800:
            return self.screen_height - 80
        else:
            return self.screen_height - 200

    # Sirina prozora podesavanja - mesto
    def odredi_sirinu_mesto(self):
        if self.screen_width < 1400:
            return self.screen_width - 200
        else:
            return self.screen_width - 1200

    # Visina prozora podesavanja - mesto...
    def odredi_visinu_mesto(self):
        if self.screen_height < 800:
            return self.screen_height - 180
        else:
            return self.screen_height - 500

    '''
     # Sirina prozora Zakljucni list
    def odredi_sirinu_svi_nalozi(self):
        if self.screen_width < 1400:
            return self.screen_width - 120
        else:
            return self.screen_width - 400

    # Visina prozora Kartica konta i Stanje konta
    def odredi_visinu_svi_nalozi(self):
        if self.screen_height < 800:
            return self.screen_height - 180
        else:
            return self.screen_height - 520

    # Visina prozora Zakljucni list
    def odredi_visinu_zakljucni_list(self):
        if self.screen_height < 800:
            return self.screen_height - 140
        else:
            return self.screen_height - 400
    '''
    # Sirina prozora Kreiran nalog
    def odredi_sirinu_kreiran_nalog(self):
        if self.screen_width < 1400:
            return self.screen_width - 100
        else:
            return self.screen_width - 300
        
    # Visina prozora Kreiran nalog
    def odredi_visinu_kreiran_nalog(self):
        if self.screen_height < 800:
            return self.screen_height - 80
        else:
            return self.screen_height - 120



