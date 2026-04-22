import flet as ft

from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        mese=self._view.dd_mese.value
        umidita=self._model.get_umidita_media(mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        for e in umidita:
            self._view.lst_result.controls.append(ft.Text(f"{e[0]}:{e[1]}"))
        self._view.update_page()


    def handle_sequenza(self, e):
        mese = self._view.dd_mese.value

        self._view.lst_result.controls.clear()
        percorso_migliore,costo_min=self._model.calcola_percorso(mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo_min}  ed è :"))

        for p in percorso_migliore:
            self._view.lst_result.controls.append(ft.Text(p))
        self._view.update_page()



    def read_mese(self, e):
        self._mese = int(e.control.value)

