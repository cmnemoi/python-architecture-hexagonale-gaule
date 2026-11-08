import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass


class Thermomix:
    def __init__(self, durée_d_un_palier_en_secondes: float = 0.3) -> None:
        self._durée_d_un_palier_en_secondes = durée_d_un_palier_en_secondes
        self._bol: ContenuDuBol | None = None
        self._degrés_actuels = 0
        self._degrés_souhaités = 0
        self._exécuteur = ThreadPoolExecutor(max_workers=1)

    # @spec cuiseur.thermomix::chauffe-progressivement
    def lancer_la_chauffe(self, degrés: int) -> None:
        self._degrés_souhaités = degrés
        self._exécuteur.submit(self._chauffer_jusqu_à, degrés)

    def lire_la_température(self) -> int:
        return self._degrés_actuels

    # @spec cuiseur.thermomix::refuse-cuisson-hors-temperature
    def cuire(self, nom: str, quantité: int) -> None:
        if self._degrés_actuels != self._degrés_souhaités:
            raise TempératureNonAtteinteException()
        self._bol = ContenuDuBol(nom=nom, quantité=quantité)

    def vider_le_bol(self) -> ContenuDuBol | None:
        contenu_du_bol = self._bol
        self._bol = None
        return contenu_du_bol

    def _chauffer_jusqu_à(self, degrés: int) -> None:
        while self._degrés_actuels < degrés:
            time.sleep(self._durée_d_un_palier_en_secondes)
            self._degrés_actuels += DEGRÉS_PAR_PALIER


@dataclass(frozen=True)
class ContenuDuBol:
    nom: str
    quantité: int


class TempératureNonAtteinteException(Exception):
    pass


DEGRÉS_PAR_PALIER = 10
