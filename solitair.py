from cards import Karte, Stapel, AnlageStapel, AblageStapel, Farbe, KartenTyp
from ascii import AsciiScreen, AsciiKarte


class Solitair(object):
    def __init__(self) -> None:
        self.ziehStapel = Stapel(karten=[Karte(col, type) for col in list(Farbe)
                                         for type in list(KartenTyp)])
        self.ablageStapel = Stapel()
        self.ablageHerz = AblageStapel(farbe=Farbe.HERZ)
        self.ablageKaro = AblageStapel(farbe=Farbe.KARO)
        self.ablageKreuz = AblageStapel(farbe=Farbe.KREUZ)
        self.ablagePik = AblageStapel(farbe=Farbe.PIK)
        self.anlageStapel = [AnlageStapel() for i in range(7)]
        self.screen = AsciiScreen(width=70, height=35)

    def _draw_card(self, karte: Karte) -> str:
        blatt = AsciiKarte.back()
        if karte:
            blatt = AsciiKarte.front(karte)
        return blatt
    
    def _draw_anlage_stapel(self, stapel: AnlageStapel) -> str:
        return self._draw_card(stapel.top())

    def _draw(self):
        for idx, a in enumerate([self.ablageHerz, self.ablageKaro, self.ablagePik, self.ablageKreuz]):
            self.screen.write_to_screen(self._draw_card(
                a.top()), AsciiKarte.width()*idx, 0)

        self.screen.write_to_screen(self._draw_card(
            self.ablageStapel.top()), self.screen.width - AsciiKarte.width()*2, 0)
        self.screen.write_to_screen(self._draw_card(
            self.ziehStapel.top()), self.screen.width - AsciiKarte.width(), 0)

        for idx, a in enumerate(self.anlageStapel):
            self.screen.write_to_screen(self._draw_anlage_stapel(a), AsciiKarte.width()*idx, AsciiKarte.height()+3)

        self.screen.write_to_screen(self._menu(), 0, AsciiKarte.height() + 26)
        self.screen.print()

    def _menu(self):
        return """─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 z: ziehen          a: anlegen          l: ablegen 
 m: verschieben     x: Spiel beenden"""

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
            k = self.ziehStapel.ziehen()
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
            pass


def main():
    '''
    The enty program for the solitair program
    '''
    s = Solitair()
    s._draw()


if __name__ == "__main__":
    main()
