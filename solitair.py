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
        self.screen = AsciiScreen(width=74, height=AsciiKarte.height()*2 + 33)
        self.navigation = False
        self.navigation_anlage = False
        self.navigation_ablage = False
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
                                        AsciiKarte.width()*idx+2, 0)

        self.screen.write_to_screen(AsciiKarte.print(self.ablageStapel.top()),
                                    self.screen.width - AsciiKarte.width()*2-2, 0)
        if self.navigation_ablage:
            self.screen.write_to_screen(
                f"[{len(self.anlageStapel)}]", self.screen.width - AsciiKarte.width()*2-1, AsciiKarte.height()+1)
        self.screen.write_to_screen(AsciiKarte.print(self.ziehStapel.top()),
                                    self.screen.width - AsciiKarte.width()-2, 0)

        for idx, a in enumerate(self.anlageStapel):
            self.screen.write_to_screen(
                a.printFanned(), AsciiKarte.width()*idx+2, AsciiKarte.height()+4)
            if self.navigation_anlage:
                self.screen.write_to_screen(
                    f"[{idx}]", AsciiKarte.width()*idx+3, AsciiKarte.height()+3)

        self.screen.write_to_screen(
            self._menu(), 0, AsciiKarte.height()*2 + 29)
        self.screen.write_to_screen(
            self.status_msg, 2, AsciiKarte.height()*2 + 27)
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

    def _get_number(self, msg: str, range: range) -> int:
        num = ""
        while True:
            num = input(msg).strip()
            if num.isdigit() and int(num) in range:
                return int(num)
            else:
                self._write_message("Bitte geben sie eine gültige Zahl an!")
                self._draw()

    def _show_navigation(self, withAblage=False):
        self.navigation_anlage = True
        if withAblage:
            self.navigation_ablage = True
        self._draw()

    def _hide_navigation(self):
        self.navigation_anlage = False
        self.navigation_ablage = False

    def _end(self):
        print("Danke das sie Solitair gespielt haben!")
        exit(0)

    def _umdrehen(self):
        if self.ziehStapel.leer():
            k = self.ablageStapel.ziehen()
            while k:
                self.ziehStapel.anlegen(k.zudecken())
                k = self.ablageStapel.ziehen()
            self.ziehStapel.shuffle()
        else:
            self._write_message(
                "Umdrehen nicht möglich, es sind noch Karten auf dem Stapel!")

    def _ziehen(self):
        k = self.ziehStapel.ziehen()
        if k:
            self.ablageStapel.anlegen(k.aufdecken())

    def _ablegen(self):
        self._show_navigation(withAblage=True)
        idx = self._get_number(
            "Welchen Stapel möchten sie ablegen? ", range(0, len(self.anlageStapel)+1))
        self._hide_navigation()
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
        k = self.ablageStapel.top()
        if k:
            self._show_navigation(withAblage=False)
            idx = self._get_number(f"Wo möchten sie die Karte {k.farbe.blatt} {k.typ.blatt} anlegen? ",
                                   range(0, len(self.anlageStapel)))
            self._hide_navigation()
            stapel = self.anlageStapel[idx].stapel

            if stapel.anlegbar(k):
                stapel.anlegen(self.ablageStapel.ziehen())
            else:
                self._write_message(
                    f"Karte {k.farbe.blatt} {k.typ.blatt} kann nicht an Stapel [{idx}] angelegt werden!")

    def _verschieben(self):
        self._show_navigation(withAblage=False)
        von = self._get_number(f"Von welchem Stapel wollen sie Karten verschieben? ",
                               range(0, len(self.anlageStapel)))
        vonStapel = self.anlageStapel[von].stapel
        self._write_message(f"Verschieben von Stapel {von}")
        self._draw()
        zu = self._get_number(f"Zu welchem Stapel wollen sie die Karten verschieben? ",
                              range(0, len(self.anlageStapel)))
        zuStapel = self.anlageStapel[zu].stapel
        self._hide_navigation()
        if not vonStapel.verschieben_nach(zuStapel):
            self._write_message(
                f"Verschieben von Stapel {von} auf Stapel {zu} nicht möglich!")
        else:
            self._write_message("")

    def _gewonnen(self):
        return self.ablageHerz.komplett() and self.ablageKaro.komplett() and self.ablageKreuz.komplett() and self.ablagePik.komplett()

    def _draw_welcome(self):
        self.screen.clear_screen()
        self.screen.write_to_screen("""
        ███████╗ ██████╗ ██╗     ██╗████████╗ █████╗ ██╗██████╗                       
        ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔══██╗██║██╔══██╗                      
        ███████╗██║   ██║██║     ██║   ██║   ███████║██║██████╔╝                      
        ╚════██║██║   ██║██║     ██║   ██║   ██╔══██║██║██╔══██╗                      
        ███████║╚██████╔╝███████╗██║   ██║   ██║  ██║██║██║  ██║                      
        ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
                        (c) 2023 Stefan Langer
                
                     Drücke Enter um fortzufahren                   
""", 0,10)
        self.screen.print()

    def _draw_gewonnen(self):
        self.screen.clear_screen()
        self.screen.write_to_screen("""
        ███████╗ ██████╗ ██╗     ██╗████████╗ █████╗ ██╗██████╗ 
        ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔══██╗██║██╔══██╗
        ███████╗██║   ██║██║     ██║   ██║   ███████║██║██████╔╝
        ╚════██║██║   ██║██║     ██║   ██║   ██╔══██║██║██╔══██╗
        ███████║╚██████╔╝███████╗██║   ██║   ██║  ██║██║██║  ██║
        ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝

 ██████╗ ███████╗██╗    ██╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗███╗   ██╗
██╔════╝ ██╔════╝██║    ██║██╔═══██╗████╗  ██║████╗  ██║██╔════╝████╗  ██║
██║  ███╗█████╗  ██║ █╗ ██║██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██╔██╗ ██║
██║   ██║██╔══╝  ██║███╗██║██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║╚██╗██║
╚██████╔╝███████╗╚███╔███╔╝╚██████╔╝██║ ╚████║██║ ╚████║███████╗██║ ╚████║
 ╚═════╝ ╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝

                        (c) 2023 Stefan Langer
""", 0,10)
        self.screen.print()

    def play(self):
        self._draw_welcome()
        input()
        self.screen.clear_screen()
        self._draw()
        # the game loop
        while not self._gewonnen():
            self.status_msg = ""
            self._input()
            self.screen.clear_screen()
            self._draw()
        self._draw_gewonnen()
        input()


def main():
    '''
    The enty program for the solitair program
    '''
    s = Solitair()
    s.play()


if __name__ == "__main__":
    main()
