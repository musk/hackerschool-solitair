from cards import Karte, Stapel, AnlageStapel, AblageStapel, Farbe, KartenTyp
from ascii import AsciiScreen, AsciiKarte, AsciiStapel


class Solitair(object):

    COMMANDS = {"z": {"text": "[z]iehen", "method": f"self._ziehen()"},
                "a": {"text": "[a]nlegen", "method": f"self._anlegen()"},
                "l": {"text": "ab[l]egen", "method": f"self._ablegen()"},
                "v": {"text": "[v]erschieben", "method": f"self._verschieben()"},
                "u": {"text": "[u]mdrehen", "method": f"self._umdrehen()"},
                "b": {"text": "[b]eenden", "method": f"self._end()"}, }

    def __init__(self) -> None:
        self.ziehStapel = Stapel(karten=[Karte(col, type) for col in list(Farbe)
                                         for type in list(KartenTyp)], ablage=True)
        self.ziehStapel.shuffle()
        self.ablageStapel = Stapel()
        self.ablageHerz = AblageStapel(farbe=Farbe.HERZ)
        self.ablageKaro = AblageStapel(farbe=Farbe.KARO)
        self.ablageKreuz = AblageStapel(farbe=Farbe.KREUZ)
        self.ablagePik = AblageStapel(farbe=Farbe.PIK)
        self.anlageStapel = [AsciiStapel(AnlageStapel(
            karten=self._initAnlage(i+1))) for i in range(7)]
        self.screen = AsciiScreen(width=70, height=35)
        self.navigation = False
        self.status_msg = ""

    def _initAnlage(self, kartenZiehen: int) -> list[Karte]:
        karten = []
        for i in range(kartenZiehen):
            karten.append(self.ziehStapel.ziehen())
            if i == kartenZiehen-1:
                karten[i].aufdecken()
        return karten

    def _draw(self):
        for idx, a in enumerate([self.ablageHerz,
                                 self.ablageKaro,
                                 self.ablagePik,
                                 self.ablageKreuz]):
            self.screen.write_to_screen(AsciiKarte.print(a.top()),
                                        AsciiKarte.width()*idx, 0)

        self.screen.write_to_screen(AsciiKarte.print(self.ablageStapel.top()),
                                    self.screen.width - AsciiKarte.width()*2, 0)
        if self.navigation:
            self.screen.write_to_screen(
                f"[{len(self.anlageStapel)}]", self.screen.width - AsciiKarte.width()*2+1, AsciiKarte.height()+1)
        self.screen.write_to_screen(AsciiKarte.print(self.ziehStapel.top()),
                                    self.screen.width - AsciiKarte.width(), 0)
        
        for idx, a in enumerate(self.anlageStapel):
            self.screen.write_to_screen(
                a.printFanned(), AsciiKarte.width()*idx, AsciiKarte.height()+4)
            if self.navigation:
                self.screen.write_to_screen(
                    f"[{idx}]", AsciiKarte.width()*idx+1, AsciiKarte.height()+3)

        self.screen.write_to_screen(self._menu(), 0, AsciiKarte.height() + 26)
        self.screen.write_to_screen(self.status_msg, 0, AsciiKarte.height() + 24)
        self.screen.print()

    def _menu(self):
        menu = "".join(["─" for i in range(self.screen.width)]) + "\n"
        idx = 1
        for cmd in [v["text"] for k, v in self.COMMANDS.items()]:
            menu += cmd + "\t"
            if idx % 4 == 0:
                menu += "\n"
            idx += 1
        return menu

    def _input(self):
        eingabe: str = input("Option: ").lower().strip()
        if eingabe in self.COMMANDS:
            exec(self.COMMANDS[eingabe]["method"])
        else:
            self._write_message(
                f"Ungültige eingabe: {eingabe}! Bitte wählen sie eine gültige Option.")

    def _write_message(self, text: str):
        self.status_msg = text

    def _end(self):
        print("Danke das sie Solitair gespielt haben!")
        exit(0)

    def _get_number(self, msg: str, range: range) -> int:
        num = ""
        while True:
            num = input(msg).strip()
            if num.isdigit() and int(num) in range:
                return int(num)
            else:
                self._write_message("Bitte geben sie eine gültige Zahl an!")

    def _toggle_navigation(self):
        self.navigation = not self.navigation
        self._draw()

    def _umdrehen(self):
        if self.ziehStapel.leer():
            k = self.ablageStapel.ziehen()
            while k:
                self.ziehStapel.anlegen(k.zudecken())
                k = self.ablageStapel.ziehen()
            self.ziehStapel.shuffle()
        else:
            self._write_message("Umdrehen nicht möglich, es sind noch Karten auf dem Stapel!")

    def _ziehen(self):
        k = self.ziehStapel.ziehen()
        if k:
            self.ablageStapel.anlegen(k.aufdecken())

    def _ablegen(self):
        self._toggle_navigation()
        idx = self._get_number(
            "Welchen Stapel möchten sie ablegen?", range(0, len(self.anlageStapel)+1))
        self._toggle_navigation()
        k: Karte = None
        if idx < len(self.anlageStapel):
            stapel = self.anlageStapel[idx].stapel
        elif idx == len(self.anlageStapel):
            stapel = self.ablageStapel

        k = stapel.top()
        msg = ""
        if k:
            for s in [self.ablageHerz, self.ablageKaro, self.ablagePik, self.ablageKreuz]:
                if k.farbe == s.farbe:
                    if s.anlegbar(k):  
                        s.anlegen(stapel.ziehen())
                        stapel.aufdecken()
                        break
                    else:
                        msg = f"Karte {k.farbe.blatt} {k.typ.name.capitalize()} kann nicht abgelegt werden!"
            self._write_message(msg)
                
    def _anlegen(self):
        pass

    def _verschieben(self):
        pass

    def play(self):
        self._draw()
        # the game loop
        while True:
            self.status_msg = ""
            self._input()
            self.screen.clear_screen()
            self._draw()


def main():
    '''
    The enty program for the solitair program
    '''
    s = Solitair()
    s.play()


if __name__ == "__main__":
    main()
