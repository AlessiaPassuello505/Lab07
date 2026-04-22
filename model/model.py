from database.meteo_dao import MeteoDao as DAO

class Model:
    def __init__(self):
        pass

    def get_umidita_media(self,mese):
        return DAO.get_umidita_media(mese)

    def get_umidita_15(self,mese):
        return DAO.get_umidita_15(mese)

    def calcola_percorso(self, mese):
        # Recuperiamo i dati dal DAO e li organizziamo per un accesso rapido
        dati_db = DAO.get_umidita_15(mese)
        # Creiamo una mappa: giorno -> {citta: umidita}
        self._mappa_umidita = {}
        for s in dati_db:
            g = s.data.day
            if g not in self._mappa_umidita:
                self._mappa_umidita[g] = {}
            self._mappa_umidita[g][s.localita] = s.umidita

        self._citta_disponibili = ["Milano", "Torino", "Genova"]
        self._percorso_migliore = []
        self._costo_minimo = float('inf')
         # Lanciamo la ricorsione partendo dal giorno 1 con percorso vuoto
        self._ricorsione([], 1,0)

        return self._percorso_migliore, self._costo_minimo

    def _ricorsione(self, parziale, giorno,costo):
        # CASO TERMINALE: abbiamo pianificato tutti i 15 giorni
        if giorno == 16:
            if costo < self._costo_minimo:
                self._costo_minimo = costo
                self._percorso_migliore = list(parziale)
            return

        # Prova a inserire una delle 3 città per il giorno attuale
        if self._vinc_ammissibile(parziale, citta):
            # CALCOLO COSTO ISTANTANEO
            nuovo_costo = costo + self._mappa_umidita[giorno][citta]

            # Aggiungo 100 solo se cambio città
            if len(parziale) > 0 and citta != parziale[-1]:
                nuovo_costo += 100

            # PRUNING: Procedo solo se il costo attuale è già migliore del record
            if nuovo_costo < self._costo_minimo:
                parziale.append(citta)
                self._ricorsione(parziale, giorno + 1, nuovo_costo)
                parziale.pop()

    def _vinc_ammissibile(self, parziale, nuova_citta):
        # Vincolo 1: Massimo 6 giorni per città
        if parziale.count(nuova_citta) >= 6:
            return False

        # Vincolo 2: Permanenza minima di 3 giorni consecutivi
        if len(parziale) > 0:
            # Se stiamo cambiando città...
            if nuova_citta != parziale[-1]:
                # ...dobbiamo aver passato almeno 3 giorni nell'ultima
                if len(parziale) < 3:
                    return False
                if not (parziale[-1] == parziale[-2] == parziale[-3]):
                    return False

        # Vincolo extra: se ho iniziato una città ma sono al giorno 2, devo continuare
        if 1 < len(parziale) < 3:
            if nuova_citta != parziale[-1]:
                return False

        return True

    def _calcola_costo_totale(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            giorno = i + 1
            citta_attuale = parziale[i]

            # Aggiungo l'umidità del giorno (sempre presente)
            costo += self._mappa_umidita[giorno][citta_attuale]

            # Aggiungo il costo di spostamento (100) se la città cambia rispetto al giorno prima
            if i > 0 and parziale[i] != parziale[i - 1]:
                costo += 100
        return costo