from cards import Karte, Stapel, AnlageStapel, AblageStapel, Farbe, KartenTyp
from ascii import AsciiScreen, AsciiKarte, AsciiStapel


class Solitair(object):
    """
    Basis Klasse für Solitär

    Die Klasse initialsiert alle wichtigen elemente und startet das spiel mit play()
    """

    SOLITAIR = """
        ███████╗ ██████╗ ██╗     ██╗████████╗ █████╗ ██╗██████╗                       
        ██╔════╝██╔═══██╗██║     ██║╚══██╔══╝██╔══██╗██║██╔══██╗                      
        ███████╗██║   ██║██║     ██║   ██║   ███████║██║██████╔╝                      
        ╚════██║██║   ██║██║     ██║   ██║   ██╔══██║██║██╔══██╗                      
        ███████║╚██████╔╝███████╗██║   ██║   ██║  ██║██║██║  ██║                      
        ╚══════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
                        (c) 2023 Stefan Langer"""

    COMMANDS = {"z": {"text": "[z]iehen", "method": f"self._ziehen()"},
                "a": {"text": "[a]nlegen", "method": f"self._anlegen()"},
                "l": {"text": "ab[l]egen", "method": f"self._ablegen()"},
                "m": {"text": "neu [m]ischen", "method": f"self._neu_mischen()"},
                "v": {"text": "[v]erschieben", "method": f"self._verschieben()"},
                "u": {"text": "[u]mdrehen", "method": f"self._umdrehen()"},
                "b": {"text": "[b]eenden", "method": f"self._end()"}, }

    def __init__(self) -> None:
        '''
        Der Konstruktor für die Klasse Solitair. Im Konstruktor werden die verschiedenen Spielelemente
        erzeugt. 
        1. Der Stapel von dem Karten gezogen werden 
        2. Die Ablagestapel wo die Karten final abgelegt werden
        3. Die 7 Anlagestapel wo die Karten während des Spiels sortiert werden
        4. Der AsciiScreen auf den das Spielfeld dargestellt wird
        5. Das Menü und die Navigationshilfen um das Spiel zu bedienen
        '''
        self.ziehStapel = Stapel(karten=[Karte(col, type) for col in list(Farbe)
                                         for type in list(KartenTyp)])
        self.ziehStapel.shuffle()
        self.ablageStapel = Stapel()
        self.ablageHerz = AblageStapel(farbe=Farbe.HERZ)
        self.ablageKaro = AblageStapel(farbe=Farbe.KARO)
        self.ablageKreuz = AblageStapel(farbe=Farbe.KREUZ)
        self.ablagePik = AblageStapel(farbe=Farbe.PIK)
        self.screen = AsciiScreen(width=74, height=AsciiKarte.height()*2 + 33)
        self.navigation = False
        self.navigation_anlage = False
        self.navigation_ablage = False
        self.status_msg = ""
        self.anlageStapel = [AsciiStapel(karten=self._initAnlage(i+1))
                             for i in range(7)]

    def _initAnlage(self, kartenZiehen: int) -> list[Karte]:
        """
        Hilfs methode um die Anlagestapel zu initialisieren.
        Die methode zieht die angegebenen Anzahl von Karten vom Stapel und gibt sie als list[Karte] zurück.

        kartenZiehen - `int` die Anzahl der verdeckten Karten die zurückgegeben werden
        """
        karten = []
        for i in range(kartenZiehen):
            karten.append(self.ziehStapel.ziehen())
            if i == kartenZiehen-1:
                karten[i].aufdecken()
        return karten

    def _draw(self) -> None:
        """
        Malt das Spielfeld in dem es die notwendigen Ascii zeichen auf den AsciiScreen schreibt und anschliessend
        print aufruft. 

        Siehe auch self.write_to_screen()
        """
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

    def _menu(self) -> str:
        """
        Generiert das Menü, dass in self.COMMANDS definiert ist. 
        """
        menu = "".join(["─" for i in range(self.screen.width)]) + "\n"
        idx = 1
        for cmd in [v["text"] for k, v in self.COMMANDS.items()]:
            menu += cmd + "\t"
            if idx % 4 == 0:
                menu += "\n"
            idx += 1
        return menu

    def _input(self):
        """
        Verarbeitet die Menüeingaben. Die Eingabe wird gegen self.COMMANDOS geprüft. Wird das Kommando 
        gefunden wird die hinterlegte methode ausgeführt. Ansonsten wird eine Fehlermeldung ausgegeben.
        """
        eingabe: str = input("Option: ").lower().strip()
        if eingabe in self.COMMANDS:
            exec(self.COMMANDS[eingabe]["method"])
        else:
            self._write_message(
                f"Ungültige eingabe: {eingabe}! Bitte wählen sie eine gültige Option.")

    def _write_message(self, text: str):
        """
        Speichert die angegebene Status message in den internen Puffer. Beim nächste aufruf von print wird die 
        Statusnachricht angzeigt.

        text - `str` die Statusnachricht
        """
        self.status_msg = text

    def _get_number(self, msg: str, range: range) -> int:
        """
        Fragt den user nach einer nummerischen Eingabe. 
        Die Frage wird so lange wiederholt bis die Eingabe valide ist.

            msg - `str`  die Frage für die Eingabe
          range - `range` das Intervall in dem sich die Eingabe befinden muss. Das obere Ende der Range is exklusive
        """
        num = ""
        while True:
            num = input(msg).strip()
            if num.isdigit() and int(num) in range:
                return int(num)
            else:
                self._write_message("Bitte geben sie eine gültige Zahl an!")
                self._draw()

    def _show_navigation(self, withAblage=False):
        """
        Setzt navigation flag auf True so dass die Eingabehilfe beim nächsten screen.print() mit angezeigt wird

        withAblage - `bool` sagt ob die Navigationshilfe für den Ablagestapel ebenfalls angezeigt werden soll
        """
        self.navigation_anlage = True
        if withAblage:
            self.navigation_ablage = True
        self._draw()

    def _hide_navigation(self):
        """
        Setzt das Navigationsflag auf False so dass die Eingabehilfe beim naächen screen.print() nicht mehr angezeigt wird. 
        """
        self.navigation_anlage = False
        self.navigation_ablage = False

    def _end(self):
        """
        Method wird aufgerufen wenn der beenden Menüpunkt gewählt wird.
        Die Methode gibt den Endscreen aus und beendet dann das Programm mit exit(0)
        """
        self.screen.clear_screen()
        self.screen.write_to_screen(self.SOLITAIR + """  
                Danke das sie Solitair gespielt haben!              
""", 0, 10)
        self.screen.print()
        exit(0)

    def _umdrehen(self):
        """
        Die Methode wird aufgerufen wenn der umdrehen Menüpunkt ausgewählt wird. 
        Zunächst wird gepräft ob der Ziehstapel leer ist und falls ja werden die Karten 
        auf dem Ablagestapel neugemischt und verdeckt auf den Ziehstapel abgelegt.
        """
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
        """
        Die Method wird aufgerufen wenn der ziehen Menüpunkt ausgewählt wird.
        Es wird eine Karte vom Stapel gezogen und auf den Ablagestapel gelegt. 
        """
        k = self.ziehStapel.ziehen()
        if k:
            self.ablageStapel.anlegen(k.aufdecken())

    def _ablegen(self):
        """
        Die Methode wird aufgerufen wenn der ablegen Menüpunkt ausgewählt wird. 
        Die Method 
        * zeigt zunächst das Navigationshilemenü
        * dann fragt es nach dem Stapel von dem die Karte genommen werden soll
        * dann wird überprüft ob die Karte tatsächlich abgelegt werden kann
            * wenn nein dann wird eine Fehlernachricht angezeigt und der Vorgan abgebrochen
            * wenn ja dann wird die Karte auf dem entsprechenden Ablagestapel abgelegt
        """
        self._show_navigation(withAblage=True)
        idx = self._get_number(
            "Welchen Stapel möchten sie ablegen? ", range(0, len(self.anlageStapel)+1))
        self._hide_navigation()
        if idx < len(self.anlageStapel):
            stapel = self.anlageStapel[idx]
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
        """
        Die Method wird aufgerufen wenn der anlege Menüpunkt ausgwählt wird.
        Die Method
        * zeigt das Navigationshilfemenü an
        * Fragt dann nach dem Anlagestapel an den angelegt werden soll
        * Überprüft dann ob die Karte angelegt werden kann
            * wenn ja dann wir die Karte vom Ablagestapel genommen und angelegt
            * wenn nein wird eine Fehlermeldung angezeigt und der Vorgang abgebrochen
        """
        k = self.ablageStapel.top()
        if k:
            self._show_navigation(withAblage=False)
            idx = self._get_number(f"Wo möchten sie die Karte {k.farbe.blatt} {k.typ.blatt} anlegen? ",
                                   range(0, len(self.anlageStapel)))
            self._hide_navigation()
            stapel = self.anlageStapel[idx]

            if stapel.anlegbar(k):
                stapel.anlegen(self.ablageStapel.ziehen())
            else:
                self._write_message(
                    f"Karte {k.farbe.blatt} {k.typ.blatt} kann nicht an Stapel [{idx}] angelegt werden!")

    def _verschieben(self):
        """
        Die Method wird aufgerufen wenn der verschieben Menüpunkt ausgwählt wird.
        Die Method
        * zeigt das Navigationshilfemenü an
        * Fragt nach von welchem Stapel Karten verschoben werden sollen
        * Fragt nach zu welchen Stapel die Karten verschoben werden sollen
        * Versucht dann die Karten mit Stapel.verschieben_nach(zielStapel) zu verschieben
            * wenn das klappt werden die Karten verschoben
            * wenn nicht dann wird eine Fehlermeldung angezeigt und der Vorgang wird abgebrochen
        """
        self._show_navigation(withAblage=False)
        von = self._get_number(f"Von welchem Stapel wollen sie Karten verschieben? ",
                               range(0, len(self.anlageStapel)))
        vonStapel = self.anlageStapel[von].stapel
        self._write_message(f"Verschieben von Stapel {von}")
        self._draw()
        zu = self._get_number(f"Zu welchem Stapel wollen sie die Karten verschieben? ",
                              range(0, len(self.anlageStapel)))
        zuStapel = self.anlageStapel[zu]
        self._hide_navigation()
        if not vonStapel.verschieben_nach(zuStapel):
            self._write_message(
                f"Verschieben von Stapel {von} auf Stapel {zu} nicht möglich!")
        else:
            self._write_message("")

    def _gewonnen(self):
        """
        Überprüft ob das Spiel gewonnen ist. 
        Wenn alle Ablagestapel komplett sind wird True zurückgegeben ansonsten False.
        """
        return self.ablageHerz.komplett() and self.ablageKaro.komplett() and self.ablageKreuz.komplett() and self.ablagePik.komplett()

    def _ja_nein_frage(self, frage: str) -> bool:
        """
        Stellt die Ja-Nein-Frage `frage` und gibt `True` zurück wenn der User mit Ja antwortet ansonsten `False`.

        frage - `str` Die Ja-Nein-Frage die gestellt werden soll.
        """
        while True:
            eingabe = input(f"{frage} (j/n)")
            if eingabe.lower() == "j":
                return True
            elif eingabe.lower() == "n":
                return False
            else:
                self._write_message(
                    "Bitte geben sie j für Ja oder n für Nein ein!")
                self._draw()

    def _neu_mischen(self):
        """
        Mischt alle Karten auf dem Spielfeld neu durch.
        """
        if self._ja_nein_frage("Wollen sie die Karten wirklich neu mischen?"):
            for a in self.anlageStapel+[self.ablageStapel]:
                while not a.leer():
                    k = a.ziehen()
                    k.zudecken()
                    self.ziehStapel.anlegen(k)

            self.ziehStapel.shuffle()
            self.anlageStapel = [AsciiStapel(karten=self._initAnlage(i+1))
                                 for i in range(7) if self.ziehStapel.karten_anzahl() > i]

    def _draw_welcome(self):
        """
        Zeigt den Welcome Screen für das Spiel an.
        """
        self.screen.clear_screen()
        self.screen.write_to_screen(self.SOLITAIR + """  
                     Drücke Enter um fortzufahren                   
""", 0, 10)
        self.screen.print()

    def _draw_gewonnen(self):
        """
        Zeigt den Sieger Screen für das Spiel an. 
        """
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
""", 0, 10)
        self.screen.print()

    def play(self):
        """
        Methode führt das Spiel aus. 
        * zuerst wird der Willkommens Screen angezeigt
        * dann wird das Spielfeld angezeigt
        * als nächstes wird die Spielschleife gestartet die solange läuft bis das Spiel 
          gewonnen wurde oder der Benutzer das Spiel beendet
        * Die Spielschleife führt folgende Kommandos der Reiche nach aus:
            * Zunächst wird der Statusnachrichtenpuffer gelöscht
            * Dann wird die Eingabe des Spielers verarbeitet
            * Anschliessend wird der Bildschirm gelöscht 
            * um dann den neuen Zustand des Spiels anzuzeigen
        * wenn die Schleife durch einen Sieg beendet wird wird der Siegerbildschirm angezeigt
        * und das Spiel beendet
        """
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


if __name__ == "__main__":
    s = Solitair()
    s.play()
