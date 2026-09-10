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


class BatteurOeufs(Commis):
    def __init__(self, nom, recipient):
        super().__init__(nom)
        self.recipient = recipient

    def run(self):
        # on suppose qu'il faut 8 tours de batteur par œuf présent dans le bol
        oeuf = self.recipient.contenu
        nb_tours = oeuf.quantite * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"\tJe bats les {oeuf.quantite} oeufs, tour n°{no_tour}")
            time.sleep(0.5)  # temps supposé d'un tour de batteur


class FondeurChocolat(Commis):
    def __init__(self, nom, recipient):
        super().__init__(nom)
        self.recipient = recipient  # en grammes

    def run(self):
        print("Je mets de l'eau à chauffer dans une bouilloire")
        time.sleep(8)
        print("Je verse l'eau dans une casserole")
        time.sleep(2)
        print("J'y pose le bol rempli de chocolat")
        time.sleep(1)
        # on suppose qu'il faut 1 tour de spatule par 10 g. de chocolat
        # présent dans le bol pour faire fondre le chocolat
        chocolat = self.recipient.contenu
        nb_tours = math.ceil(chocolat.quantite / 10)
        for no_tour in range(1, nb_tours + 1):
            print(f"Je mélange {chocolat.quantite} de chocolat à fondre, tour n°{no_tour}")
            time.sleep(1)  # temps supposé d'un tour de spatule

class Appareil:
    """Mélange homogène d'ingrédients servant de base à une préparation."""

    def __init__(self, nom: str):
        self.nom = nom
        self.ingredients = {}

    def add_ingredient(self, nom: str, quantite: float, unite: str):
        self.ingredients[nom] = Ingredient(nom, quantite, unite)

    def quantite(self, nom: str):
        return self.ingredients[nom].quantite

class Recipient:
    """Récipient contenant l'ingrédient ou l'appareil qui est travaillé."""

    def __init__(self, nom: str, contenu):
        self.nom = nom
        self.contenu = contenu

    def __str__(self):
        return self.nom

def main():
    cul_de_poule = Recipient("le cul-de-poule", Oeuf(6))
    bol_chocolat_1 = Recipient("le bol de chocolat n°1", Chocolat(100))
    bol_chocolat_2 = Recipient("le bol de chocolat n°2", Chocolat(100))

    batteur = BatteurOeufs("Alice, commis batteur", cul_de_poule)
    fondeur_1 = FondeurChocolat("Basile, commis fondeur", bol_chocolat_1)
    fondeur_2 = FondeurChocolat("Chloé, commis fondeur", bol_chocolat_2)

    batteur.start()
    fondeur_1.start()
    fondeur_2.start()
    batteur.join()
    fondeur_1.join()
    fondeur_2.join()

if __name__ == "__main__":
    main()
