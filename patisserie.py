import threading
import time
import math
from abc import ABC, abstractmethod

class Commis(threading.Thread, ABC):
    def __init__(self, nom):
        super().__init__(name=nom)
        self.nom = nom

    @abstractmethod
    def run(self):
        pass

class Ingredient(ABC):
    """Classe abstraite représentant un ingrédient mesurable."""

    def __init__(self, nom: str, quantite: float, unite: str):
        self.nom = nom
        self.quantite = quantite
        self.unite = unite

    def __str__(self):
        return f"{self.quantite:g} {self.unite} de {self.nom}"


class Oeuf(Ingredient):
    def __init__(self, quantite: int):
        super().__init__("oeuf", quantite, "pièce(s)")


class Chocolat(Ingredient):
    def __init__(self, quantite: float):
        super().__init__("chocolat", quantite, "g")


class BatteurOeufs(threading.Thread):
    def __init__(self, nb_oeufs):
        threading.Thread.__init__(self)
        self.nb_oeufs = nb_oeufs

    def run(self):
        # on suppose qu'il faut 8 tours de batteur par œuf présent dans le bol
        nb_tours = self.nb_oeufs * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"\tJe bats les {self.nb_oeufs} oeufs, tour n°{no_tour}")
            time.sleep(0.5)  # temps supposé d'un tour de batteur


class FondeurChocolat(threading.Thread):
    def __init__(self, quantite):
        threading.Thread.__init__(self)
        self.quantite = quantite  # en grammes

    def run(self):
        print("Je mets de l'eau à chauffer dans une bouilloire")
        time.sleep(8)
        print("Je verse l'eau dans une casserole")
        time.sleep(2)
        print("J'y pose le bol rempli de chocolat")
        time.sleep(1)
        # on suppose qu'il faut 1 tour de spatule par 10 g. de chocolat
        # présent dans le bol pour faire fondre le chocolat
        nb_tours = math.ceil(self.quantite / 10)
        for no_tour in range(1, nb_tours + 1):
            print(f"Je mélange {self.quantite} de chocolat à fondre, tour n°{no_tour}")
            time.sleep(1)  # temps supposé d'un tour de spatule


if __name__ == "__main__":
    batteur = BatteurOeufs(6)
    fondeur = FondeurChocolat(200)
    batteur.start()
    fondeur.start()
    batteur.join()
    fondeur.join()
    print("\nJe peux à présent incorporer le chocolat aux oeufs")
