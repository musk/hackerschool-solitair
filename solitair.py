from cards import Karte, Stapel, AnlageStapel, AblageStapel, Farbe


class Solitair(object):
    def __init__(self) -> None:
        self.stapel = Stapel()
        self.ablageHerz = AblageStapel(farbe=Farbe.HERZ)
        self.ablageKaro = AblageStapel(farbe=Farbe.KARO)
        self.ablageKreuz = AblageStapel(farbe=Farbe.KREUZ)
        self.ablagePik = AblageStapel(farbe=Farbe.PIK)
        self.anlageStapel = [AnlageStapel() for i in range(7)]

    def _draw(self):
        pass

    def _menu(self):
        return """
z: Karte vom Stapel ziehen                  a: Karte auf Stapel x anlegen       l: Karte auf Ablagestapel legen 
m: Karten von Stapel x zu y verschieben     x: Spiel beenden"""

    def _waehle_anlage(self) -> AnlageStapel:
        nummer = -1
        while nummer < 0 or nummer >= 7:
            nummer = input("Auf welchen Stapel wollen sie die Karte anlegen?")
            if nummer < 0 or nummer >= 7:
                print("Bitte geben sie eine Zahlt zwischen 0 und 7 an!")
        return self.anlageStapel[nummer]

    def _waehle_ablage(self) -> AblageStapel:
        while True:
            eingabe = input(
                "Auf welchen Ablagestapel soll die Karte abgelegt werden? h: Herz k: Karo p: Pik z: Kreuz")
            if eingabe == "h":
                return self.ablageHerz
            elif eingabe == "k":
                return self.ablageKaro
            elif eingabe == "p":
                return self.ablagePik
            elif eingabe == "z":
                return self.ablageKreuz
            else:
                print("Bitte wählen sie eine gültige eingabe!")

    def _input(self):
        eingabe: str = input("Zug? ").lower().strip()
        if eingabe == "a":
            a = self._waehle_anlage()
            k = self.stapel.ziehen()
            a.anlegen(k)
        elif eingabe == "l":
            a = self._waehle_ablage()
            k = self._waehle_anlage()
            
            pass
        elif eingabe == "m":
            pass
        elif eingabe == "x":
            print("Herzlichen Dank das sie Solitair gespielt haben!")
            exit(0)
        elif eingabe == "z":
            pass

    def play(self):
        # the game loop
        while True:


def main():
    '''
    The enty program for the solitair program
    '''
    deck = Stapel()
    print(deck)
    print()
    deck.shuffle()
    print(deck)


if __name__ == "__main__":
    main()
