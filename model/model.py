from database.meteo_dao import MeteoDao as DAO

class Model:
    def __init__(self):
        self._citta_disponibili = ["Milano", "Torino", "Genova"]
        self._percorso_migliore = []
        self._costo_minimo = float('inf')
        self._mappa_umidita={}

    def get_umidita_media(self,mese):
        return DAO.get_umidita_media(mese)

    def get_umidita_15(self,mese):
        return DAO.get_umidita_15(mese)

    def calcola_percorso(self, mese):
        # Recuperiamo i dati dal DAO e li organizziamo per un accesso rapido
        dati_db = DAO.get_umidita_15(mese)
        self._mappa_umidita={}
        # Creiamo una mappa: giorno -> {citta: umidita}
        for s in dati_db:
            g = s.data.day
            if g not in self._mappa_umidita:
                self._mappa_umidita[g] = {}
            self._mappa_umidita[g][s.localita] = s.umidita
        # Lanciamo la ricorsione partendo dal giorno 1 con percorso vuoto

        self._costo_minimo=float('inf')
        self._percorso_migliore=[]
        self._ricorsione([], 0)

        return self._percorso_migliore, self._costo_minimo

    def get_umidita_specifica(self, giorno, citta):
        return self._mappa_umidita[giorno][citta]

    def _ricorsione(self, parziale,costo):
        giorno=len(parziale)+1
        # CASO TERMINALE: abbiamo pianificato tutti i 15 giorni
        if giorno == 16:
            if costo < self._costo_minimo:
                print(f"Nuovo record trovato! Costo: {costo}")
                self._costo_minimo = costo
                self._percorso_migliore = list(parziale)
            return

        # Prova a inserire una delle 3 città per il giorno attuale
        for citta in self._citta_disponibili:
            if self._vinc_ammissibile(parziale, citta):
                # CALCOLO COSTO ISTANTANEO
                nuovo_costo = costo + self._mappa_umidita[giorno][citta]
                # Aggiungo 100 solo se cambio città
                if len(parziale) > 0 and citta != parziale[-1]:
                    nuovo_costo += 100

                # PRUNING: taglio rami inutili
                if nuovo_costo < self._costo_minimo:
                    parziale.append(citta)
                    self._ricorsione(parziale, nuovo_costo)
                    parziale.pop()

    def _vinc_ammissibile(self, parziale, citta):
        # Vincolo 1: Massimo 6 giorni per città
        if parziale.count(citta) >= 6:
            return False
        # Vincolo 2: Permanenza minima di 3 giorni consecutivi
        if len(parziale) == 0:
            return True
        ultima_citta=parziale[-1]
        # Se stiamo cambiando città...
        if citta != ultima_citta:
                # ...dobbiamo aver passato almeno 3 giorni nell'ultima
                if len(parziale) < 3:
                    return False
                if not (parziale[-1] == parziale[-2] == parziale[-3]):
                    return False
        return True


